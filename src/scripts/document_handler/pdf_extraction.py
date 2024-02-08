from PyPDF2 import PdfReader
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter

class PdfExtraction:
    def __init__(self) -> None:
        self.pdf_page_count = 0
        self.text = ""
   
    
    def get_page_count(self, file):
            pdf_reader = PyPDF2.PdfFileReader(file)
            page_count = pdf_reader.numPages
            return page_count


    def get_pdf_text(self,pdf_path):
        self.pdf_page_count = self.get_page_count(pdf_path)
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                self.text += page.extractText()
            return self.text
        

    def get_text_chunks(self, text):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
    



    




