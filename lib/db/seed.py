import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lib.db.session import SessionLocal
from lib.models import Author, Book, Review, ReadingStatus
from faker import Faker

fake = Faker()

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data (optional)
        db.query(Review).delete()
        db.query(Book).delete()
        db.query(Author).delete()
        db.commit()
        
        # Create authors
        authors = []
        for _ in range(5):
            author = Author.create(
                db,
                name=fake.name(),
                biography=fake.text()
            )
            authors.append(author)
        
        # Create books for each author
        books = []
        for author in authors:
            for _ in range(3):
                book = Book.create(
                    db,
                    title=fake.catch_phrase(),
                    author_id=author.id,
                    genre=fake.word(),
                    pages=fake.random_int(100, 500),
                    status=fake.random_element(list(ReadingStatus))
                )
                books.append(book)
        
        # Create reviews for some books
        for book in books[:8]:  # Reviews for first 8 books
            for _ in range(2):
                Review.create(
                    db,
                    book_id=book.id,
                    rating=fake.random_int(1, 5),
                    comment=fake.sentence()
                )
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()