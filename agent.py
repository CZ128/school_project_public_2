# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "dotenv",
#     "langchain==0.3.27",
#     "langchain-core",
#     "langchain-openai",
#     "langgraph",
#     "langmem",
#     "langsmith",
#     "pydantic",
#     "qdrant_client",
#     "langchain_community",
#     "fastembed",
# ]
# ///
from pydantic import BaseModel, Field
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import RemoveMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import AnyMessage,add_messages
from typing import TypedDict,List,Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langmem import create_memory_searcher

from langchain_core.messages import AIMessage,BaseMessage,HumanMessage
from langsmith import traceable
import uuid
from langmem.short_term import SummarizationNode, RunningSummary,summarize_messages
from materials.qdrant_database import search_qdrant,qdrant_result_conventor_to_list

load_dotenv()
memory =InMemorySaver()

llm = ChatOpenAI(temperature=0,
                    model="gpt-4o-mini",
                    max_tokens=1000
                    )
llm_summary = ChatOpenAI(temperature=0,
                    model="gpt-4o-mini",
                    max_tokens=400
                    ).bind(max_tokens=256)


config = {"configurable":{"thread_id": f"{uuid.uuid4()}"}}

prompt = PromptTemplate.from_template("""
-------------------------------------------------------------------------------------------------------------------------------------
Use ONLY the following context to answer. 
You may see overlapping information in the context. 
Summarize it once, without repeating the same facts multiple times.

Context:
{context}

Question: {message}


last interactions:
{interactions}
""")

prompt_grading = PromptTemplate.from_template("""
You are an evaluator. Compare the paragraph with the query.the paragraf must be overall related but doesn't have to be whole.

Instructions:
- If the paragraph is similar in meaning to the query, output "true".
-Check if the given paragraph connects to the question and identify the contextual link that makes it relevant, output "true".
- If it is not similar, output "false".  
- Do not write anything else. Only output "true" or "false".

Question:{message}

Paragraf:
{paragraf}
""")

class  grading_response(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    grade:List[bool]=Field(
        description="Documents are relevant to the question, 'true' or 'false"
    )
class AgentState(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]
    context:str
    summary:RunningSummary | None


@traceable
def summary_node(state:AgentState)->AgentState:

    summary = state.get("summary","")
    messages = state["messages"]
    
    if len(messages) > 4:
        
        num = len(messages)-2
        
        summarization_result = summarize_messages(  
            messages=state["messages"][:num],
            # IMPORTANT: Pass running summary, if any
            running_summary=summary,  
            token_counter=llm_summary.get_num_tokens_from_messages,
            model=llm_summary, 
            max_tokens=256,  
            max_tokens_before_summary=128,  
            max_summary_tokens=128
    )
        
        print(f"{type(summarization_result.running_summary)}----------------------------------------------ghghnbhkjhmnhkjkjjhjgnbh")
        if summarization_result.running_summary:  
            state["summary"] = summarization_result.running_summary.summary

        # remove the earliest four messages
        state["messages"]=[RemoveMessage(id=m.id) for m in messages[:num]]
    return state
    

@traceable
def qdrant_search_node(state:AgentState)->AgentState:
    latest_human_query = state["messages"][-1]
    context=qdrant_result_conventor_to_list(search_qdrant(query=latest_human_query))
    print(len(context))
    state["context"] = context
    return state
@traceable     
def model(state:AgentState)->AgentState:   
    answer= ""
    latest_query = state["messages"][-1].content
    
    interactions = " ".join([m.content for m in state['messages'][:-1]])+ state.get("summary","")
    
    prompt_text = prompt.format(context= state["context"],message=latest_query,interactions = interactions)
    
    answer= llm.invoke(prompt_text)
    return  {"messages":AIMessage(content=answer.content)}
graph = StateGraph(AgentState) 
graph.add_node("memory_node",summary_node) 
graph.add_node("model",model)
graph.add_node("qdrant",qdrant_search_node)
graph.add_edge(START,"memory_node")
graph.add_edge("memory_node","qdrant")
graph.add_edge("qdrant","model")
graph.add_edge("model",END)

app=graph.compile(checkpointer=memory)
#with open("graph.png","wb") as t :
#        t.write(app.get_graph().draw_mermaid_png())
while True:
        
        message = str(input("You: "))
        print()
        
        if message.lower()=="memory":
           print(app.get_state_history(config)) 
        elif message.lower()=="quit":
                
                responceEnding = "Later, alligator!"
                
                print(responceEnding)
            
                break
        
        elif not message.lower()=="":
            

                
                    
                    response_ai= app.invoke({"messages":message}, config=config)
                    latest_message=response_ai["messages"][-1].content
                    print(latest_message)
                    print(response_ai.get("summary",""))
                    print("\n\n")

                    message=""