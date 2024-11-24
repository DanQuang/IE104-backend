from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_together import ChatTogether
import os
from dotenv import load_dotenv
load_dotenv()

class GeneralChat:
    def __init__(self):

        self.llm = ChatTogether(
                model=os.getenv('LLM_NAME'),
                together_api_key=os.getenv('LLM_API_KEY'),
                max_tokens=512,
                top_p=0.95,
                temperature=0.4,
            )
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            "Act as an intelligent assistant, providing helpful responses to user inquiries. If you're unsure about, politely indicate that you don't have the information and offer to assist with something else. Let's ensure a friendly and informative interaction!"
        )

        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            "{question}"
        )

        self.chat_template = ChatPromptTemplate.from_messages([
            self.system_message_prompt,
            self.human_message_prompt
        ])

    def make_qa_chain(self):
        chain = self.chat_template | self.llm  
        return chain
    

chain=GeneralChat().make_qa_chain()

async def get_llm_response(user_query):

    async for chunk in chain.astream({
        "question": user_query
    }):
        yield chunk
