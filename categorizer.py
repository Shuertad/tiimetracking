import numpy as np
from embeddings import get_embedding
from xano import fetch_categories

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def generate_category_embeddings(email, userToken):
    dims = fetch_categories(email, userToken)
    embedded_categories = []

    for dim_name, categories in dims.items():
        if dim_name == "dim0":
            continue
        for cat in categories:
            value = cat["value"]
            embedding = get_embedding(value)

            cat_embedding = {
                "dim": dim_name,
                "id": cat["id"],
                "value": value,
                "embedding": embedding,
            }

            for key in cat:
                if key.endswith("_id") and key != "id":
                    cat_embedding[key] = cat[key]

            embedded_categories.append(cat_embedding)

    return embedded_categories

def suggest_categories(event_title, embedded_categories):
    event_embedding = get_embedding(event_title)
    selected = {}
    parent_ids = {}

    for dim_level in sorted(set(cat["dim"] for cat in embedded_categories),
                            key=lambda x: int(x.replace("dim", ""))):
        candidates = []
        for cat in embedded_categories:
            if cat["dim"] != dim_level:
                continue

            skip = False
            for parent_key, parent_val in parent_ids.items():
                if parent_key in cat:
                    parent_values = cat[parent_key]
                    if isinstance(parent_values, list) and parent_values:
                        if parent_val not in parent_values:
                            skip = True
                            break

            if skip:
                continue

            score = cosine_similarity(event_embedding, cat["embedding"])
            candidates.append((score, cat))

        if candidates:
            best_score, best_cat = max(candidates, key=lambda x: x[0])
            selected[dim_level] = {
                "id": best_cat["id"],
                "value": best_cat["value"],
                "score": best_score
            }
            parent_ids[f"{dim_level}_id"] = best_cat["id"]
        else:
            continue

    return selected
