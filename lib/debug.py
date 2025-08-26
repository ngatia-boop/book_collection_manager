#!/usr/bin/env python3

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.session import get_db_session, create_tables
from lib.models import Author, Book, Review, ReadingStatus

def debug():
    db = get_db_session()
    
    # Create tables if they don't exist
    create_tables()
    
    # Sample data for testing
    author = Author.create(db, "J.K. Rowling", "British author best known for Harry Potter series")
    book = Book.create(db, "Harry Potter and the Philosopher's Stone", author.id, "Fantasy", 320, ReadingStatus.FINISHED)
    review = Review.create(db, book.id, 5, "A magical start to an incredible series!")
    
    print("Sample data created:")
    print(f"Author: {author.name}")
    print(f"Book: {book.title}")
    print(f"Review: {review.rating} stars - {review.comment}")
    
    # Test relationships
    print(f"\nAuthor's books: {[b.title for b in author.books]}")
    print(f"Book's reviews: {[f'{r.rating} stars' for r in book.reviews]}")
    print(f"Book average rating: {book.average_rating}")

if __name__ == "__main__":
    debug()