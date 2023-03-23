import re

import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.stem import PorterStemmer


class Preprocessor:
    def __init__(self):
        pass

    def tokenisation(self, s):
        return [x for x in re.split('\W', s) if x]

    def case_folding(self, token_list):
        return [x.lower() for x in token_list]

    def normalisation(self, token_list):
        ps = PorterStemmer()
        return [ps.stem(x) for x in token_list]

    def preprocess(self, s):
        token_list = self.tokenisation(s)
        token_list = self.case_folding(token_list)
        token_list = self.normalisation(token_list)
        return token_list


def generate_data():
    data = []
    p = Preprocessor()

    df = pd.read_csv('movies_17w.csv', keep_default_na=False, low_memory=False,
                     dtype={'_id': str, 'Title': str, 'Director': str, 'Actors': str, 'Plot': str, 'Genre': str})

    df['imdbRating'].fillna('0', inplace=True)
    df['imdbVotes'].fillna('0', inplace=True)
    # delete comma in imdbVotes
    df['imdbVotes'] = df['imdbVotes'].apply(lambda x: x.replace(',', ''))
    df['imdbVotes'] = df['imdbVotes'].apply(lambda x: x.replace('N/A', '0'))
    # convert to int
    df['imdbVotes'] = df['imdbVotes'].astype(int)
    df_ = df[df['imdbVotes'] >= 8000]

    for _, l in df_.iterrows():
        content = p.preprocess(' '.join([l['_id'], l['Title'], l['Genre']]))
        data.append(content)

    return data


def write_metadata(data):
    with open('metadata.txt', 'w') as f:
        for line in data:
            f.write(','.join(line) + '\n')


def build_model(data):
    tagged_data = [TaggedDocument(words=d[1:], tags=[d[0]]) for d in data]

    vector_size = 100
    epochs = 50
    min_count = 2
    dm = 1
    window = 5

    model = Doc2Vec(tagged_data,
                    vector_size=vector_size,
                    epochs=epochs,
                    min_count=min_count,
                    dm=dm,
                    window=window)

    return model


def get_similarity(model, movie):
    inferred_vector = model.infer_vector(movie[0])
    similar_movies = model.docvecs.most_similar([inferred_vector], topn=10)

    return similar_movies


data = generate_data()
write_metadata(data)
model = build_model(data)
model.save('similarity_model')
# similar_movies = get_similarity(model, data)

# print(data[0])
# print(similar_movies)
