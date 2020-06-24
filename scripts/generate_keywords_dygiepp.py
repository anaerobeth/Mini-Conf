import jsonlines
import csv

def to_csv(keywords):
    columns = ["UID", "generated_keywords"]
    keyword_file = "generated_keywords_dygie_full_model.csv"
    try:
        with open(keyword_file, "w") as f:
           writer = csv.DictWriter(f, fieldnames=columns)
           writer.writeheader()
           for keyword in keywords:
               writer.writerow(keyword)
    except IOError:
        print("I/O error")

# Load predictions from DyGIE++ created from preproccessed abstracts using the pretrained SciERC full model 
with jsonlines.open('predictions/miniconf_full_keywords.jsonl') as f:
    all_keywords = []
    for line in f.iter():
        tokens = [item for sublist in  line['sentences'] for item in sublist]
        ner = line['predicted_ner']
        id = line['doc_key']

        phrase = {}
        for entities in ner:
            for entity in entities:
                entity_type = entity.pop()
                if entity_type not in phrase:
                    phrase[entity_type] = []
                if len(set(entity)) == 1:
                    words = tokens[entity[0]]
                else:
                    words = ' '.join([tokens[item] for item in entity])
                if words not in phrase[entity_type]:
                    phrase[entity_type].append(words)

        all_keywords.append({ id: phrase })

    top_keywords = []
    for keywords in all_keywords:
        for k, v in keywords.items():
            # Choose the top 5 keywords for each abstract
            ordered_keywords = (
                (v['Task'] if 'Task' in v else []) +
                (v['Method'] if 'Method' in v else []) +
                (v['OtherScientificTerm'] if 'OtherScientificTerm' in v else []) +
                (v['Metric'] if 'Metric' in v else []) +
                (v['Material'] if 'Material' in v else []) +
                (v['Generic'] if 'Generic' in v else [])
            )
            top_keywords.append({
                'UID': k,
                'generated_keywords': '|'.join(ordered_keywords[:4])
            })

    to_csv(top_keywords)
