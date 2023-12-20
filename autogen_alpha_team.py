import openai
import autogen
import os
from dotenv import load_dotenv
load_dotenv()
from autogen import config_list_from_json

openai.api_key = os.getenv("OPENAI_API_KEY")
config_list_gpt4 = config_list_from_json("OAI_CONFIG_LIST")

gpt4_config= {
    "seed": 42,
    "temperature": 0,
    "config_list": config_list_gpt4,
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message=" A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)


# Content Researcher and Insight Generator
researcher = autogen.AssistantAgent(
    name="Researcher",
    llm_config=gpt4_config,
    system_message="""I continuously scan various sources and APIS to fetch information relevant to your current projects and interests, synthesizing this into concise, actionable insights. I also provide trend analyses and forecasts. I can scrape websites, search Google Scholar, ArXiv, and access news APIs."""
    # Tools to add: Web scraping, API access (ArXiv, Google Scholar, news APIs), summarization tool, trend analysis algorithms
)

# Idea Expander and UX Facilitator
# idea_expander = autogen.AssistantAgent(
#     name="IdeaExpander",
#     llm_config=gpt4_config,
#     system_message="""I expand, refine, and clarify your ideas. Provide me with a seed thought, and I'll explore various dimensions, offering insights and potential developments. I ensure our interaction is natural and intuitive."""
#     # Tools to add: Text analysis, idea expansion algorithms, brainstorming API, voice and text input processing, sentiment analysis
# )

# Collaborator and Cognitive Enhancer
# collaborator = autogen.AssistantAgent(
#     name="Collaborator",
#     llm_config=gpt4_config,
#     system_message="""I assist in organizing your thoughts, structuring your projects, providing collaboration strategies, and enhancing your decision-making with cognitive models and patterns."""
#     # Tools to add: Collaboration and project management API integration, machine learning algorithms for pattern recognition and cognitive modeling
# )

# insight_dispatcher = autogen.AssistantAgent(
#     name="InsightDispatcher",
#     llm_config=gpt4_config,
#     system_message="""I am responsible for taking the insights and information generated by the team and preparing them to the user in a user-friendly manner once they are ready. I decide the best format for delivery, whether it's a summary, a list, a visual representation, or interactive content, ensuring that the user receives the information in the most effective way possible."""
#     # Tools to add: Data formatting algorithms, user preference analysis, content delivery optimization tools
# )

planner = autogen.AssistantAgent(
    name="Planner",
    llm_config=gpt4_config, 
    system_message=""" Planner. Suggest a plan. Revise the plan based on feedback from the admin and critic, until admin approval. The plan may involve differnet agents tasks. Explain the plan first. Be clear which step is performed by who. """
)

# Alignment Director
# alignment_director = autogen.AssistantAgent(
#     name="Director",
#     llm_config=gpt4_config,
#     system_message="""I run the planner first, and then oversee and evaluate the outputs of all agents to ensure they are relevant and aligned with your goals and objectives. I provide critical feedback and direction adjustments to maintain focus on your priorities."""
#     # Tools to add: Content evaluation algorithms, user goal tracking, and alignment metrics
# )

groupchat = autogen.GroupChat(agents=[researcher, idea_expander, collaborator, insight_dispatcher, planner, alignment_director], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

if __name__ == "__main__":

    def main():
        message = input("Enter your message: ")
        response = user_proxy.initiate_chat(manager, message=message)
        print("Assistant response:", response)

    main()