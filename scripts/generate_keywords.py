import csv
import spacy
import textacy.ke
from collections import Counter

nlp = spacy.load("en_core_web_sm")
keywords = []

def generate_keywords():
    """Identify keywords from text in paper title and abstract
    """
    with open("../sitedata/papers.csv", "r") as f:
        data = csv.DictReader(f)
        for row in data:
            text = f'{row["title"]}\n{row["abstract"]}'
            top_phrases = collect_phrases(nlp(text))
            keywords.append({
                "UID": row["UID"],
                "generated_keywords": top_phrases
            })

    to_csv(keywords)


def collect_phrases(doc):
    """Use Textacy keyword extraction
    Algorithms: textrank, yake, scake
    Ref: https://chartbeat-labs.github.io/textacy/build/html/api_reference/information_extraction.html
    """
    scake = [tuple[0] for tuple in textacy.ke.scake(doc, topn=10)]
    textrank =  [tuple[0] for tuple in textacy.ke.textrank(doc, topn=10)]
    yake =  [tuple[0] for tuple in textacy.ke.yake(doc, topn=10)]
    counts = Counter(scake + textrank + yake)
    # Keep phrases identified by at least one algorithm and 
    # exclude single words unless acronyms or hyphenated
    filtered_phrases = [k for k, v in counts.items() if v > 1 and (' ' in k or '-' in k or k.isupper())]

    phrases = "|".join(filtered_phrases[:4])

    return phrases

def to_csv(keywords):
    columns = ["UID", "generated_keywords"]
    # For now, append algorithm used to the filename
    keyword_file = "../sitedata/generated_keywords_filtered.csv"
    try:
        with open(keyword_file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for keyword in keywords:
                writer.writerow(keyword)
    except IOError:
        print("I/O error")


if __name__ == "__main__":
    generate_keywords()
