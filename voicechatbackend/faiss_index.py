import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from metadata import get_metadata

data = json.load(open("y.json"))
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

texts, metadata = get_metadata()

embeddings = embedding_model.encode(texts, convert_to_numpy=True)
faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
faiss_index.add(embeddings)
faiss.write_index(faiss_index, "index.faiss")