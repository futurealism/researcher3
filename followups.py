from gpt import generate_text, generate_text_function
idea = """Like with advertising and messaging and whatever, but like at a larger frame as the system starts to get more intelligent with, with the idea that at the highest level I am is not just like I mean yes, it's an intelligent messaging platform and there's all these different assistants. But if an assistant something like the Sherpa or maybe there's like this high level like, you know Siri or something or it's like the general assistant or some some Sherpa ish type first responder, but that that thing, it's almost like a mirror neuron of you. That is like, it's not just about the relationship between the general system and the brain and all of the world's information and capabilities and execution tasks. It's about your soul and your life and how it it's almost like this very deeply personal, like life coach, guide, Sherpa, whatever you want to call it, Shaman or Sherpa or whatever, but it really understands your goals. And it really understands what you want out of life and your the way you think about life. Maybe it understands your spirituality or your religion or how you what your values are, I guess is a better way to put it. And because it knows your values and it knows your goals. It can cat waterfall down to the rest of the system. This sort of these principles that dictate how the entire system works, how your whole kingdom basically of information works for you, based on your your principles, values and goals so that you can lead a bigger life and like take back your life like in this digital like tsunami so that these companies aren't just like sucking your soul away like further I don't know what happened. But yeah, that like what you just wrote. Yeah, quality of life assistant. Yeah, exactly. And like, that's almost like that's almost like the highest level like personalization layer because the end result is like your life actually changes. Not just like saving you time or like saving you frustration or making things easier for you the actual progression of how you evolve as a human from like 25 to 35 and from 35 to 45 like actually like your destiny basically gets affected by how well you can, you know, track and achieve and, and evolve essentially. So, to me, that's super interesting. And we can totally do that. It's not that different than anything else. We're doing. It just requires like one level, abstracted. It's just a slower it's like the slower version of the brain basically, like instead of happening in like 30 seconds to two minutes. It's like happening in like three months to two years. And just constantly like running every day being like, you know, how can we be better? Just like checking in meditating, dreaming talking to you observing everything that's happening all right, that was it. Cool. Well, yeah. Just stay in touch. What are you officially going offline? Tuesday the 28th. The end of the day, essentially, I may have some I'm flying on the 29th. So I don't know if I'll have Wi Fi in the airport or not. But I don't think I'll be very productive. But I need to try to get all this stuff done in like the next two days because I have to. I have to prepare. I can't just like work up until the very last minute because then I won't be able to I won't have like the medicine. So I'm just gonna get this stuff. Online. I'm going to try and do this final pass and then get all this stuff online and then All right, I'll see you later."""

system_role = "You are a personal super intelligence companion. your goal is to augment and enchance the user's cognitive abilities, and improve their lives." 
functions = [
    {
        "name": "categorize_text",
        "description": "Identify the key themes, concepts, and categories for the text",
        "parameters": {
           "type": "object",
            "properties": {
                "key_themes" : {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "The key themes identified in the text"
                    }
                },
                "concepts" : {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "The main concepts discussed in the text"
                    }
                },
                "categories" : {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "The categories the text belongs to"
                    }
                }
            }
        }
    }
]
#  EXPAND IDEA 

chat_history = """User: Hi iM, I need to book a table for dinner.

iM: Sure, I can help with that. How many people will be dining?

User: It will be for four people.

iM: Great. Do you have a preferred date and time?

User: Yes, next Saturday at 7 PM.

iM: Any preference for the restaurant's location or cuisine?

User: Somewhere downtown, preferably Italian cuisine.

iM: Okay, how about "La Bella Pasta" in downtown? They have great reviews.

User: Sounds perfect. Please book it.

iM: Done! Your table for four at "La Bella Pasta" is booked for next Saturday at 7 PM. You will receive a confirmation email shortly."""


async def generate_follow_up_plan(chat_history):
    prompt = (
    f"""Based on the provided chat history between a user and 'iM', the AI assistant, I need a comprehensive and strategic follow-up interaction plan. 
    This plan should clearly outline the sequence of steps 'iM' should undertake in future communications with the user. 
    Each step in the plan should be accompanied by a rationale, specifying why it's important and beneficial in the context of the user's needs and preferences as demonstrated in the chat. 
    Additionally, include a proposed schedule for these interactions, explaining the optimal timing for each step to maximize user engagement and satisfaction.
    chat history: {chat_history}"""
)
    response = await generate_text(system_role, prompt)
    return response


async def parse_expanded_response(response):
    sections = {
        "Idea Overview": [],
        "Detailed Insights": [],
        "Potential Implementations": [],
        "Creative Angles": []
    }
    current_section = None

    for line in response.split('\n'):
        if line in sections:
            current_section = line
            continue
        if current_section:
            sections[current_section].append(line)

    return sections

#  REFINE IDEA 



# SEMANTIC ANALYSIS AND CATEGORIZATION
async def categorize_text(text):
    function_name = "categorize_text"
    prompt = (f"Identify the key themes, concepts, and categories for the following expanded idea:\n\n{text}")
    response = await generate_text_function(system_role, prompt, functions,function_name)
    return response

async def main():
    followup_plan = await generate_follow_up_plan(chat_history)
    print("AI: ", followup_plan)
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == 'exit':
    #         break
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
