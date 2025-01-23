import faiss

faiss_index = faiss.read_index("index.faiss")

def handle_query_faiss(query, embedding_model, metadata, card_name_filter=None, top_k=3):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    distances, indices = faiss_index.search(query_embedding, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        card_name, section_type, text = metadata[idx]
        if card_name_filter and card_name != card_name_filter:
            continue
        results.append({
            "distance": dist,
            "card_name": card_name,
            "section_type": section_type,
            "text": text
        })
    return results