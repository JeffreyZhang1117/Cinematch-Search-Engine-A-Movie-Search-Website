from API.db import get_movie_by_oID


class Rank:
    def __init__(self, movie_list, sort_by):
        self.movie_list = movie_list
        self.sort_by = sort_by

    def relevance_rank(self):
        pass

    def popularity_rank(self):
        movie = get_movie_by_oID(self.movie_list)
        print(movie)

    def rating_rank(self):
        pass

    def release_data_rank(self):
        pass

    def rank(self):
        if self.sort_by == 'popularity':
            self.popularity_rank()
