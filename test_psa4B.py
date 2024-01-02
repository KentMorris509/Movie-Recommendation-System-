# File: test_psa4B.py
# Author: John Glick    
# Date: March 6, 2020
# Description: Program that tests the correctness
#              of comp 120, psa4,
#              on `movie rating database.

import sys

# import the module containing psa4 solution
import movie_recommendations

def test_psa4():
    # Do tests with the dummy files.

    # Create movie recommendation object using dummy movies and ratings.
    rc = movie_recommendations.Movie_Recommendations(
        "movies.csv", "training_ratings.csv")

    # Initialize test count
    num_correct = 0
    num_tested = 0

    # Test get_movie_similarity
    num_tested += 1
    print("Testing get_similarity")
    try:
        similarity = rc.movie_dict[1196].get_similarity(112852, rc.movie_dict, rc.user_dict)
        if round(similarity, 2) == 0.82:
            print("  passed")
            num_correct += 1
        else:
            print(f"  failed.  You returned {similarity}.  similarity should be 0.82 rounded to 2 decimals")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print("  similarity should be 0.82, rounded to 2 decimals")

    # Test predict_rating
    num_tested += 1
    print("Testing predict_rating")
    try:
        predicted_rating = rc.predict_rating(483, 1589)
        if round(predicted_rating, 2) == 3.65:
            print("  passed")
            num_correct += 1
        else:
            print(f"  failed.  You returned {predicted_rating} Should have retured 3.65 rounded to 2 decimals")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print("  Should have retured 3.65 rounded to 2 decimals")
    
    # test correlation on test ratings
    num_tested += 1
    print("Testing correlation on test ratings")
    try:
        rating_predictions = rc.predict_ratings("test_ratings.csv")
        predicted = [rating[2] for rating in rating_predictions]
        actual = [rating[3] for rating in rating_predictions]
        correlation = rc.correlation(predicted, actual)
        if round(correlation, 2) == 0.47:
            print("  passed")
            num_correct += 1
        else:
            print("  failed.  You returned")
            print(correlation)
            print(f"Should be {0.47}")
    except Exception as e:
        print(f"  failed.  Your code raised the exception {e}")
        print(f"Should be {0.47}")
        
    if num_correct == num_tested:
        print("Everything correct.  Make sure you have followed all")
        print("program requirements, and then sync to repository")
        print("and post to Piazza (folder #psa4_submit) saying you are submitting")
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
