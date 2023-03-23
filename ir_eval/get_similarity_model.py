from gensim.models.doc2vec import Doc2Vec


def load_metadata(file_path):
    metadata = {}
    with open(file_path, 'r') as f:
        for line in f.readlines():
            data = line.strip().split(',')
            metadata[data[0]] = data[1:]

    return metadata


def get_similarity(model, id, metadata):
    movie = metadata[id]
    inferred_vector = model.infer_vector(movie)
    similar_movies_id = model.dv.most_similar([inferred_vector], topn=10)
    # similar_movies = [metadata[id] for id, score in similar_movies_id]

    return similar_movies_id


if __name__ == '__main__':
    metadata = load_metadata('metadata.txt')
    model = Doc2Vec.load('similarity_model')
    similars = get_similarity(model, '64036d080748941800232a79', metadata)
    print(similars)
