from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from metadata import get_metadata
from identify_card import identify_card_from_query
from qa_pipeline import generate_answer
from sentence_transformers import SentenceTransformer
from accelerate import infer_auto_device_map, load_checkpoint_and_dispatch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

texts, metadata = get_metadata()

model_name='./stabilitylm'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True
)
device_map = infer_auto_device_map(model, max_memory={"cpu":"5GB", "disk":"100GB"})
model = load_checkpoint_and_dispatch(model, model_name, device_map=device_map, offload_folder="offload_dir")
# question_answerer = pipeline("question-answering", model="zephyr-7b-beta")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

class TextInput(BaseModel):
    query: str

@app.post("/generate")
async def handle_user_query(input: TextInput):
    query = input.query
    identified_card, card_names = identify_card_from_query(query)
    top_k=1
    
    if identified_card:
        print(f"Card identified: {identified_card}\nProceeding with your query...")
        answer = generate_answer(query, tokenizer, model, embedding_model, metadata, identified_card, top_k)
        return {"generated_text": answer}
    else:
        card_list = '\n'.join(card_names)
        answer = "Could not identify the card. Please mention the card name along with your query again.\nHere is a list of available card names:\n"+card_list
        return {"generated_text": answer}