import csv
import spacy
import textacy.ke

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
    For now, limits results to 5 for each paper
    Algorithms: textrank, yake, scake
    Ref: https://chartbeat-labs.github.io/textacy/build/html/api_reference/information_extraction.html
    """
    tuples = textacy.ke.scake(doc, topn=10)
    phrases = "|".join([tuple[0] for tuple in tuples[:4]])

    return phrases

def to_csv(keywords):
    columns = ["UID", "generated_keywords"]
    # For now, append algorithm used to the filename
    keyword_file = "../sitedata/generated_keywords_scake.csv"
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
