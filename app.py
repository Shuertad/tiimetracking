from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
from embeddings import get_embedding
from xano import fetch_categories
from categorizer import suggest_categories, generate_category_embeddings

app = FastAPI()

class EventInput(BaseModel):
    title: str
    email: str
    userToken: str

@app.post("/suggest")
def suggest(event: EventInput):
    try:
        embedded_categories = generate_category_embeddings(event.email, event.userToken)
        suggestions = suggest_categories(event.title, embedded_categories)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
