# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langchain-text-splitters",
#     "langchain_langchain_community",
# ]
# ///
import asyncio
from langchain_community.document_loaders import PyPDFLoader
import os
def loadDatabase(path_name:str, disabled_names=[],allowed_names=[])-> dir:
    
    def prepare_names(path_name:str,disabled_names=[],allowed_names=[])->list:
        
        files =os.listdir(path_name)
        if not disabled_names and not allowed_names:
            
            for i in range(len(files)):
                if i == len(files):
                    return files
                    
                if not os.path.isfile(f"{path_name}/{files[i]}"):
                        print(files[i])
                        del files[i]
                        
        if disabled_names and not allowed_names:
            
            for i in range(len(files)):
                
                if i == len(files):
                    return files
                    
                if not os.path.isfile(f"{path_name}/{files[i]}"):
                        
                        del files[i]
                elif i in disabled_names:
                        del files[i]
                        
        if not disabled_names and allowed_names:
            
            for i in range(len(files)):
                
                if i == len(files):
                    return files
                    
                if not os.path.isfile(f"{path_name}/{files[i]}"):
                        
                        del files[i]
                        
                elif i not in allowed_names:
                        del files[i]
                        
        if disabled_names and allowed_names:
            
            raise Exception("this is not allowed")
                        
        return files
    
    async def load_PDFs_Database(file_names:list,path_name:str)->dir:
        loader_database =[]
        pages = []
        for i in range(len(file_names)):
                
                loader = PyPDFLoader(f"{path_name}/{file_names[i]}")

                async for page in loader.alazy_load():
                        page.metadata["document"] = file_names[i].replace(".pdf","")
                        pages.append(page)
                        
                        
                loader_database+= pages
                pages=[]
        return loader_database
    
    def replace(text,replace_first_position:str,replace_second_position:str )-> dir:
        
        for u in range(len(text)):
           text[u].page_content= text[u].page_content.replace(replace_first_position,replace_second_position)
        return text
    
    
    
    file_names=prepare_names(path_name=path_name)
    
    print(file_names)
    
    full_database=asyncio.run(load_PDFs_Database(file_names=file_names,path_name=path_name))
    
    replaced_database=replace(text=full_database,
                              replace_first_position="""WWW.ANGLICKYZAROK.CZ – individuální výuka angličtiny pro začátečníky i pokročilé, kurzy do 
zaměstnání, přípravné kurzy na maturitu a certifikáty. anglickyzarok@gmail.com""",
                              replace_second_position=""
                              )
    replaced_database=replace(text=full_database,
                              replace_first_position="""WWW.ANGLICKYZAROK.CZ – individuální výuka angličtiny pro začátečníky i pokročilé, 
kurzy do zaměstnání, přípravné kurzy na maturitu a certifikáty. anglickyzarok@gmail.com""",
                              replace_second_position=""
                              )
    
    return replaced_database
def DocumentConventor_multiple_indexing(documents=[])->str:
    stringDocument=""
    if documents:
        for document in documents:
            stringDocument+=document.page_content
    return stringDocument

def DocumentConventor_ColBERT(documents):
    if documents:
        for i in range (len(documents)):
            documents[i] = documents[i].page_content
    return  documents

