from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen
import os
from dotenv import load_dotenv

load_dotenv()
config_list = config_list_from_json("OAI_CONFIG_LIST")

# ------------------ Create agent ------------------ #

# Create user proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    system_message="I am your personal interface with Alpha. Share your thoughts, ideas, or queries, and I'll guide our conversation.",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1
)

# Create idea expander agent
idea_expander = GPTAssistantAgent(
    name="idea_expander",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_idea_expander_id"  # Placeholder for actual ID
    },
    system_message="I help expand and refine your ideas. Share a concept, and I'll explore various dimensions and offer insights."
)

# Create collaboration facilitator agent
collaboration_facilitator = GPTAssistantAgent(
    name="collaboration_facilitator",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_collaboration_facilitator_id"  # Placeholder for actual ID
    },
    system_message="I assist in organizing your thoughts and structuring your projects for effective collaboration."
)

# Create feedback processor agent
feedback_processor = GPTAssistantAgent(
    name="feedback_processor",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_feedback_processor_id",  # Placeholder for actual ID
    },
    system_message="I analyze your feedback to refine Alpha's responses and ensure they align with your needs."
)

# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, idea_expander, collaboration_facilitator, feedback_processor], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

if __name__ == "__main__":

    def main():
        message = input("Enter your message: ")
        response = user_proxy.initiate_chat(group_chat_manager, message=message)
        print("Assistant response:", response)

    main()
