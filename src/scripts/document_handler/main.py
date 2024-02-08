from .pdf_extraction import PdfExtraction
pdf_extraction = PdfExtraction()


def document_extraction_main(file_path):
    #classification of doc and extraction
    if file_path.endswith('.pdf'):
        extracted_text = pdf_extraction.get_pdf_text(file_path)
        return extracted_text
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            extracted_text = file.read()
        return extracted_text
    else:
        print("Unsupported file type.")
        return None
    print("pdf extraction")
