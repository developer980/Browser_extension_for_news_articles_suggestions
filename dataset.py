import pandas as pd
import os
from nltk import word_tokenize, pos_tag, FreqDist
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))

folder_path = "./reuters/reuters/training"
folder = os.listdir(folder_path)

# data = pd.read_csv('1', delimiter = ",")

# print(data)

# my_text_data = ''
# my_intersection = []

data = []
most_frequent_nouns = []

for file in folder:
    file_path = os.path.join(folder_path, file)

    with open(file_path, 'r') as res:
        text_data = res.read()
        text_data_tokens = text_data.lower().split()
        filtered_data_tokens = [token for token in text_data_tokens if token not in stopwords]

        data.append(filtered_data_tokens)

        # if len(my_intersection) == 0 :
        #     my_intersection = filtered_data_tokens

        # else: 
        #     my_intersection = set(my_intersection).intersection(set(filtered_data_tokens))
        #     print(my_intersection)

        pos_tags = pos_tag(text_data_tokens)

        # print(pos_tags)
        noun_freq = FreqDist(word.lower() for word, pos in pos_tags if pos.startswith('N'))
        frequent_nouns = [noun for noun in noun_freq.most_common(2)]

        for noun in frequent_nouns:
            if noun not in most_frequent_nouns:
                most_frequent_nouns.append(noun)

topic = ''.join(str(most_frequent_nouns))

        # my_data_tokens = word_tokenize(my_text_data)

print(topic)
