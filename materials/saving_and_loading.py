# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langchain-core",
# ]
# ///
import shutil
import json
from langchain_core.load import dumpd, dumps, load, loads
import os

def Saving_lists(IDs:list,url:str):
    
    with open(url,"w",encoding="utf-8") as u:
        json.dump(IDs,u, ensure_ascii=False, indent=2)
        
def Saving_Docs(url:str,database=[]):
    
    with open(url,"w",encoding="utf-8") as t:
        for i in range ( len(database)):
           database[i]=dumpd(database[i])
            
        json.dump(database,t, ensure_ascii=False, indent=2)   
        
def Loading_lists(url:str):
    with open(url,"r",encoding="utf-8") as u:
       doc_ids= json.load(u)
    return doc_ids

def Loading_Docs(url:str):
    with open(url,"r",encoding="utf-8") as t:
        database = json.load(t)
        for i in range(len(database)):
            
            database[i] = load(database[i])
    return database

def file_delete(url:str):
    if os.path.exists(url):
        shutil.rmtree(url)
        print("File deleted successfully.")
    else:
        print("File does not exist.")   
                      