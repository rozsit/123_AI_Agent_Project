"""
AI Web Search Agent using GPT-5-Mini + Tavily.
This agent can decide when to perform a web search, fetch real-time info,
and answer with reasoning + citations.
"""

import os
import json
import pathlib
from datetime import datetime, timezone

from openai import OpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables from .env
env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize API clients
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def web_search(query: str, num_results: int = 10):
    """
    Perform a web search using Tavily and return structured results.
    """
    try:
        result = tavily.search(
            query=query,
            search_depth="basic",
            max_results=num_results,
            include_answer=False,
            include_raw_content=False,
            include_images=False
        )

        results = result.get("results", [])

        return {
            "query": query,
            "results": results,
            "sources": [
                {"title": r.get("title", ""), "url": r.get("url", "")}
                for r in results
            ],
        }

    except Exception as e:
        return {
            "error": f"Search error: {e}",
            "query": query,
            "results": [],
            "sources": [],
        }


# Tool schema for function calling
tool_schema = [
    {
        "type": "function",
        "name": "web_search",
        "description": (
            "Execute a web search to fetch up-to-date information. "
            "Extract text and return the best available results, citing 1-3 sources. "
            "If sources conflict, highlight uncertainty and prefer recent evidence."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string"},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    }
]

# Conversation state variables
previous_response_id = None
tool_results = []

print("\nAI Web Search Agent ready. Type 'exit' or 'q' to quit.\n")

# Chat loop
while True:

    # User input unless we have tool results
    if not tool_results:
        user_message = input("User: ")

        if isinstance(user_message, str) and user_message.strip().lower() in {"exit", "q"}:
            print("Exiting chat. Goodbye!")
            break

    else:
        user_message = tool_results.copy()
        tool_results = []

    today_date = datetime.now(timezone.utc).date().isoformat()

    response = client.responses.create(
        model="gpt-5-mini",
        input=user_message,
        instructions=f"Current date is {today_date}.",
        tools=tool_schema,
        previous_response_id=previous_response_id,
        text={"verbosity": "low"},
        reasoning={"effort": "low"},
        store=True,
    )

    previous_response_id = response.id

    # Parse model output
    for output in response.output:

        if output.type == "reasoning":
            print("Assistant (thinking...)")
            for summary in output.summary:
                print(" -", summary)

        elif output.type == "message":
            for item in output.content:
                print("Assistant:", item.text)

        elif output.type == "function_call":
            function_name = globals().get(output.name)
            args = json.loads(output.arguments)
            function_response = function_name(**args)

            tool_results.append(
                {
                    "type": "function_call_output",
                    "call_id": output.call_id,
                    "output": json.dumps(function_response),
                }
            )
