# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langchain-community",
#     "langchain-text-splitters",
# ]
# ///
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

async def pdf_loader(file_path:str)->list:
    
    loader = PyPDFLoader(file_path)
    pages = []
    
    async for page in loader.alazy_load():
        pages.append(page)
    return pages  

    


def splitter(doc:list)->list:

    text_splitte = RecursiveCharacterTextSplitter( 
                                                chunk_size=300,
                                                chunk_overlap=30,
                                                length_function=len
                                                )
    for i in range(len(doc)):
       doc[i]=doc[i].page_content.replace("WWW.ANGLICKYZAROK.CZ – individuální výuka angličtiny pro začátečníky i pokročilé, kurzy do \nzaměstnání, přípravné kurzy na maturitu a certifikáty. anglickyzarok@gmail.com","")
    
    whole_splitted_text=text_splitte.create_documents(doc)
        
    return whole_splitted_text
def splitter_with_metadata(doc:list)->list:

    text_splitte = RecursiveCharacterTextSplitter( 
                                                chunk_size=300,
                                                chunk_overlap=30,
                                                length_function=len
                                                )
    for i in range(len(doc)):
        
     doc[i].page_content=doc[i].page_content.replace("""WWW.ANGLICKYZAROK.CZ – individuální výuka angličtiny pro začátečníky i pokročilé, kurzy do 
zaměstnání, přípravné kurzy na maturitu a certifikáty. anglickyzarok@gmail.com""","")
     
    doc[i].page_content=doc[i].page_content.replace("""WWW.ANGLICKYZAROK.CZ – individuální výuka angličtiny pro začátečníky i pokročilé, 
kurzy do zaměstnání, přípravné kurzy na maturitu a certifikáty. anglickyzarok@gmail.com""","")

    
    whole_splitted_text=text_splitte.transform_documents(documents=doc)
        
    return whole_splitted_text
