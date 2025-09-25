# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "dotenv",
#      "qdrant_client",
#      "fastembed",
# ]
# ///
from qdrant_client import QdrantClient,models
from .basicRAGindexing import pdf_loader,splitter_with_metadata
from .saving_and_loading import Loading_Docs
import os
from dotenv import load_dotenv
load_dotenv()
key=os.getenv("QDRANT_API_KEY")
url = os.getenv("QDRANT_URL")
model_name = "BAAI/bge-small-en"
docs=Loading_Docs(".//docs/databaseText.json")

client = QdrantClient( url=url,api_key=key)

def preparation_for_qdrant(split:list):
    page_contents=[]
    ids = []
    metadata_with_docs=[]
    split = splitter_with_metadata(docs)
    
    for i,part in enumerate(split):

        metadata_with_docs.append({"page_content":part.page_content, "metadata":part.metadata})
        page_contents.append(part.page_content)
        ids.append(i)
    return {"ids":ids,"page_contents":page_contents,"metadata_with_docs":metadata_with_docs}

def create_collection(name:str,model_name:str):
    if not client.collection_exists(collection_name=name):
        client.create_collection(collection_name=name,
                        vectors_config=models.VectorParams(
                        size=client.get_embedding_size(model_name), 
                        distance=models.Distance.COSINE
                        ))
def upload_data_qdrant(ids:list,page_contents:list,model_name:str,metadata_with_docs:list):    
    client.upload_collection(
        collection_name="english",
        vectors=[models.Document(text=doc, model=model_name) for doc in page_contents],
        payload=metadata_with_docs,
        ids=ids,
)
def search_qdrant(query:str):  
    print(f"{[query]}")
    search_result = client.query_points(
        collection_name="english",
        query=models.Document(
        text=query.content, 
        model=model_name
    )
    ).points
    return search_result
def qdrant_result_conventor_to_list(input:list):
    result=[]
    for i in input:
        result.append( i.payload["page_content"])
        
    return result
