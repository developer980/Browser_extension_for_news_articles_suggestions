import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk

nltk.download('maxent_ne_chunker')
nltk.download('words')

text = "GWYNETH PALTROW PARK CITY TRIAL SET TO BEGIN TUESDAY IN DEER VALLEY SKI CRASH CASE"
text1 = "Gwyneth Paltrow crash: Skier's daughter tells court he changed after injury"

stopwords = set(stopwords.words('english'))

text_tokens = word_tokenize(text)
text1_tokens = word_tokenize(text1)

text_keywords = [token.lower() for token in text_tokens if token.lower() not in stopwords]
text1_keywords = [token.lower() for token in text1_tokens if token.lower() not in stopwords]

lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in text_keywords]
lemmatized_tokens1 = [lemmatizer.lemmatize(token) for token in text1_keywords]

filtered_tokens = ne_chunk(nltk.pos_tag(lemmatized_tokens))
filtered_tokens1 = ne_chunk(nltk.pos_tag(lemmatized_tokens1))

print(filtered_tokens)
print(filtered_tokens1)
# print(filtered_tokens1)

entity_list = []

for chunk in filtered_tokens.subtrees():
    if chunk.label() == "PERSON":
        entity_list.append(' '.join(word for word, tag in chunk.leaves()))


entity_list1 = []

for chunk in filtered_tokens1.subtrees():
    if chunk.label() == "PERSON":
        entity_list1.append(' '.join(word for word, tag in chunk.leaves()))


# common_entities = set(entity_list) & set(entity_list1)


print(set(entity_list).intersection(set(entity_list1)))
        