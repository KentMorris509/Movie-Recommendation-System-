"""
Name: movie_recommendations.py
Date: 11/11/22
Author: Kent Morris 
Description: Predicting movie ratings based on a users rating of other movies using collabartive filtering
"""

from logging import raiseExceptions
import math
import csv
from numpy import average
from scipy.stats import pearsonr


# Created Cutom Exception to handle Bad Input's of Movie ID's and User ID's
class BadInputError(Exception):
    pass


class Movie_Recommendations:
    # Constructor
    def __init__(self, movie_filename, training_ratings_filename):
        """
        Initializes the Movie_Recommendations object from 
        the files containing movie names and training ratings.  
        The following instance variables should be initialized:
        self.movie_dict - A dictionary that maps a movie id to
               a movie objects (objects the class Movie)
        self.user_dict - A dictionary that maps user id's to a 
               a dictionary that maps a movie id to the rating
               that the user gave to the movie.    
        """
        
        self.movie_dict = {}
        self.user_dict = {}
        
        # open and read movies.csv
        f = open(movie_filename)
        f.readline()
        csv_reader = csv.reader(f, delimiter= ',', quotechar = '"')
        
        # open and read training_rating.csv
        f2 = open(training_ratings_filename)
        f2.readline()
        csv_reader2 = csv.reader(f2, delimiter= ',', quotechar = '"')

        ''' Our Comments: In this for loop we iterate over each line of the movies file storing them in our movie_dictionary,
        we then store the movie_id as a key for out movie_dictionary, and value as our Movie object which holds our move_id,
        title, users who have watched the movie (originally empty) and a dictionary of similarites between other movies (originally empty).
        '''
        
        for line in csv_reader:
            movieid = int(line[0])
            movie_title = line[1]

            self.movie_dict[movieid] = Movie(movieid, movie_title)

        ''' Our Comments: In this for loop we iterate over each line of the training_rating_file, adding the userid as our key to a user_dictionary.
        we then add the value as a dictionary within out dictionary which holds the movie_id as a key and the rating the user gave for 
        that movie as the value. While we loop through we then add the users who have seen that movie to our users list that was
        originally empty in our Movie class object. If a user is already in our user_dictionary then they have given a rating and
        we replace their rating with the rating they had before'''

        for line in csv_reader2:
            userid = int(line[0])
            movie_id = int(str(line[1]))
            rating = float(line[2])
            movie = self.movie_dict[movie_id]
            movie.users.append(userid)
            

            if userid not in self.user_dict:
                self.user_dict[userid] = {movie_id:rating}
                
            else:
                self.user_dict[userid][movie_id] = rating

        





    def predict_rating(self, user_id, movie_id):
        """
        Returns the predicted rating that user_id will give to the
        movie whose id is movie_id. 
        If user_id has already rated movie_id, return
        that rating.
        If either user_id or movie_id is not in the database,
        then BadInputError is raised.
        """
        

        ''' Our Comments: Function calculates predicted rating, using the predicted rating formula gone over in class. If the sum of the similarites
         is zero we give it a predicted rating of 2.5 meaning we didn't find any similarited between the movie therefore we give it a average 
         score. If the movie already has a rating we just return that rating and don't predict since its already done'''
    
    
        if user_id not in self.user_dict.keys() or movie_id not in self.movie_dict.keys():
            raise BadInputError
        
        similarity_sum = 0
        rating_sim_product_sum = 0
        if movie_id not in self.user_dict[user_id].keys():
            for movie in self.user_dict[user_id].keys():   
                sim = self.movie_dict[movie_id].get_similarity(movie, self.movie_dict, self.user_dict)
                similarity_sum += sim
                rating = self.user_dict[user_id][movie]
                rating_sim_product = sim * rating
                rating_sim_product_sum += rating_sim_product
            
            if similarity_sum == 0:
                return 2.5
            else:
                predict_rating = rating_sim_product_sum/similarity_sum
                return predict_rating
            
        else:
            return self.user_dict[user_id][movie_id]


        

    def predict_ratings(self, test_ratings_filename):
        """
        Returns a list of tuples, one tuple for each rating in the
        test ratings file.
        The tuple should contain
        (user id, movie title, predicted rating, actual rating)
        """
        
        ''' Our Comments: Created variables to read in this files user_id, movie_id, and actual_rating
         Then to get predicted rating we call our predict_rating function to calculate the predicted rating,
        we pass through the user_id and movie_id that we are reading from test_ratings_file, then return a tuple to a
        list we created as we loop through each line in the file'''
        
        predicted_ratings = []
        f3 = open(test_ratings_filename)
        f3.readline()
        csv_reader3 = csv.reader(f3, delimiter= ',', quotechar = '"')
        for line in csv_reader3:
            userid = int(line[0])
            movieid = int(line[1])
            actual_rating = float(line[2])
            predicted_rating = self.predict_rating(userid,movieid)
            movie_title = self.movie_dict[movieid].title
            
            rating_tuple = (userid,movie_title,predicted_rating,actual_rating)
            predicted_ratings.append(rating_tuple)
        return predicted_ratings
        
       

    def correlation(self, predicted_ratings, actual_ratings):
        """
        Returns the correlation between the values in the list predicted_ratings
        and the list actual_ratings.  The lengths of predicted_ratings and
        actual_ratings must be the same.
        """
        return pearsonr(predicted_ratings, actual_ratings)[0]
        
class Movie: 
    """
    Represents a movie from the movie database.
    """
    def __init__(self, id, title):
        """ 
        Constructor.
        Initializes the following instances variables.  You
        must use exactly the same names for your instance 
        variables.  (For testing purposes.)
        id: the id of the movie
        title: the title of the movie
        users: list of the id's of the users who have
            rated this movie.  Initially, this is
            an empty list, but will be filled in
            as the training ratings file is read.
        similarities: a dictionary where the key is the
            id of another movie, and the value is the similarity
            between the "self" movie and the movie with that id.
            This dictionary is initially empty.  It is filled
            in "on demand", as the file containing test ratings
            is read, and ratings predictions are made.
        """
        
        
        # create instance variables in our object to be changes later

        self.id = id
        self.title = title
        self.users = []
        self.similarities = {}

    def __str__(self):
        """
        Returns string representation of the movie object.
        Handy for debugging.
        """

        
        return str(Movie(self.id, self.title))
        

    def __repr__(self):
        """
        Returns string representation of the movie object.
        """
        return str(Movie(self.id, self.title, self.users, self.similarities))

        

    def get_similarity(self, other_movie_id, movie_dict, user_dict):
        """ 
        Returns the similarity between the movie that 
        called the method (self), and another movie whose
        id is other_movie_id.  (Uses movie_dict and user_dict)
        If the similarity has already been computed, return it.
        If not, compute the similarity (using the compute_similarity
        method), and store it in both
        the "self" movie object, and the other_movie_id movie object.
        Then return that computed similarity.
        If other_movie_id is not valid, raise BadInputError exception.
        """
        
        # Add computed similiarites to both similiarties dictionarys in both movie objects
        # return computed similiarity between two movies, if already computed returs value already stored in similiarties dictionary
        
        if other_movie_id not in movie_dict.keys():
            raise BadInputError
        if other_movie_id in self.similarities.keys():
            return self.similarities[other_movie_id]
        else:
            similarity = self.compute_similarity(other_movie_id,movie_dict,user_dict)
            self.similarities[other_movie_id] = similarity
            movie_dict[other_movie_id].similarities[self.id] = similarity
            return similarity
        
            
        
                
            

        
       

    def compute_similarity(self, other_movie_id, movie_dict, user_dict):
        """ 
        Computes and returns the similarity between the movie that 
        called the method (self), and another movie whose
        id is other_movie_id.  (Uses movie_dict and user_dict)
        """
       
        '''Our Comment: Function uses the similarity formula to compute the similarity between two movies, if the average difference of the movies is 0 meaning
        there was no 2 movies with a rating by the zero we return 0 as the similiarity because there is no similarity.'''
       
        try:
            if other_movie_id not in movie_dict.keys():
                raise BadInputError
            sum = 0
            number_of_comparisons = 0
            for user in self.users:
                if user not in movie_dict[other_movie_id].users:
                    pass
                else:
                    sum += abs(float((user_dict[user][self.id]))- float(user_dict[user][other_movie_id]))
                    number_of_comparisons += 1
            average_difference = sum/number_of_comparisons
            similiarity = 1-(average_difference/4.5)
            return similiarity
        except ZeroDivisionError:
            return 0
                

        
                
                
                
                
                

if __name__ == "__main__":
    # Create movie recommendations object.
    movie_recs = Movie_Recommendations("movies.csv", "training_ratings.csv")

    # Predict ratings for user/movie combinations
    rating_predictions = movie_recs.predict_ratings("test_ratings.csv")
    print("Rating predictions: ")
    for prediction in rating_predictions:
        print(prediction)
    predicted = [rating[2] for rating in rating_predictions]
    actual = [rating[3] for rating in rating_predictions]
    correlation = movie_recs.correlation(predicted, actual)
    print(f"Correlation: {correlation}")    