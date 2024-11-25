import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self):
        # Sample data: rows are users, columns are movies, values are ratings (1-5)
        self.ratings = np.array([
            [5, 3, 0, 1, 4, 0],
            [4, 0, 3, 1, 2, 4],
            [1, 2, 4, 0, 0, 5],
            [0, 4, 2, 5, 3, 0],
            [2, 0, 1, 4, 0, 3]
        ])
        
        # Sample movie titles
        self.movies = [
            "MAX",
            "Hebbuli",
            "KGF",
            "Love Mocktail",
            "Bagheera",
            "Ranna"
        ]
        
        # Dictionary to store user-movie ratings
        self.user_ratings = {}
        
    def get_movie_index(self, movie_name):
        """Get the index of a movie by its name"""
        try:
            return self.movies.index(movie_name)
        except ValueError:
            raise ValueError(f"Movie '{movie_name}' not found in database")
        
    def add_user_rating(self, user_id, movie_ratings):
        """
        Add ratings for a user using movie names instead of indices
        movie_ratings: Dictionary with movie names as keys and ratings as values
        """
        if len(movie_ratings) > len(self.movies):
            raise ValueError("Too many movie ratings provided")
            
        user_vector = np.zeros(len(self.movies))
        for movie_name, rating in movie_ratings.items():
            movie_idx = self.get_movie_index(movie_name)
            if not (0 <= rating <= 5):
                raise ValueError(f"Rating must be between 0 and 5")
            user_vector[movie_idx] = rating
            
        self.user_ratings[user_id] = user_vector
        
    def get_recommendations(self, user_id, n_recommendations=3):
        if user_id not in self.user_ratings:
            raise ValueError("User not found")
            
        # Combine ratings matrix with user ratings
        all_ratings = np.vstack([self.ratings, self.user_ratings[user_id]])
        
        # Calculate similarity between the target user and all other users
        user_similarities = cosine_similarity([all_ratings[-1]], all_ratings[:-1])[0]
        
        # Get weighted average of ratings for movies the user hasn't rated
        user_ratings = all_ratings[-1]
        unrated_movies = np.where(user_ratings == 0)[0]
        
        predictions = []
        for movie_idx in unrated_movies:
            # Get ratings for this movie from other users
            other_ratings = self.ratings[:, movie_idx]
            # Calculate weighted average rating
            weighted_rating = np.sum(other_ratings * user_similarities) / np.sum(user_similarities)
            predictions.append((self.movies[movie_idx], weighted_rating))
        
        # Sort by predicted rating and return top n recommendations
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:n_recommendations]
    
    def get_available_movies(self):
        """Return list of all available movies"""
        return self.movies

# Example usage
if __name__ == "__main__":
    # Initialize the recommender
    recommender = MovieRecommender()
    
    # Print available movies
    print("Available movies:")
    for movie in recommender.get_available_movies():
        print(f"- {movie}")
    
    # Add ratings for a new user using movie names
    user_ratings = {
        "KGF": 5,
        "Hebbuli": 4,
        "Love Mocktail": 3,
        "Ranna": 0
    }
    recommender.add_user_rating("new_user", user_ratings)
    
    # Get recommendations
    print("\nRecommended movies:")
    recommendations = recommender.get_recommendations("new_user")
    for movie, score in recommendations:
        print(f"{movie}: {score:.2f}/5")