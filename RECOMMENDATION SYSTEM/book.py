import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class BookRecommender:
    def __init__(self):
        # Initialize with sample book data
        self.books = {
            'book1': {
                'title': 'The Great Gatsby',
                'authors': ['F. Scott Fitzgerald'],
                'categories': ['Fiction', 'Classic', 'Romance'],
                'publisher': 'Scribner',
                'published_date': '1925',
                'average_rating': 4.2,
            },
            'book2': {
                'title': '1984',
                'authors': ['George Orwell'],
                'categories': ['Fiction', 'Science Fiction', 'Dystopian'],
                'publisher': 'Secker and Warburg',
                'published_date': '1949',
                'average_rating': 4.5,
            },
            'book3': {
                'title': 'Pride and Prejudice',
                'authors': ['Jane Austen'],
                'categories': ['Fiction', 'Classic', 'Romance'],
                'publisher': 'T. Egerton',
                'published_date': '1813',
                'average_rating': 4.3,
            },
            'book4': {
                'title': 'The Hobbit',
                'authors': ['J.R.R. Tolkien'],
                'categories': ['Fiction', 'Fantasy', 'Adventure'],
                'publisher': 'Allen & Unwin',
                'published_date': '1937',
                'average_rating': 4.6,
            },
            'book5': {
                'title': 'To Kill a Mockingbird',
                'authors': ['Harper Lee'],
                'categories': ['Fiction', 'Classic', 'Literary'],
                'publisher': 'J. B. Lippincott & Co.',
                'published_date': '1960',
                'average_rating': 4.4,
            }
        }
        
        # Store user ratings
        self.book_ratings = defaultdict(dict)  # user_id -> {book_id -> rating}

    def search_book(self, query):
        """Search for a book by title or author"""
        query = query.lower()
        results = []
        
        for book_id, book in self.books.items():
            if (query in book['title'].lower() or 
                any(query in author.lower() for author in book['authors'])):
                results.append({
                    'id': book_id,
                    'title': book['title'],
                    'authors': book['authors'],
                    'published_date': book['published_date'],
                    'average_rating': book['average_rating']
                })
                
        return results[:5]  # Return top 5 matches

    def add_user_rating(self, user_id, book_id, rating):
        """Add a user rating for a book"""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
            
        if book_id not in self.books:
            raise ValueError("Book not found")
            
        self.book_ratings[user_id][book_id] = rating
        
    def calculate_book_similarity(self, book_id1, book_id2):
        """Calculate similarity between two books based on features"""
        book1 = self.books[book_id1]
        book2 = self.books[book_id2]
        
        # Calculate author similarity
        authors1 = set(book1['authors'])
        authors2 = set(book2['authors'])
        author_sim = len(authors1.intersection(authors2)) / len(authors1.union(authors2)) if authors1 or authors2 else 0
        
        # Calculate category similarity
        categories1 = set(book1['categories'])
        categories2 = set(book2['categories'])
        category_sim = len(categories1.intersection(categories2)) / len(categories1.union(categories2)) if categories1 or categories2 else 0
        
        # Calculate publisher similarity
        publisher_sim = 1 if book1['publisher'] == book2['publisher'] else 0
        
        # Weighted similarity
        return 0.4 * category_sim + 0.4 * author_sim + 0.2 * publisher_sim

    def get_recommendations(self, user_id, n_recommendations=3):
        """Get book recommendations for a user"""
        if user_id not in self.book_ratings:
            raise ValueError("User not found")
            
        # Get books rated by the user
        rated_books = set(self.book_ratings[user_id].keys())
        
        # Calculate recommendations
        recommendations = []
        for book_id in self.books:
            if book_id not in rated_books:
                # Calculate weighted rating based on similar books
                similarity_scores = []
                weighted_ratings = []
                
                for rated_book_id, rating in self.book_ratings[user_id].items():
                    similarity = self.calculate_book_similarity(book_id, rated_book_id)
                    if similarity > 0:
                        similarity_scores.append(similarity)
                        weighted_ratings.append(rating * similarity)
                
                if similarity_scores:
                    predicted_rating = sum(weighted_ratings) / sum(similarity_scores)
                    book = self.books[book_id]
                    recommendations.append((
                        book_id,
                        predicted_rating,
                        book['title'],
                        book['authors'],
                        book['published_date']
                    ))
        
        # Sort by predicted rating and return top n
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]

def format_authors(authors):
    """Format author list for display"""
    if not authors:
        return "Unknown Author"
    elif len(authors) == 1:
        return authors[0]
    else:
        return ", ".join(authors[:-1]) + " and " + authors[-1]

def main():
    # Initialize recommender
    recommender = BookRecommender()
    
    while True:
        print("\n1. Search for a book")
        print("2. Rate a book")
        print("3. Get recommendations")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            query = input("Enter book title or author to search: ")
            results = recommender.search_book(query)
            if results:
                print("\nSearch results:")
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book['title']}")
                    print(f"   Author(s): {format_authors(book['authors'])}")
                    print(f"   Published: {book['published_date']}")
                    print(f"   Average Rating: {book['average_rating']}\n")
            else:
                print("No books found.")
                
        elif choice == '2':
            user_id = input("Enter your user ID: ")
            query = input("Enter book title to rate: ")
            results = recommender.search_book(query)
            
            if results:
                print("\nSearch results:")
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book['title']} by {format_authors(book['authors'])}")
                    
                book_choice = int(input("Select book number: ")) - 1
                if 0 <= book_choice < len(results):
                    rating = float(input("Enter rating (1-5): "))
                    recommender.add_user_rating(user_id, results[book_choice]['id'], rating)
                    print("Rating added successfully!")
                else:
                    print("Invalid selection.")
            else:
                print("No books found.")
                
        elif choice == '3':
            user_id = input("Enter your user ID: ")
            try:
                recommendations = recommender.get_recommendations(user_id)
                print("\nRecommended books:")
                for book_id, rating, title, authors, published_date in recommendations:
                    print(f"\n{title}")
                    print(f"by {format_authors(authors)}")
                    print(f"Published: {published_date}")
                    print(f"Predicted rating: {rating:.2f}/5")
            except ValueError as e:
                print(e)
                
        elif choice == '4':
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()