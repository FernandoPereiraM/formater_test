import json
import hashlib
from deep_translator import GoogleTranslator

# Input and output file paths
input_path = "Prueba_Junior.json"
output_path = "Test_en_full.json"

# Translation map
KEY_TRANSLATION = {
    "id": "id",
    "tipo": "type",
    "texto": "text",
    "actor": "actor",
    "isExpanded": "isExpanded",
    "equipo": "team",
    "herramienta": "tool",
    "interacciones": "interactions"
}

# prefixes
ACTOR_PREFIXES = {
    "Des. Usuario": "USER_RESPONSE",
    "Instrucción": "INSTRUCTION",
    "Salto": "INSTRUCTION"
}

# Google Translator 
translator = GoogleTranslator(source="auto", target="en")

# ID mapping 
id_map = {}

def detect_text_category(text, actor):
    if actor == "Des. Usuario" and text.strip().lower().startswith("el usuario indica"):
        return "DATA_INQUIRY___________"
    return ACTOR_PREFIXES.get(actor, "OTHER__________________")

def generate_new_id(original_id, actor, text):
    if original_id in id_map:
        return id_map[original_id]
    prefix = detect_text_category(text, actor)
    hash_part = hashlib.sha256(original_id.encode()).hexdigest()[:30]
    new_id = (prefix + hash_part)[:50]
    id_map[original_id] = new_id
    return new_id

def translate_string(value):
    try:
        return translator.translate(value)
    except Exception as e:
        print(f"Translation failed for: {value[:30]} → {e}")
        return value

def transform_node(node):
    if isinstance(node, dict):
        new_node = {}
        actor = node.get("actor", "")
        text = node.get("texto", "")
        for key, value in node.items():
            translated_key = KEY_TRANSLATION.get(key, key)
            if key == "id":
                new_node[translated_key] = generate_new_id(value, actor, text)
            elif key == "interacciones":
                new_node[translated_key] = [transform_node(child) for child in value]
            elif isinstance(value, str):
                new_node[translated_key] = translate_string(value)
            else:
                new_node[translated_key] = transform_node(value)
        return new_node
    elif isinstance(node, list):
        return [transform_node(item) for item in node]
    elif isinstance(node, str):
        return translate_string(node)
    else:
        return node

# Load and transform data
with open(input_path, "r", encoding="utf-8") as infile:
    data = json.load(infile)

transformed = transform_node(data)

# Save output
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(transformed, outfile, ensure_ascii=False, indent=2)

print(f"Translated and transformed file saved as: {output_path}")
