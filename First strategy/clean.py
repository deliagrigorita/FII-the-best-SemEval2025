import json
import re

def clean_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Load the JSON object
            data = json.loads(line)
            
            # Remove the 'targets' key entirely
            if 'targets' in data:
                del data['targets']  # Removes the 'targets' key entirely

            # Remove any brackets around text unless the text is 'TAG-HOLDER'
            if 'prediction' in data:
                text = data['prediction']
                # Regular expression to remove brackets unless they are around 'TAG-HOLDER'
                text = re.sub(r'\[(?!TAG-HOLDER)(.*?)\]', r'\1', text)
                data['prediction'] = text
            
            # Write the cleaned line back to the output file
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

# Example usage
clean_jsonl('data/predictions/model_name/test/zh_TW.jsonl', 'cleaned_zh_TW.jsonl')