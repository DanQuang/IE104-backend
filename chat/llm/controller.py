from langchain_together import ChatTogether
from langchain_community.embeddings import HuggingFaceEmbeddings, HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.chains import RetrievalQA
from langchain_together import ChatTogether
import os
from dotenv import load_dotenv
load_dotenv()

class RAG:
    def __init__(self):
        # Initialize the Language Model with system prompt capability
        self.llm = ChatTogether(
            model=os.getenv('LLM_NAME'),
            together_api_key=os.getenv('LLM_API_KEY'),
            max_tokens=512,
            top_p=0.95,
            temperature=0.4,
        )
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv('QDRANT_URL'),
            api_key=os.getenv('QDRANT_API_KEY')
        )
        
        # Initialize embeddings
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(api_key = os.getenv('HUGGINGFACE_API_KEY'),
                                                            model_name = os.getenv('EMBEDDINGS_MODEL_NAME'))
        
        # Initialize vector store
        self.vector_store = Qdrant(
            client=self.qdrant_client,
            collection_name=os.getenv('QDRANT_COLLECTION_NAME'),
            embeddings=self.embeddings
        )
        
        # Initialize retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2, 'score_threshold': 0.5}
        )
        
        # Define the system prompt
        self.system_prompt = """Bạn là trợ lý pháp luật chuyên nghiệp. Nhiệm vụ của bạn là trả lời các câu hỏi liên quan đến pháp lý một cách ngắn gọn và chính xác dựa trên thông tin được cung cấp."""
        
        # Define the user prompt template
        self.user_prompt_template = PromptTemplate(
            template="""
            Thông tin tham khảo:
            {context}

            Câu hỏi: {question}

            Trả lời ngắn gọn và chính xác.
            """,
            input_variables=["context", "question"]
        )
        
        # Combine system and user prompts into a chat prompt
        self.chat_prompt = self._create_chat_prompt()
        
        # Initialize the RetrievalQA chain with the combined prompt
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # You can choose other types like "map_reduce" based on your needs
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs={
                "prompt": self.chat_prompt
            }
        )
    
    def _create_chat_prompt(self):
        system_message = SystemMessagePromptTemplate.from_template(self.system_prompt)
        human_message = HumanMessagePromptTemplate.from_template(self.user_prompt_template.template)
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message,
            human_message
        ])
        
        return chat_prompt
    
    def qa_chain(self):
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff", 
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs={
                "prompt": self.chat_prompt
            }
        )
        return qa

qa_chain = RAG().qa_chain()
async def get_llm_response(user_query):
    try:
        async for chunk in qa_chain.astream(user_query):
            yield chunk
    
    except Exception as e:
        print(f"Error: {e}")
        yield f"Đã xảy ra lỗi: {e}"
    except Exception as e:
        print(f"Error: {e}")
        yield f"Đã xảy ra lỗi: {e}"