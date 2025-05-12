import os
import json

from pathlib import Path
from dotenv import load_dotenv
from pymilvus import MilvusClient
from crawl4ai import *
from utils import *
from google.genai import types

# Load environment variables from .env file
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path, override=True)

# Initialize Milvus client
milvus_client = MilvusClient(
    uri=os.getenv("ZILIZ_MILVUS_URI"),
    token=os.getenv("ZILIZ_MILVUS_TOKEN"),
)

# Function to generate system prompt
def system_prompt():
    system_prompt = """
    Human: You are an professional Pokemon TCG player. You are able to build an effective pokemon deck given information from the contextual passage snippets provided.
    """
    return system_prompt

# Function to generate user prompt using context from database
def user_prompt(query):
    # Get the context for regulations
    regulation_prompt = "Cari cara membuat pokemon TCG deck yang efektif"
    regulation_result = milvus_client.search(
        collection_name="regulations",
        data=[emb_ollama(regulation_prompt)],
        limit=15,
        search_params={"metric_type": "COSINE", "params": {}},
        output_fields=["text"],
    )
    regulation_distance = [
        (res["entity"]["text"], res["distance"]) for res in regulation_result[0]
    ]
    regulation_context = "\n".join(
        [line_with_distance[0][0] for line_with_distance in regulation_distance]
    )


    # Get the context for cards selection
    card_result = milvus_client.search(
        collection_name="cards",
        data=[emb_ollama(query)],
        limit=30,
        search_params={"metric_type": "COSINE", "params": {}},
        output_fields=["text"],
    )
    card_distance = [
        (res["entity"]["text"], res["distance"]) for res in card_result[0]
    ]
    card_context = "\n".join(
        [line_with_distance[0] for line_with_distance in card_distance]
    )

    # Generate the user prompt
    user_prompt = f"""
    Use the following pieces of deck building and battle information enclosed in <regulations> tags to build a pokemon deck with a selection of cards enclosed in <> tags using parameters enclosed in <query> tags.
    <regulations>
    {regulation_context}
    </regulations>
    <cards>
    {card_context}
    </cards>
    <query>
    {query}
    </query>
    """

    return user_prompt