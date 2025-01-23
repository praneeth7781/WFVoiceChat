from rag import handle_query_faiss

def generate_answer(query, tokenizer, model, embedding_model, metadata, identified_card=None, top_k=3):
  retrieved_contexts = handle_query_faiss(query, embedding_model, metadata, identified_card, top_k)
  context_texts = [context["text"] for context in retrieved_contexts]
  question = f"Answer the following question, by extracting the relevant answer from the context provided. Do not use any other knowledge. Keep the answer concise. \n\n Question: {query} \n\n Context: {' '.join(context_texts)} \n\n Answer:"
  # answer = pipe(question=query, context=' '.join(context_texts))['answer']
  prompt = [{"role": "user", "content": question}]
  inputs = tokenizer.apply_chat_template(
      prompt,
      add_generation_prompt=True,
      return_tensors='pt'
  )
  tokens = model.generate(
      inputs.to(model.device),
      max_new_tokens=1024,
      temperature=0.5,
      do_sample=True
  )
  outputs = tokenizer.decode(tokens[0], skip_special_tokens=False)

  answer = outputs.split('<|assistant|>')[1].split('<|endoftext|')[0].strip()

  return answer