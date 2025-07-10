import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_embeddings(text: str) -> list[float]:
    response = genai.embed_content(
        model="text-embedding-004",
        content=text,
    )

    embedding = response.get("embedding")
    if not embedding or not isinstance(embedding, list):
        raise RuntimeError("Não foi possível gerar os embeddings corretamente.")

    return embedding