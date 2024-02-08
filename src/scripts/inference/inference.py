from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Inference():
    def __init__(self, input_data) -> None:
        self.prompt = input_data['prompt']
        if "name" in input_data.keys():
            self.name = input_data['name']

    def load_vectorstore(self):
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(f"D:/chatbot-repos/generic-assistant/dataset/faiss_index/{self.name}",embeddings)
        return vectorstore

    def get_conversation_chain(self, vectorstore):
        llm = ChatOpenAI()
        # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

        memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain

    def response_main(self):
        text_vectorstore = self.load_vectorstore()
        conversation_chain  = self.get_conversation_chain(text_vectorstore)
        #docs = text_vectorstore.similarity_search(self.prompt )
        response = conversation_chain.run(question=self.prompt )
        # response = response.replace("\n","<br/>")
        return response

class PromptItem(BaseModel):
    prompt: str

@app.post("/ask")
def answer_question(request: PromptItem):
    prompt = request.prompt
    input_data = {}
    input_data['prompt'] = prompt
    input_data['name'] = "fusion_360"
    inference = Inference(input_data)
    return {"response": inference.response_main()}



        