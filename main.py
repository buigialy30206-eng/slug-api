"""
Text to Slug API
Convert text to URL-friendly slugs. Pure Python, zero deps.
"""

import re, unicodedata

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Text to Slug API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class SlugResult(BaseModel):
    original: str
    slug: str
    length: int

def text_to_slug(text: str, separator: str = "-") -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", separator, text)
    return text

@app.get("/")
async def root():
    return {"service": "Text to Slug API", "version": "1.0.0"}

@app.get("/slugify", response_model=SlugResult)
async def slugify(
    text: str = Query(..., description="Text to convert to slug"),
    separator: str = Query("-", description="Word separator, default '-'"),
):
    slug = text_to_slug(text, separator)
    return SlugResult(original=text, slug=slug, length=len(slug))
