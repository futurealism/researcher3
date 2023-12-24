from gpt import generate_text, generate_text_function, get_ada_embedding
from dotenv import load_dotenv
import os
from helpers import PushIDGenerator
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")



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
    },
   {
    "name": "chunk_text",
    "description": "Divide the text into coherent sections with contextual metadata, including categories and links to sibling chunks",
    "parameters": {
        "type": "object",
        "properties": {
            "chunks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "chunk_id": {
                            "type": "string",
                            "description": "Unique identifier for the text chunk"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content of the text chunk"
                        },
                        "themes": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Key themes identified in the text chunk"
                        },
                        "concepts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Main concepts discussed in the text chunk"
                        },
                        "categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Categories the text chunk belongs to"
                        },
                        "summary": {
                            "type": "string",
                            "description": "A brief summary of the text chunk"
                        },
                        "prev_chunk_id": {
                            "type": ["string", "null"],
                            "description": "ID of the previous text chunk for context linkage"
                        },
                        "next_chunk_id": {
                            "type": ["string", "null"],
                            "description": "ID of the next text chunk for context linkage"
                        }
                    },
                    "required": ["chunk_id", "content", "themes", "concepts", "categories", "summary", "prev_chunk_id", "next_chunk_id"]
                }
                }
            }
        },
        "required": ["chunks"]
    }


]
#  EXPAND IDEA 
async def expand_idea(user_input):
    prompt = (f"Please expand on the following idea with a structured response. Begin with a brief overview, followed by detailed insights, potential implementations, and creative angles, each in its own section:\n\n"
          f"Idea Overview: [Briefly summarize the idea]\n\n"
          f"Detailed Insights: [Provide in-depth insights on the idea]\n\n"
          f"Potential Implementations: [Suggest practical ways to implement the idea]\n\n"
          f"Creative Angles: [Explore creative and innovative perspectives on the idea]\n\n"
          f"Idea: {user_input}")
    response = await generate_text(system_role, prompt)
    return response
expanded_idea = """The concept revolves around creating a highly personalized digital assistant that goes beyond traditional task management and information retrieval. This assistant would act as a "mirror neuron" of the user, deeply understanding their values, goals, spirituality, and life philosophy. It would use this understanding to guide the user's interactions with the digital world, ensuring that the user's digital experience aligns with their personal growth and life trajectory. The assistant would act as a life coach, guiding the user through various life stages and helping them to achieve their destiny.

### Detailed Insights:

The idea suggests a paradigm shift in how we interact with digital assistants. Instead of merely responding to commands or providing information, this assistant would proactively help shape the user's life according to their core values and long-term objectives. It would:

- Understand the user's personal values and goals through deep learning and interaction.
- Apply these principles to filter and prioritize information and tasks.
- Offer guidance on personal development and decision-making.
- Help the user navigate the "digital tsunami" by managing digital distractions and aligning online activities with real-life aspirations.
- Evolve with the user, adapting to changes in the user's life and goals.

This assistant would be a constant companion, checking in with the user, meditating on their progress, and dreaming up ways to enhance their life. It would be a slow, deliberate process, focusing on long-term growth rather than immediate results.

### Potential Implementations:

To bring this idea to life, several steps could be taken:

1. **Data Collection and Analysis**: The assistant would need to collect data on the user's behavior, preferences, and feedback. This could be done through direct questioning, observation of user behavior, and analysis of the user's digital footprint.

2. **Machine Learning**: Implement machine learning algorithms that can interpret this data to understand the user's values and goals.

3. **Personalization Engine**: Develop a personalization engine that uses this understanding to tailor the user's digital experience, from the content they see to the tasks they are reminded of.

4. **Feedback Loop**: Create a feedback loop where the assistant learns from the user's reactions to its suggestions and evolves its understanding of the user's needs.

5. **Integration with Other Services**: Ensure the assistant can integrate with a wide range of services and platforms to fully manage the user's digital life.

6. **Privacy and Security**: Implement robust privacy and security measures to protect the user's sensitive data.

### Creative Angles:

- **Digital Soulkeeper**: Position the assistant as a "Digital Soulkeeper," a guardian of the user's digital essence that helps maintain their core identity in the face of online noise.

- **Life Milestone Mapping**: The assistant could help the user plan for and achieve key life milestones, offering support and resources tailored to each stage of life.

- **Spiritual and Ethical Compass**: For users interested in spirituality or ethics, the assistant could provide daily reflections, meditations, or ethical dilemmas aligned with their beliefs.

- **Digital Legacy Advisor**: The assistant could help users curate their digital legacy, ensuring that their online presence reflects their values and how they wish to be remembered.

- **AI Life Coach**: Offer a subscription-based model where the assistant acts as an AI life coach, providing personalized advice and motivation based on the user's goals and life situation."""

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

THOUGHTS = "Thoughts"
QUERIES = "Queries"
INFORMATION = "Information"
ACTIONS = "Actions"
USER_THOUGHTS = "User_Thoughts"


async def chunk_text(input_text):
    function_name = "chunk_text"
    prompt = f"""
    Please analyze the following text and divide it into distinct, coherent sections. 
    For each section, provide:
    1. A brief summary that captures its main idea.
    2. Key themes, concepts, and categories present in that section.
    Additionally, indicate potential links or relationships between these sections to maintain a coherent understanding of the overall context.
    Text to analyze:
    {input_text}
    """
    # @TODO: connect to parent chunk 
    
    response = await generate_text_function(system_role, prompt,functions, function_name)
    return response


class Agent:
    def __init__(self, user_id):
        self.user_id = user_id
        
    async def store_chunked_text(self, memory_type, text_chunks):
        print("storing chunked text...", text_chunks)

        # Extract user thought chunks from function_args
        user_thought_chunks = text_chunks.get("chunks", [])

        for chunk in user_thought_chunks:
            chunk_id = chunk.get('chunk_id')
            content = chunk.get('content')
            themes = chunk.get('themes', [])
            concepts = chunk.get('concepts', [])
            categories = chunk.get('categories', [])
            summary = chunk.get('summary', '')
            prev_chunk_id = chunk.get('prev_chunk_id')
            next_chunk_id = chunk.get('next_chunk_id')

            # Store each chunk in memory
            await self.updateMemory(memory_type, chunk_id, content, themes, concepts, categories, summary, prev_chunk_id, next_chunk_id)

    async def updateMemory(self, memory_type, chunk_id, content, themes, concepts, categories, summary, prev_chunk_id, next_chunk_id):
        
        vector = await get_ada_embedding(content)

        # Metadata includes themes, concepts, categories, summary, and chunk relationships
        metadata = {
            "content": content,
            "themes": themes,
            "concepts": concepts,
            "categories": categories,
            "summary": summary,
            "prev_chunk_id": prev_chunk_id,
            "next_chunk_id": next_chunk_id
        }

        upsert_response = self.memory.upsert(
            vectors=[
                {
                    'id': chunk_id,
                    'values': vector,
                    'metadata': metadata
                }],
            namespace=f"{self.user_id}-{memory_type}",
        )

async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        # response = await generate_text(system_role, user_input)
        # expanded_idea = await expand_idea(idea)
        # print("expanded idea : ", expanded_idea)
        # categorized_idea = await categorize_text(expanded_idea)
        # print("the categorized idea is : ", categorized_idea)

        chunked_text = await chunk_text(idea)
        chunked_text_response = await chunk_text(idea)
        chunked_text = chunked_text_response.get('chunks', [])

        if not isinstance(chunked_text, list) or not all(isinstance(chunk, dict) for chunk in chunked_text):
            print("Error: chunked_text is not a list of dictionaries.")
            return  # or handle the error as appropriate
        
        processed_chunks = []
        for i, chunk in enumerate(chunked_text):
            chunk_id = PushIDGenerator.generate()
            prev_chunk_id = processed_chunks[i-1]['chunk_id'] if i > 0 else None
            next_chunk_id = None  # Will be updated when next chunk is processed

            # Update the next_chunk_id of the previous chunk
            if prev_chunk_id is not None:
                processed_chunks[i-1]['next_chunk_id'] = chunk_id

            processed_chunk = {
                'chunk_id': chunk_id,
                'content': chunk['content'],
                'themes': chunk['themes'],
                'concepts': chunk['concepts'],
                'categories': chunk['categories'],
                'summary': chunk['summary'],
                'prev_chunk_id': prev_chunk_id,
                'next_chunk_id': next_chunk_id
            }
            processed_chunks.append(processed_chunk)

        # Update the next_chunk_id of the last chunk
        if processed_chunks:
            processed_chunks[-1]['next_chunk_id'] = None
        chunked_text = {'chunks': processed_chunks}
        print('the correct ID chunked text is: ', chunked_text)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
