# File: test_psa4A.py
# Author: John Glick    
# Date: March 6, 2020
# Description: Program that tests the correctness
#              of comp 120, psa4,
#              on a small dummy set of ratings.

import sys

# import the module containing psa4 solution
import movie_recommendations

class IncorrectCode(Exception):
    pass

def test_psa4():
    # Do tests with the dummy files.

    # Create movie recommendation object using dummy movies and ratings.
    mr = movie_recommendations.Movie_Recommendations(
        "dummy_movies.csv", "dummy_training_ratings.csv")

    # Initialize test count
    num_correct = 0
    num_tested = 0

    users = ({}, {1, 4}, {1, 2, 3}, {1, 2, 4, 5}, {1, 2, 3, 4, 5}, {1, 4})
    ratings = ({}, {1:5, 2:3, 3:1, 4:2, 5:3},
                {2:5, 3:0, 4:4},
                {2:0, 4:4},
                {1:0, 3:4, 4:3, 5:0},
                {3:5, 4:5})

    similarities = ((), (0, 1, 0.56,0.11,0.33,0.78),
                    (0, 0.56,1, 0.22,0.56,1.00),
                    (0, 0.11,0.22,1, 0.67,0.33),
                    (0, 0.33,0.56,0.67,1,0.56),
                    (0, 0.78,1.00,0.33,0.56, 1))

    # Test movie_dict of Movie_Recommendations constructor
    try:
        num_tested += 1
        print("Testing movie_dict of Movie_Recommendation constructor.")
        
        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        md = mr.movie_dict
        if set(range(1, 6)) != set(md):
            raise IncorrectCode(f"set of movie ids incorrect.  Should be {set(range(1, 6))}")
        for i in range(1, 6):
            if md[i].title != "M" + str(i):
                raise IncorrectCode(f"movie id {i} should have title M{i}")
            if md[i].id != i:
                raise IncorrectCode(f"movie id {i} should have id {i}")
            if set(md[i].users) != users[i]:
                raise IncorrectCode(f"movie id {i} should have users {users[i]}")
            if md[i].similarities != {}:
                raise IncorrectCode(f"movie id {i} should have similarities {'{}'}")   
        print("  passed")
        num_correct += 1
    except IncorrectCode as e:
        print(f"  failed. {e}")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")

    # Test user_dict of Movie_Recommendations constructor
    try:
        num_tested += 1
        print("Testing user_dict of Movie_Recommendation constructor.")

        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        if set(range(1, 6)) != set(ud):
            raise IncorrectCode(f"set of user ids incorrect.  Should be {set(range(1, 6))}")
        for i in range(1, 6):
            if set(ud[i]) != set(ratings[i]):
                raise IncorrectCode(f"ratings dictionary for user {i} incorrect.  Should be {ratings[i]}")
            for movie_id in ud[i]:
                if ud[i][movie_id] != ratings[i][movie_id]:
                    raise IncorrectCode(f"rating of movie {movie_id} by user {i} incorrect.  Should be {ratings[i][movie_id]}")
        print("  passed")
        num_correct += 1
    except IncorrectCode as e:
        print(f"  failed. {e}")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")

    # Test compute_similarity method of Movie class
    try:
        num_tested += 1
        print("Testing compute similarity method of Movie class.")

        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        for movie_id in md:
            for other_movie_id in md:
                if movie_id != other_movie_id:
                    similarity = md[movie_id].compute_similarity(other_movie_id, md, ud)
                    if round(similarity, 2) != similarities[movie_id][other_movie_id]:
                        raise IncorrectCode(f"Similarity between {movie_id} and {other_movie_id} incorrect.  Should be {similarities[movie_id][other_movie_id]}  You computed {similarity}")        
        print("  passed")
        num_correct += 1
    except IncorrectCode as e:
        print(f"  failed. {e}")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")

    # Test get_similarity method of Movie class
    try:
        num_tested += 1
        print("Testing get similarity method of Movie class.")

        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        try:
            md[1].get_similarity(10, md, ud)
        except movie_recommendations.BadInputError:
            pass
        except Exception:
            print(f"  failed.  Your code did not raise BadInputError when invalid movie id is passed to get_similarity")
            raise Exception
        md[1].get_similarity(2, md, ud)
        if 2 not in md[1].similarities or 1 not in md[2].similarities:
            raise IncorrectCode("get_similarity does not save the similarity in both movie entries in the movie dictionary")  
        print("  passed")
        num_correct += 1
    except IncorrectCode as e:
        print(f"  failed. {e}")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")

    # Test predict_rating with a valid movie id
    num_tested += 1
    print("Testing predict_rating with a valid user id and valid movie id")
    try:
        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        predicted_rating = mr.predict_rating(2, 1)
        if round(predicted_rating, 2) == 4.11:
            print("  passed")
            num_correct += 1
        else:
            print(f"  failed.  You returned {predicted_rating} Should have retured 4.11 rounded to 2 decimals")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print("  Should have retured 4.11 rounded to 2 decimals")

    # Test predict_rating with a valid movie id that
    # user has already rated.
    num_tested += 1
    print("Testing predict_rating with a valid user id and valid movie id")
    print("  that user has already rated.")
    try:
        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        predicted_rating = mr.predict_rating(2, 4)
        if round(predicted_rating, 2) == 4:
            print("  passed")
            num_correct += 1
        else:
            print(f"  failed.  You returned {predicted_rating} Should have retured 4 rounded to 2 decimals")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print("  Should have retured 4 rounded to 2 decimals")

    # Test predict_rating with an invalid user id
    # and invalid movie id.
    num_tested += 1
    print("Testing predict_rating with an invalid movie id")
    print("  and an invalid user id")
    try:
        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        predicted_rating = mr.predict_rating(20, 30)
    except movie_recommendations.BadInputError:
        print("  passed")
        num_correct += 1
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print("  Should have raised BadInputError.")
    else:
        print("  failed.  Should have raised BadInputError.")

    # Test predict_ratings.
    num_tested += 1
    print("Testing predict_ratings")
    try:
        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        predicted_ratings = mr.predict_ratings("dummy_test_ratings.csv")
        round_ratings(predicted_ratings)
        if predicted_ratings == [(2, 'M1', 4.11, 5.0), (2, 'M5', 3.82, 5.0), (3, 'M1', 1.5, 0.0), (3, 'M3', 3.0, 3.0), (3, 'M5', 1.43, 5.0), (4, 'M2', 1.1, 4.0), (5, 'M1', 5.0, 2.0), (5, 'M2', 5.0, 2.0), (5, 'M5', 5.0, 2.0)]:
            print("  passed")
            num_correct += 1
        else:
            print("  failed.  You returned")
            print(predicted_ratings)
            print("Should be ")
            print("[(2, 'M1', 4.11, 5.0), (2, 'M5', 3.82, 5.0), (3, 'M1', 1.5, 0.0), (3, 'M3', 3.0, 3.0), (3, 'M5', 1.43, 5.0), (4, 'M2', 1.1, 4.0), (5, 'M1', 5.0, 2.0), (5, 'M2', 5.0, 2.0), (5, 'M5', 5.0, 2.0)]")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print("Should be ")
        print("[(2, 'M1', 4.11, 5.0), (2, 'M5', 3.82, 5.0), (3, 'M1', 1.5, 0.0), (3, 'M3', 3.0, 3.0), (3, 'M5', 1.43, 5.0), (4, 'M2', 1.1, 4.0), (5, 'M1', 5.0, 2.0), (5, 'M2', 5.0, 2.0), (5, 'M5', 5.0, 2.0)]")
    
    # test correlation on dummy test ratings
    num_tested += 1
    print("Testing overall correctness by computing correlation for predictions of test ratings")
    try:
        mr = movie_recommendations.Movie_Recommendations(
            "dummy_movies.csv", "dummy_training_ratings.csv")
        ud = mr.user_dict
        md = mr.movie_dict
        rating_predictions = mr.predict_ratings("dummy_test_ratings.csv")
        predicted = [rating[2] for rating in rating_predictions]
        actual = [rating[3] for rating in rating_predictions]
        correlation = mr.correlation(predicted, actual)
        print(f"Correlation: {correlation}") 
        if round(correlation, 2) == -0.13:
            print("  passed")
            num_correct += 1
        else:
            print("  failed.  You returned")
            print(correlation)
            print(f"Should be {-0.13}")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print(f"Should be {-0.13}")
        
    if num_correct == num_tested:
        print("Everything correct.  Move on to testing on the full, real")
        print("movie database by running test_psa4B.py.")
    else:
        print("One or more incorrect.  Fix before submitting.")
        print("Num tested =", num_tested)
        print("Num correct =", num_correct)

def round_ratings(predicted_ratings):
    """
    Round the predicted rating in each tuple to 2 decimal places
    """
    for i in range(len(predicted_ratings)):
        entry = predicted_ratings[i]
        predicted_ratings[i] = (entry[0], entry[1], round(entry[2], 2), entry[3])

if __name__ == "__main__":
    test_psa4()
