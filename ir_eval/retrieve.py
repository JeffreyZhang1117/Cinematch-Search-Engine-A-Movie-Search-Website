import re
from collections import defaultdict

import numpy as np
from nltk.stem import PorterStemmer


class Preprocessor:
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


class Retrieval:
    def __init__(self, title_index_path, plot_index_path, celeb_index_path, genre_index_path):
        title_inv_dt = self.load_index(title_index_path)
        plot_inv_dt = self.load_index(plot_index_path)
        celeb_inv_dt = self.load_index(celeb_index_path)
        genre_inv_dt = self.load_index(genre_index_path)
        self.inv_dt = {}
        self.inv_dt['title'] = title_inv_dt
        self.inv_dt['plot'] = plot_inv_dt
        self.inv_dt['celeb'] = celeb_inv_dt
        self.inv_dt['genre'] = genre_inv_dt

    def load_index(self, index_path):
        dt = defaultdict(list)
        with open(index_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                term, df = line.strip().split(':')
                for _ in range(int(df)):
                    line = f.readline()
                    docID, idx = line.strip().split(': ')
                    idx = list(map(int, idx.split(',')))
                    dt[term].append((docID, idx))

                line = f.readline()

        return dt

    def term_search(self, query, search_type):
        term = query[0]
        if term not in self.inv_dt[search_type]:
            return set()
        res = set([doc[0] for doc in self.inv_dt[search_type][term]])

        return res

    def phrase_search(self, query, search_type='title'):

        docs1 = self.inv_dt[search_type][query[0]]
        res = set()

        for docID, idx in docs1:
            for i in idx:
                contain = True
                offset = 1
                for term in query[1:]:
                    id_idx = [id_idx for id, id_idx in self.inv_dt[search_type][term] if id == docID]
                    if id_idx and i + offset in id_idx[0]:
                        offset += 1
                    else:
                        contain = False
                        break

                if contain:
                    res.add(docID)
                    break

        return res

    def proximity_search(self, query, search_type='title'):
        dist_after = max(10, 2 * len(query))
        dist_before = dist_after // 2

        docs1 = self.inv_dt[search_type][query[0]]
        res = set()

        for docID, idx in docs1:
            for i in idx:
                contain = True
                for term in query[1:]:
                    id_idx = [id_idx for id, id_idx in self.inv_dt[search_type][term] if id == docID]
                    if id_idx:
                        contain_ = False
                        for pr_id in id_idx[0]:
                            if (pr_id > i and pr_id <= i + dist_after) or (pr_id < i and pr_id >= i - dist_before):
                                contain_ = True
                                break
                        if not contain_:
                            contain = False
                            break
                    else:
                        contain = False

                if contain:
                    res.add(docID)
                    break

        return res

    def search(self, query, search_type):
        p = Preprocessor()
        query = p.preprocess(query)
        # phrase_id = self.phrase_search(query, search_type)
        # proximity_id = self.proximity_search(query, search_type)
        result = self.phrase_search(query, search_type)
        if not result:
            result = self.proximity_search(query, search_type)
        return result

    def ranked_retrieval(self, query, id_list, type='title'):
        res = []

        for id in id_list:
            score = 0
            for term in query:
                tf = [len(idx) for ID, idx in self.inv_dt[type][term] if ID == id]
                if not tf:
                    continue
                tf = tf[0]
                df = len(self.inv_dt[type][term])
                score += (1 + np.log10(tf)) * np.log10(170000 / df)

            res.append((id, score))

        res.sort(key=lambda x: x[1], reverse=True)
        return [id for id, score in res]


if __name__ == '__main__':

    # this_time = time.time()
    onlineIR = Retrieval('index_title.txt', 'index_plot.txt', 'index_celeb.txt', 'index_genre.txt')

    while True:
        query = input('Please input the query: ')
        phrase_id, proximity_id = onlineIR.search(query, 'title')
        print(phrase_id)
        print(proximity_id)
