#!/usr/bin/env python3

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from lib.db.session import create_tables, get_db_session
from lib.models.author import Author
from lib.models.book import Book, ReadingStatus
from lib.models.review import Review

def test():
    # Create tables
    create_tables()
    
    # Get session
    db = get_db_session()
    
    # Create test data
    author = Author.create(db, "Test Author", "Test biography")
    book = Book.create(db, "Test Book", author.id, "Test Genre", 100, ReadingStatus.UNREAD)
    review = Review.create(db, book.id, 5, "Great book!")
    
    print("Test successful!")
    print(f"Author: {author.name}")
    print(f"Book: {book.title}")
    print(f"Review: {review.rating} stars")

if __name__ == "__main__":
    test()