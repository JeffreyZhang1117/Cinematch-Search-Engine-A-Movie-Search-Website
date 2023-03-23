from flask import Blueprint, request, jsonify
from API.db import get_movie_by_imdbID, get_movies, get_movie_by_ID, get_movies_by_oid
# from flask_cors import CORS
# from ir_eval.BM25 import *
from ir_eval.spellcorrect_new import *
from bson.objectid import ObjectId
from ir_eval.retrieve import *
from ir_eval.get_similarity_model import *

movies_api = Blueprint('movies_api', __name__, url_prefix='/api/movies')
IR = Retrieval('ir_eval/index_title.txt', 'ir_eval/index_plot.txt', 'ir_eval/index_celeb.txt',
               'ir_eval/index_genre.txt')
metadata = load_metadata('ir_eval/metadata.txt')
similarity_model = Doc2Vec.load('ir_eval/similarity_model')

"""
In a production environment, you should only allow cross-origin requests from the 
domain where the front-end application is hosted. 
Refer to the Flask-CORS documentation for more info on this
"""
# CORS(movies_api)

# get all movies on the home page
DEFAULT_MOVIES_PER_PAGE = 20


@movies_api.route('/', methods=['GET'])
def api_get_movies():
    page = int(request.args.get('page', 1))
    print(page)
    movies, total_number = get_movies(
        None, page=page, movies_per_page=DEFAULT_MOVIES_PER_PAGE)
    response = {
        "movies": movies,
        'total_number': total_number,
        'current_page': page
    }
    return jsonify(response), 200


# basic search function
@movies_api.route('/search', methods=['GET'])
def api_search_movie():
    filters = {}
    page = int(request.args.get('page', 1))
    # all = request.args.get('All')
    title = request.args.get('Title')
    celeb = request.args.get('Celebrity')
    genre = request.args.get('Genre')
    # year = request.args.get('Year')
    plot = request.args.get('Plot')
    sort = request.args.get('sort')
    # if all:
    #     filters['all'] = all
    if title:
        filters['title'] = title
    elif celeb:
        filters['celeb'] = celeb
    elif genre:
        filters['genre'] = genre
    # elif year:
    #     filters['year'] = year
    elif plot:
        filters['plot'] = plot
    print(filters)
    oid_list = get_oid_from_BM25(filters)

    # sort_by includes 'popularity', 'rating', 'release_date', 'relevance'
    sort_by = sort
    if oid_list:
        # if all:
        #     movies = {}
        #     for category, oid_list in oid_list.items():
        #         if oid_list:
        #             movies[category] = get_movies_by_oid(
        #                 oid_list, page, DEFAULT_MOVIES_PER_PAGE, sortBy=sort_by)[0]
        #         else:
        #             movies[category] = None
        #     response = {
        #         "movies": movies,
        #         "response": 'success'
        #     }
        # else:
        print(len(oid_list))
        movies, total_number = get_movies_by_oid(
            oid_list, page, DEFAULT_MOVIES_PER_PAGE, sortBy=sort_by)
        response = {
            "movies": movies,
            "total_number": total_number,
            "current_page": page,
            "response": 'success'
        }
    else:
        response = {
            "response": 'fail'
        }
    return jsonify(response), 200


# get movie by ID
@movies_api.route('/id/<id>', methods=['GET'])
def api_get_movie_by_id(id):
    movie = get_movie_by_imdbID(id)
    if movie is None:
        return jsonify({
            "error": "Not found"
        }), 400
    elif movie == {}:
        return jsonify({
            "error": "uncaught general exception"
        }), 400
    else:
        return jsonify(
            {
                "movie": movie,
                "response": 'success'
            }
        ), 200


# get movie by _ID
@movies_api.route('/_id/<id>', methods=['GET'])
def api_get_movie_by_dbId(id):
    movie = get_movie_by_ID(id)
    if movie is None:
        return jsonify({
            "error": "Not found"
        }), 400
    elif movie == {}:
        return jsonify({
            "error": "uncaught general exception"
        }), 400
    else:
        return jsonify(
            {
                "movie": movie,
                "response": 'success'
            }
        ), 200


def get_oid_from_BM25(filters):
    print("Searching")
    oid_list = None
    # if 'all' in filters:
    #     title_result = IR.search(filters['title'], 'title')
    #     celebrity_result = IR.search(filters['celeb'], 'celeb')
    #     year_result = None
    #     genre_result = IR.search(filters['genre'], 'genre')
    #     return {'title': title_result[:3] if title_result else None,
    #             'celebrity': celebrity_result[:3] if celebrity_result else None,
    #             'year': year_result[:3] if year_result else None,
    #             'genre': genre_result[:3] if genre_result else None}
    if 'title' in filters:
        # oid_list = search_title(filters['title'])
        oid_list = IR.search(filters['title'], 'title')
        oid_list = IR.ranked_retrieval(filters['title'], oid_list, 'title')
    elif 'celeb' in filters:
        oid_list = IR.search(filters['celeb'], 'celeb')
        oid_list = IR.ranked_retrieval(filters['celeb'], oid_list, 'celeb')
    elif 'genre' in filters:
        oid_list = IR.search(filters['genre'], 'genre')
        oid_list = IR.ranked_retrieval(filters['genre'], oid_list, 'genre')
    elif 'plot' in filters:
        oid_list = IR.search(filters['plot'], 'plot')
        oid_list = IR.ranked_retrieval(filters['plot'], oid_list, 'plot')

    return oid_list


@movies_api.route('/check', methods=['GET'])
def api_spell_check():
    id = request.args.get('_id')
    if len(input) > 0:
        promp_list = [' '.join(tuple) for tuple in spellchecker(input)]
        print(f"check {input} -> {promp_list}")
        if promp_list:
            if len(promp_list) > 8:
                promp = promp_list[:8]
            else:
                promp = promp_list
            return jsonify(
                {
                    "promp": promp,
                    "response": "success"
                }
            )
        return jsonify(
            {
                "response": "fail"
            }
        )
    else:
        return jsonify({
            "response": 'empty input'
        })


# 获取相关电影
@movies_api.route('/relation', methods=['GET'])
def api_spell_relation():
    id = request.args.get('id')
    if id:
        movies = get_similarity(similarity_model, id, metadata)
        response = {
            "movies": movies[1:6],
            "total_number": 5,
            "response": 'success'
        }
    else:
        response = {
            "response": 'fail'
        }
    return jsonify(response), 200


# search promp function (discarded)
# @movies_api.route('/promp', methods=['GET'])
# def api_input_prompt():
#     input = request.args.get('input')
#     print(input)
#     oid = {'title': '62235b3999820f460dbdd37e', 'genre': '62235b3999820f460dbdd37e',
#            'year': '62235b3999820f460dbdd37e', 'celeb': '62235b3999820f460dbdd37e'}
#     output = {}
#     for category, oid in oid.items():
#         output[category] = get_movies_by_oid([oid], 1, 1)[0]
#     if output:
#         response = {
#             "prompt": output,
#             "response": 'success'
#         }
#     else:
#         response = {
#             "response": 'fail'
#         }
#     return jsonify(response), 200
if __name__ == '__main__':
    pass
