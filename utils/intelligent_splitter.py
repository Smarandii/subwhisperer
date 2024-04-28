import spacy
nlp = spacy.load("ru_core_news_sm")


def intelligent_split(text, max_length):
    doc = nlp(text)
    sentences = list(doc.sents)
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence.text) <= max_length:
            current_chunk += sentence.text + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence.text + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# Usage example
text = "В случае с ретродроп-проектами основными ролями являются разработчик блокчейна, веб-разработчики, аудиторы смарт-контрактов, специалисты по безопасности, ну и там остальные."
chunks = intelligent_split(text, 76)  # Assuming 76 is your maximum line length
for chunk in chunks:
    print(chunk)
