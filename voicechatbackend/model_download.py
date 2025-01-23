from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
model = AutoModelForCausalLM.from_pretrained("HuggingFaceH4/zephyr-7b-beta")

print("running")
tokenizer.save_pretrained("./zephyr-7b-beta")
model.save_pretrained("./zephyr-7b-beta")