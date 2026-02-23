from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings
from dotenv import load_dotenv



def get_chat_model():
    load_dotenv()  # Load environment variables from .env file

    llm = HuggingFaceEndpoint(repo_id="openai/gpt-oss-20b", task="text-generation")
    model = ChatHuggingFace(llm=llm)

    return model