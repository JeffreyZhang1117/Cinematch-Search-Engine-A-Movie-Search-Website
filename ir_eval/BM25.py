from collections import Counter

from createIndex import *


class BM25:
    def __init__(self, docs):
        self.docs = docs  # List of tokenized documents
        self.doc_num = len(docs)  # Number of documents
        self.vocab = set(word for doc in docs for word in doc)  # Vocabulary of all unique words in documents
        self.avgdl = sum([len(doc) for doc in docs]) / self.doc_num  # Average document length
        self.k1 = 1.5  # Tunable BM25 parameter to control term frequency scaling
        self.b = 0.75  # Tunable BM25 parameter to control document length normalization

    def idf(self, word):
        # Calculate the inverse document frequency (IDF) of a given word
        if word not in self.vocab:
            return 0
        qn = {word: 0 for word in self.vocab}
        for doc in self.docs:
            for w in set(doc):  # Using set to avoid counting duplicate words
                if w in qn:
                    qn[w] += 1
        return np.log((self.doc_num - qn[word] + 0.5) / (qn[word] + 0.5))

    def score(self, word):
        # Calculate the BM25 score for a given word in each document
        score_list = []
        for doc in self.docs:
            word_count = Counter(doc)
            f = word_count[word] / len(doc) if word in word_count else 0
            r_score = (f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))
            score_list.append(self.idf(word) * r_score)
        return score_list

    def score_all(self, sequence):
        # Calculate the BM25 score for all words in the sequence across all documents
        return np.sum([self.score(word) for word in sequence], axis=0)


# Load data
def load_data():
    data = {}
    data_files = [
        ('../pkl_data/plot_dict.pkl', 'plot_dict'),
        ('../pkl_data/plot_token_dict.pkl', 'Plot_token_dict'),
        ('../pkl_data/title_dict.pkl', 'title_dict'),
        ('../pkl_data/Title_token_dict.pkl', 'Title_token_dict'),
        ('../pkl_data/people_dict.pkl', 'people_dict'),
        ('../pkl_data/People_token_dict.pkl', 'People_token_dict'),
        ('../pkl_data/Genre_dict.pkl', 'Genre_dict'),
        ('../pkl_data/Year_dict.pkl', 'Year_dict'),
        ('../pkl_data/dict_score.pkl', 'dict_score'),
    ]

    for file_path, var_name in data_files:
        with open(file_path, 'rb') as f:
            data[var_name] = pickle.load(f, encoding='bytes')

    return data


# Search title
def search_title(query, data):
    try:
        query_tokens = Preprocess(query)
        docs, docs_dict = generate_docs(query_tokens, data['Title_token_dict'], data['title_dict'])

        return process_search_query(query_tokens, docs, docs_dict, data['dict_score'])
    except KeyError:
        return None


# Search year
def search_year(year, data):
    try:
        return rank_items_by_score(data['Year_dict'][year], data['dict_score'])
    except KeyError:
        return None


# Search genre
def search_genre(genre, data):
    try:
        return rank_items_by_score(data['Genre_dict'][genre], data['dict_score'])
    except KeyError:
        return None


# Search celebrity
def search_celebrity(query, data):
    try:
        query_tokens = Preprocess(query)
        docs, docs_dict = generate_docs(query_tokens, data['People_token_dict'], data['people_dict'])

        return process_search_query(query_tokens, docs, docs_dict, data['dict_score'])
    except KeyError:
        return None


# Search plot
def search_plot(query, data):
    try:
        query_tokens = Preprocess(query)
        docs, docs_dict = generate_docs(query_tokens, data['Plot_token_dict'], data['plot_dict'], limit=200)

        return process_search_query(query_tokens, docs, docs_dict, data['dict_score'])
    except KeyError:
        return None


# Generate documents for search
def generate_docs(query_tokens, token_dict, item_dict, limit=None):
    docs = []
    docs_dict = {}
    for token in query_tokens:
        ids = token_dict[token]
        ids = ids[:limit] if limit else ids
        for id in ids:
            item = Preprocess(item_dict[id])
            if item not in docs:
                docs.append(item)
                docs_dict[' '.join(item)] = id

    return docs, docs_dict


# Process search query
def process_search_query(query_tokens, docs, docs_dict, scores):
    bm = BM25(docs)
    score = bm.score_all(query_tokens)
    score_index = {}

    score_max, score_min = max(score), min(score)
    scale = score_max - score_min if score_max != score_min else 1
    score = np.array([(e - score_min) / scale for e in score])

    for i, s in enumerate(score):
        score_index[i] = s + scores[docs_dict[' '.join(docs[i])]]

    score_index = sorted(score_index.items(), key=lambda x: (x[1], x[0]), reverse=True)

    return [docs_dict[' '.join(docs[i[0]])] for i in score_index]


# Rank items by score
def rank_items_by_score(ids, scores):
    try:
        ranked_items = {id: scores[id] for id in ids}
        ranked_items = sorted(ranked_items.items(), key=lambda x: x[1], reverse=True)

        return [item[0] for item in ranked_items]
    except KeyError:
        return None


def search_BM25(query, type):
    data = load_data()
    if type == 'title':
        results = search_title(query, data)
    elif type == 'year':
        results = search_year(query, data)
    elif type == 'genre':
        results = search_genre(query, data)
    elif type == 'celebrity':
        results = search_celebrity(query, data)
    elif type == 'plot':
        results = search_plot(query, data)
    else:
        return None
    return results


# Main
if __name__ == '__main__':
    data = load_data()

    results = search_plot("super hero movie", data)
    count = 0
    for i in results:
        print(data['title_dict'][i])
        count += 1
        if count == 10:
            break
