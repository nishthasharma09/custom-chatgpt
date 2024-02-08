from dotenv import load_dotenv
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
# from langchain.callbacks import get_openai_callback

import os
from PyPDF2 import PdfReader
import docx

class CreateFaissIndex:
    def __init__(self, input_data) -> None:
        self.name = input_data['name']
        self.scrapped_data_filepath = "dataset/scrapped_data/" + self.name + ".txt"
        if "dataset_folder" in input_data.keys():
            self.text_input_data = self.read_documents_from_directory(input_data['dataset_folder'])
        else:
            with open(self.scrapped_data_filepath, 'r', encoding="utf-8") as file:
                self.text_input_data = file.read()
    
    def read_pdf(self, file_path):
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            print(e)
            return ''

    def read_word(self, file_path):
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def read_txt(self, file_path):
        with open(file_path, "r",encoding='utf-8') as file:
            text = file.read()
        return text

    def read_documents_from_directory(self, directory):
        combined_text = ""
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.endswith(".pdf"):
                combined_text += self.read_pdf(file_path)
            elif filename.endswith(".docx"):
                combined_text += self.read_word(file_path)
            elif filename.endswith(".txt"):
                combined_text += self.read_txt(file_path)
        return combined_text

    def create_faiss_index(self):
        try:
            # if os.path.exists(f"dataset/faiss_index/{self.name}") == True: 
            #     pass
            # #     print("Data already present in path: ", f"dataset/faiss_index/{self.name}")
            # #     print("Taking old data...")
            # else:
            embeddings = OpenAIEmbeddings()
            
            char_text_splitter = CharacterTextSplitter(separator="\n", 
                                                chunk_size=4000, 
                                                chunk_overlap=0, 
                                                length_function=len)
            
            text_chunks = char_text_splitter.split_text(self.text_input_data)
            docsearch = FAISS.from_texts(text_chunks, embeddings)
            docsearch.save_local(f"D:/chatbot-repos/generic-assistant/dataset/faiss_index/{self.name}")

        except Exception as e:
            print("Could not create faiss_index", e)
