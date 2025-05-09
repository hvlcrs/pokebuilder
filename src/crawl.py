import os
import asyncio

from pathlib import Path
from dotenv import load_dotenv
from pymilvus import MilvusClient, DataType
from crawl4ai import *
from tqdm import tqdm
from utils import *

# Load environment variables from .env file
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path, override=True)

# Initialize Milvus client
milvus_client = MilvusClient(
    uri=os.getenv("ZILIZ_MILVUS_URI"),
    token=os.getenv("ZILIZ_MILVUS_TOKEN"),
)

# Function to crawl a webpage and extract its content
async def crawl(path):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=path,
        )
        return result.markdown

# Function to split the markdown content into sections
def split_markdown_content(content):
    return [section.strip() for section in content.split("# ") if section.strip()]

# Function to create a collection in Milvus
def create_collection(collection_name):
    # Create a schema for the collection
    schema = milvus_client.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR,dim=768) #3072 for gemini, 1536 for openai, 768 for ollama

    index_params = milvus_client.prepare_index_params()
    index_params.add_index(
        field_name="id",
        index_type="AUTOINDEX"
    )

    index_params.add_index(
        field_name="vector", 
        index_type="AUTOINDEX",
        metric_type="COSINE"
    )

    # Create a collection in Milvus if it doesn't exist
    if not milvus_client.has_collection(collection_name):
        milvus_client.create_collection(
            collection_name=collection_name,
            consistency_level="Strong",
            schema=schema,
            index_params=index_params,
        )

# Function to insert data into the collection in Milvus
def insert_data(sections, collection_name):
    data = []

    for i, section in enumerate(tqdm(sections, desc="Processing sections")):
        embedding = emb_ollama(section)
        data.append({"id": i, "vector": embedding, "text": section})

    # Insert data into the collection
    milvus_client.insert(
        collection_name=collection_name,
        data=data,
    )

# Function to insert data into the collection in Milvus without chunking
def insert_data_unchunked(sections, collection_name):
    milvus_client.insert(
        collection_name=collection_name,
        data=[{"vector": emb_ollama(sections), "text": sections}],
    )
    

async def main():
    # Create a collection for the markdown content
    create_collection("regulations")
    create_collection("cards")

    # Crawl the regulations
    regulations = open(project_root.joinpath("crawls/urls/regulations/urls.txt"), "r")
    for line in regulations:
        markdown_content = await crawl(line)
        sections = split_markdown_content(markdown_content)
        insert_data_unchunked(sections, "regulations")

    # Crawl the tactical decks
    tactical_decks = open(project_root.joinpath("crawls/urls/tactical_decks/urls.txt"), "r")
    for line in tactical_decks:
        markdown_content = await crawl(line)
        insert_data_unchunked(markdown_content, "cards")
    
if __name__ == "__main__":
    asyncio.run(main())