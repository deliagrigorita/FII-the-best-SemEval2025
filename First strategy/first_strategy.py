import os
import json
import requests
import re
import time
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import google.generativeai as genai

# Initialize the Gemini API
genai.configure(api_key="*******")

# Load the NER model
tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
model = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")
nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Define paths
source_dir = "data/references/test"
output_dir = "data/predictions/model_name/test"
os.makedirs(output_dir, exist_ok=True)

# Language file mappings
language_files = {
    #"ar": "ar_AE6.jsonl",
    #"de": "de_DE1.jsonl",
    #"es": "es_ES1.jsonl",
    #"fr": "fr_FR3.jsonl",
    #"it": "it_IT1.jsonl",
    "ja": "ja_JP1.jsonl",
    #"ko": "ko_KR1.jsonl",
    #"th": "th_TH1.jsonl",
    #"tr": "tr_TR2.jsonl",
    #"zh": "zh_TW3.jsonl",
}

# Helper: Normalize entity names
def normalize_name(name):
    # Remove spaces around hyphens
    name = re.sub(r'\s*-\s*', '-', name)
    # Remove space before colons
    name = name.replace(" :", ":")
    # Remove spaces around apostrophes
    name = name.replace(" ' ", "'").replace(" 's", "'s")
    # Add space after abbreviations (e.g., St., Dr.)
    name = re.sub(r'\b(St|Dr|Mr|Mrs|Ms|Prof)\.(\w)', r'\1. \2', name)
    # Add space after apostrophe if directly followed by a word
    name = re.sub(r"(?<=')(\w)", r" \1", name)
    # Remove trailing punctuation (?, !, .)
    name = re.sub(r'[?!.]+$', '', name)
    # Collapse multiple spaces into one
    name = re.sub(r'\s+', ' ', name).strip()
    return name

# Helper: Search for entity in Wikidata
def search_entity(name, lang='en'):
    normalized_name = normalize_name(name)
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={normalized_name}&language={lang}&format=json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.text.strip():
            results = response.json()
            if 'search' in results and results['search']:
                return results['search'][0]['id']
        print(f"No search results for '{name}' (normalized as '{normalized_name}') in {lang}.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request to Wikidata failed: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON response from Wikidata for query '{name}'.")
        return None

# Helper: Translate entities
def translate_named_entities(entity_words, target_lang):
    def get_translation(entity_id, lang, original_name):
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={entity_id}&languages={lang}&format=json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['entities'][entity_id]['labels'][lang]['value'] if lang in data['entities'][entity_id]['labels'] else original_name
        except Exception as e:
            print(f"Error fetching translation for {entity_id}: {e}")
            return original_name

    translated_words = []
    for word in entity_words:
        entity_id = search_entity(word)
        if entity_id:
            translation = get_translation(entity_id, target_lang, word)
            translated_words.append(translation)
        else:
            translated_words.append(word)
    return translated_words

# Helper: Replace entities with placeholders
def replace_with_tag_holder(sentence, entity_words):
    for word in entity_words:
        sentence = sentence.replace(word, "[TAG-HOLDER]")
    return sentence

# Helper: Translate sentence with Gemini
def gemini_translate_with_entities(sentence_with_tags, entity_translations, target_lang):
    prompt = (
        f"Translate the following sentence from English into {target_lang} by correctly replacing each occurrence of [TAG-HOLDER] with the corresponding entity translation provided below.\n"
        f"Sentence to translate: {sentence_with_tags}\n"
        f"Entity translations (in order): {entity_translations}\n\n"
        f"Instructions:\n"
        f"1. Replace each [TAG-HOLDER] in the sentence with the corresponding entity translation in the same order as listed.\n"
        f"2. Ensure that no part of the resulting translation contains [TAG-HOLDER]. All placeholders must be replaced.\n"
        f"3. The translation must be a grammatically correct and cohesive sentence in {target_lang}.\n"
        f"4. If an entity translation appears to be ungrammatical or awkward in the target language, adapt it appropriately while preserving its meaning.\n\n"
        f"Return only the final translated sentence, with all [TAG-HOLDER] replacements completed."
    )

    try:
        response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
        if response and hasattr(response, 'text'):
            return response.text
        else:
            print("Gemini returned an empty or invalid response.")
            return "Translation failed."
    except Exception as e:
        print(f"Error during Gemini translation: {e}")
        return "Translation failed."

# Process each language file
for lang, file_name in language_files.items():
    input_path = os.path.join(source_dir, file_name)
    output_path = os.path.join(output_dir, file_name)

    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            source_text = data['source']
            entity_words = [entity['word'] for entity in nlp(source_text)]
            translated_entities = translate_named_entities(entity_words, lang)
            sentence_with_tags = replace_with_tag_holder(source_text, entity_words)

            # Call the Gemini API with a delay to avoid rate limits
            prediction = gemini_translate_with_entities(sentence_with_tags, translated_entities, lang)
            time.sleep(4)  # Add a 4-second delay (adjust based on rate limit)

            # Prepare output
            output = {
                "id": data["id"],
                "source_language": "en",
                "target_language": lang,
                "text": source_text,
                "prediction": prediction,
                "targets": data.get("targets", []),
            }
            outfile.write(json.dumps(output, ensure_ascii=False) + "\n")

    print(f"Finished processing {file_name}")
