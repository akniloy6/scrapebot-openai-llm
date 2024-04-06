import pprint

from ai_extractor import extract
from scrape import ascrape_playwright
from fastapi import FastAPI, Request
import uvicorn
import asyncio




async def scrape_with_playwright(url: str, tags, **kwargs):
    html_content = await ascrape_playwright(url, tags)
    
    print(html_content)

    print("Extracting content with LLM")

    html_content_fits_context_window_llm = html_content[:token_limit]

    extracted_content = extract(**kwargs,
                                content=html_content_fits_context_window_llm)

    pprint.pprint(extracted_content)
    
    return extracted_content

# Scrape and Extract with LLM


app = FastAPI()

@app.post("/extract")
async def extract_data(request: Request):
    data = await request.json()
    url = data.get("url")
    tags = data.get("tags", ["span"])
    schema = data.get("schema")
    #token_limit = data.get("token_limit", 4000)
    
    print(url)
    print(schema)
    print(tags)

    if not url or not schema:
        return {"error": "URL and schema are required"}

    try:
        response = await scrape_with_playwright(
    url=url,
    tags=["span"],
    schema=schema
)

        return response
    except Exception as e:
        print(e)
        return {"error": str(e)}

if __name__ == "__main__":
    token_limit = 10000
    uvicorn.run(app, host="0.0.0.0", port=8000)

