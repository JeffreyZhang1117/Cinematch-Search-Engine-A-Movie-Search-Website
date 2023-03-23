import re
from collections import defaultdict

import pandas as pd
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


def get_dict(type):
    dt = {}
    p = Preprocessor()

    df = pd.read_csv('movies_17w.csv', keep_default_na=False, low_memory=False,
                     dtype={'_id': str, 'Title': str, 'Director': str, 'Actors': str, 'Plot': str, 'Genre': str})

    df['imdbRating'].fillna('0', inplace=True)
    df['imdbVotes'].fillna('0', inplace=True)

    for _, l in df.iterrows():
        if type == 'title':
            content = p.preprocess(l['Title'])
        elif type == 'celeb':
            content = p.preprocess(' '.join([l['Director'], l['Actors']]))
        elif type == 'plot':
            content = p.preprocess(' '.join([l['Title'], l['Plot']]))
        elif type == 'genre':
            content = p.preprocess(l['Genre'])
        else:
            raise NotImplementedError
        # title = l['Title']
        # plot = l['Plot']
        # content = (title + ' ') * 5 + plot
        # content = p.preprocess(l[type])

        dt[l['_id']] = content

    return dt


def get_inverted_dict(dt):
    inv_dt = defaultdict(list)
    for docID, content in dt.items():
        for idx, term in enumerate(content):
            if inv_dt[term] and inv_dt[term][-1][0] == docID:
                inv_dt[term][-1][1].append(idx)
            else:
                inv_dt[term].append((docID, [idx]))

    return inv_dt


def write_index(inv_dt, type):
    dt = sorted(inv_dt.items(), key=lambda d: d[0])
    with open('index_{}.txt'.format(type), 'w', encoding='utf-8') as f:
        for term, doc_list in dt:
            df = len(doc_list)
            f.write('{}:{}\n'.format(term, df))

            for docID, idx_list in doc_list:
                idx = ','.join(map(str, idx_list))
                f.write('\t{}: {}\n'.format(str(docID), idx))


types = ['title', 'celeb', 'plot', 'genre']
for type in types:
    dt = get_dict(type)
    # print(dt)

    inv_dt = get_inverted_dict(dt)
    write_index(inv_dt, type)
