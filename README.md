# Overview

`pokebuilder` is an AI-powered application designed to assist users in building effective Pokemon Trading Card Game (TCG) decks. It leverages advanced AI models and a vector database to analyze regulations, card data, and user queries to generate optimized decks.

The application consists of the following components:

- **Crawling Module**: Fetches and processes data from online sources, such as regulations and card details.
- **Vector Database**: Stores embeddings of regulations and card data for efficient similarity searches.
- **MCP Server**: Provides an API interface for generating decks based on user queries.
- **RAG (Retrieval-Augmented Generation)**: Combines retrieved context with user input to generate meaningful prompts for deck building.

## Features

- Crawls Pokemon TCG regulations and card data from specified URLs.
- Stores processed data in a Milvus vector database for fast retrieval.
- Uses AI embeddings to match user queries with relevant data.
- Generates optimized Pokemon TCG decks based on user input and contextual data.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.10+
- A virtual environment tool (e.g., `venv` or `virtualenv`)
- Milvus vector database
- Required Python dependencies (listed in `requirements.txt`)
- Local Ollama installation
- Google Gemini API key

## Installation

1. Clone the repository:

    ```bash
        git clone https://github.com/your-repo/pokebuilder.git
        cd pokebuilder
    ```

2. Create and activate a virtual environment:

    ```bash
        python3 -m venv .venv
        source .venv/bin/activate
    ```

3. Install dependencies

    ```bash
        pip install -r requirements.txt
    ```

### Usage

1. Crawling data
    Run the crawling script to fetch and process regulations and card data:

    ```bash
        python3 src/crawl.py
    ```

    This script will:

    - Crawl URLs listed in crawl/urls/regulations/urls.txt and crawl/urls/tactical_decks/urls.txt.
    - Process the content and store embeddings in the Milvus vector database.

2. Starting the MCP server
    Start the MCP server to handle user queries and generate decks:

    ```bash
        python3 src/mcp_server/py
    ```

    The server will run on the host and port specified in the .env file (default: `http://0.0.0.0:8051`).

3. Querying the server
    For testing purpose run the MCP inspector using following command:

    ```bash
        mcp dev src/mcp_server.py
    ```

    Within the inspector, send a query like:
    > Build a deck with PikachuEX and CharizardEX as the main cards with 2 energy type cards.
    The server will return an optimized deck based on the provided query and contextual data.
