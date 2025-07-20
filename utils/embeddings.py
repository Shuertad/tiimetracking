import openai
from utils.fetch import fetch_categories

openai.api_key = "OPENAI_API_KEY" 

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def generate_category_embeddings(email, user_token):
    dims = fetch_categories(email, user_token)
    embedded_categories = []

    for dim_name, categories in dims.items():
        if dim_name == "dim0":
            continue
        for cat in categories:
            embedding = get_embedding(cat["value"])
            entry = {
                "dim": dim_name,
                "id": cat["id"],
                "value": cat["value"],
                "embedding": embedding
            }
            for key in cat:
                if key.endswith("_id") and key != "id":
                    entry[key] = cat[key]
            embedded_categories.append(entry)
    return embedded_categories
