import json

data = json.load(open("y.json"))

def get_metadata():
    texts = []
    metadata = []
    for entry in data:
        card_name = entry["card_name"]
        section_type = entry["section_type"]
        details = entry["details"]

        for detail in details:
            if "question" in detail and "answer" in detail:
                text = f"{card_name} - {section_type}: Question: {detail['question']} Answer: {detail['answer']}"
                texts.append(text)
                metadata.append((card_name,section_type,text))
            else:
                if isinstance(detail["value"], list):
                    for nested_detail in detail["value"]:
                        text = f"{card_name} - {section_type}: {detail['type']} - {nested_detail['type']} : {nested_detail['value']}"
                        texts.append(text)
                        metadata.append((card_name, section_type, text))
                else:
                    text = f"{card_name} - {section_type}: {detail['type']} : {detail['value']}"
                    texts.append(text)
                    metadata.append((card_name, section_type, text))
    
    return texts, metadata

texts, metadata = get_metadata()
print(texts[-1])