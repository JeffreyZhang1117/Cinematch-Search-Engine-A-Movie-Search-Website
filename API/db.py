from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
from werkzeug.local import LocalProxy

import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

db = None


def get_db():
    # add database url
    url = "mongodb+srv://jeffreyzhang:20230317@ttds.t2wpupf.mongodb.net/testt"
    client = MongoClient(url)
    db = client.sample_movies
    return db


db = LocalProxy(get_db)


def build_query_sort_project(filters):
    query = {}
    sort = [("imdbRating", DESCENDING), ("_id", ASCENDING)]
    project = None
    # print(filters)
    if filters:
        if "title" in filters:
            query = {"$text": {"$search": filters["title"]}}
            meta_score = {"$meta": "textScore"}
            sort = [("score", meta_score)]
            project = {"score": meta_score}
        elif "cast" in filters:
            query = {"Cast": {"$in": filters["cast"]}}
        elif "genre" in filters:
            query = {"Genre": {"$in": filters['genre']}}

    return query, sort, project


def get_movies(filters, page, movies_per_page):
    query, sort, project = build_query_sort_project(filters)
    print(query, sort, project)
    if project:
        cursor = db.movies2.find(query, project).sort(sort)
    else:
        cursor = db.movies2.find(query).sort(sort)
    total_num_movies = 0
    if page == 0:
        total_num_movies = db.movies2.count_documents(query)
    movies = cursor.skip(page*movies_per_page).limit(movies_per_page)
    print(f"total number: {total_num_movies}")
    return list(movies), total_num_movies


def get_movie_by_imdbID(id):
    try:
        query = {"imdbID": id}
        movie = db.movies2.find_one(query)
        return movie
    except Exception as e:
        return {}


def get_movie_by_ID(id):
    try:
        query = {"_id": ObjectId(id)}
        movie = db.movies2.find_one(query)
        return movie
    except Exception as e:
        return {}


def get_movies_by_oid(oid_list, page, movies_per_page, sortBy):
    oid_list_ = [ObjectId(i) for i in oid_list]
    query = {'_id': {'$in': oid_list_}}
    cursor = db.movies2.find(query)
    if sortBy == 'popularity':
        cursor = cursor.sort('imdbVotes', -1)
    elif sortBy == 'rating':
        cursor = cursor.sort('imdbRating', -1)
    elif sortBy == 'release_date':
        cursor = cursor.sort('Year', -1)
    # elif sortBy == 'relevance':
    #     pass
    total_num_movies = 0
    if page == 1:
        total_num_movies = db.movies2.count_documents(query)
    movies = cursor.skip((page-1)*movies_per_page).limit(movies_per_page)

    return list(movies), total_num_movies

