import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lib.db.session import get_db_session as _get_db_session
from lib.models import Author, Book, Review, ReadingStatus

def get_db_session():
    return _get_db_session()

def exit_program():
    print("Goodbye!")
    exit()

def display_authors(authors):
    if not authors:
        print("No authors found.")
        return
    
    print("\n=== AUTHORS ===")
    for author in authors:
        print(f"{author.id}. {author.name}")
        if author.biography:
            print(f"   Biography: {author.biography[:100]}...")
        print(f"   Books: {len(author.books)}")
        print()

def display_books(books, show_details=False):
    if not books:
        print("No books found.")
        return
    
    print("\n=== BOOKS ===")
    for book in books:
        status_emoji = {
            ReadingStatus.UNREAD: "📚",
            ReadingStatus.READING: "📖",
            ReadingStatus.FINISHED: "✅"
        }
        
        print(f"{book.id}. {status_emoji[book.status]} {book.title}")
        print(f"   Author: {book.author.name}")
        print(f"   Genre: {book.genre}")
        print(f"   Pages: {book.pages}")
        print(f"   Status: {book.status.value}")
        
        if show_details and book.reviews:
            avg_rating = book.average_rating
            print(f"   Average Rating: {avg_rating:.1f}/5")
            print(f"   Reviews: {len(book.reviews)}")
        print()

def display_reviews(reviews):
    if not reviews:
        print("No reviews found.")
        return
    
    print("\n=== REVIEWS ===")
    for review in reviews:
        stars = "⭐" * review.rating + "☆" * (5 - review.rating)
        print(f"{review.id}. {stars} - {review.book.title}")
        if review.comment:
            print(f"   Comment: {review.comment}")
        print()