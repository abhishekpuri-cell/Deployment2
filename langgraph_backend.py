from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import pandas as pd
from langchain_core.tools import Tool
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from typing_extensions import Annotated, TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from IPython.display import Image, display
# from langchain_openai import ChatOpenAI


load_dotenv()

# Fetch API key
api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model='gpt-4o', openai_api_key=api_key)

# Edit code
answer_prompt = SystemMessage(content="""
Based on the conversation and the recent user message, provide an appropriate reply. Response should be concise.
""")

def answer_chain(state):

    return {"messages": [llm.invoke([answer_prompt] + state["messages"])]}


def print_chunk(chunk):
    if "messages" in chunk:
        for msg in chunk["messages"]:
            # msg is a BaseMessage, AIMessage, or HumanMessage
            print(f"{msg.type}: {msg.content}")
    else:
        print(chunk)


builder = StateGraph(MessagesState)
builder.add_node("answer_chain", answer_chain)

builder.add_edge(START, "answer_chain")
builder.add_edge("answer_chain", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "session-1"}, "recursion_limit": 50}





# messages = [HumanMessage(content="what is total sales for enfamel", name='User')]
# messages = [HumanMessage(content="Hi there, my name is Avijit", name='User')]
messages = [HumanMessage(content="what is my name?", name='User')]

arr= []
for chunk in graph.stream({"messages": messages}, config, stream_mode="updates"):
  arr.append(chunk)
  print_chunk(chunk)
  print()
 # End code 

# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# def chat_node(state: ChatState):
#     messages = state['messages']
#     response = llm.invoke(messages)
#     return {"messages": [response]}

# # Checkpointer
# checkpointer = InMemorySaver()

# graph = StateGraph(ChatState)
# graph.add_node("chat_node", chat_node)
# graph.add_edge(START, "chat_node")
# graph.add_edge("chat_node", END)

# chatbot = graph.compile(checkpointer=checkpointer)