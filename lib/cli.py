#!/usr/bin/env python3

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.helpers import (
    get_db_session, exit_program, display_authors, display_books, display_reviews
)
from lib.models import Author, Book, Review, ReadingStatus

def main():
    db = get_db_session()
    
    while True:
        main_menu()
        choice = input("> ")
        
        if choice == "0":
            exit_program()
        elif choice == "1":
            author_menu(db)
        elif choice == "2":
            book_menu(db)
        elif choice == "3":
            review_menu(db)
        elif choice == "4":
            search_menu(db)
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    print("\n📚 PERSONAL BOOK COLLECTION MANAGER")
    print("=" * 40)
    print("1. Manage Authors")
    print("2. Manage Books")
    print("3. Manage Reviews")
    print("4. Search")
    print("0. Exit")
    print("=" * 40)

def author_menu(db):
    while True:
        print("\n👤 AUTHOR MANAGEMENT")
        print("1. View all authors")
        print("2. Add new author")
        print("3. Find author by name")
        print("4. Delete author")
        print("5. Back to main menu")
        
        choice = input("> ")
        
        if choice == "1":
            authors = Author.get_all(db)
            display_authors(authors)
        elif choice == "2":
            name = input("Enter author name: ").strip()
            biography = input("Enter biography (optional): ").strip() or None
            if name:
                Author.create(db, name, biography)
                print("Author created successfully!")
            else:
                print("Author name is required.")
        elif choice == "3":
            name = input("Enter author name to search: ").strip()
            if name:
                authors = Author.find_by_name(db, name)
                display_authors(authors)
            else:
                print("Please enter a name to search.")
        elif choice == "4":
            author_id = input("Enter author ID to delete: ").strip()
            if author_id.isdigit():
                if Author.delete(db, int(author_id)):
                    print("Author deleted successfully!")
                else:
                    print("Author not found.")
            else:
                print("Please enter a valid ID.")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def book_menu(db):
    while True:
        print("\n📖 BOOK MANAGEMENT")
        print("1. View all books")
        print("2. Add new book")
        print("3. Find book by title")
        print("4. Find books by author")
        print("5. Find books by genre")
        print("6. Update book status")
        print("7. Delete book")
        print("8. Back to main menu")
        
        choice = input("> ")
        
        if choice == "1":
            books = Book.get_all(db)
            display_books(books, show_details=True)
        elif choice == "2":
            title = input("Enter book title: ").strip()
            author_id = input("Enter author ID: ").strip()
            genre = input("Enter genre (optional): ").strip() or None
            pages = input("Enter number of pages (optional): ").strip()
            
            if title and author_id.isdigit():
                author = Author.find_by_id(db, int(author_id))
                if author:
                    Book.create(
                        db, title, int(author_id), genre,
                        int(pages) if pages.isdigit() else None
                    )
                    print("Book created successfully!")
                else:
                    print("Author not found.")
            else:
                print("Title and valid author ID are required.")
        elif choice == "3":
            title = input("Enter book title to search: ").strip()
            if title:
                books = Book.find_by_title(db, title)
                display_books(books)
            else:
                print("Please enter a title to search.")
        elif choice == "4":
            author_id = input("Enter author ID: ").strip()
            if author_id.isdigit():
                books = Book.find_by_author(db, int(author_id))
                display_books(books)
            else:
                print("Please enter a valid author ID.")
        elif choice == "5":
            genre = input("Enter genre to search: ").strip()
            if genre:
                books = Book.find_by_genre(db, genre)
                display_books(books)
            else:
                print("Please enter a genre to search.")
        elif choice == "6":
            book_id = input("Enter book ID: ").strip()
            if book_id.isdigit():
                book = Book.find_by_id(db, int(book_id))
                if book:
                    print("Current status:", book.status.value)
                    print("1. Unread")
                    print("2. Reading")
                    print("3. Finished")
                    status_choice = input("Select new status: ").strip()
                    
                    status_map = {
                        "1": ReadingStatus.UNREAD,
                        "2": ReadingStatus.READING,    #menu choice mapping
                        "3": ReadingStatus.FINISHED
                    }
                    
                    if status_choice in status_map:
                        book.update_status(db, status_map[status_choice])
                        print("Status updated successfully!")
                    else:
                        print("Invalid status choice.")
                else:
                    print("Book not found.")
            else:
                print("Please enter a valid book ID.")
        elif choice == "7":
            book_id = input("Enter book ID to delete: ").strip()
            if book_id.isdigit():
                if Book.delete(db, int(book_id)):
                    print("Book deleted successfully!")
                else:
                    print("Book not found.")
            else:
                print("Please enter a valid ID.")
        elif choice == "8":
            break
        else:
            print("Invalid choice.")

def review_menu(db):
    while True:
        print("\n⭐ REVIEW MANAGEMENT")
        print("1. View all reviews")
        print("2. Add new review")
        print("3. Find reviews for book")
        print("4. Find reviews by rating")
        print("5. Delete review")
        print("6. Back to main menu")
        
        choice = input("> ")
        
        if choice == "1":
            reviews = Review.get_all(db)
            display_reviews(reviews)
        elif choice == "2":
            book_id = input("Enter book ID: ").strip()
            rating = input("Enter rating (1-5): ").strip()
            comment = input("Enter comment (optional): ").strip() or None
            
            if book_id.isdigit() and rating.isdigit() and 1 <= int(rating) <= 5:
                book = Book.find_by_id(db, int(book_id))
                if book:
                    Review.create(db, int(book_id), int(rating), comment)
                    print("Review created successfully!")
                else:
                    print("Book not found.")
            else:
                print("Valid book ID and rating (1-5) are required.")
        elif choice == "3":
            book_id = input("Enter book ID: ").strip()
            if book_id.isdigit():
                reviews = Review.find_by_book(db, int(book_id))
                display_reviews(reviews)
            else:
                print("Please enter a valid book ID.")
        elif choice == "4":
            min_rating = input("Enter minimum rating (1-5): ").strip()
            if min_rating.isdigit() and 1 <= int(min_rating) <= 5:
                reviews = Review.find_by_rating(db, int(min_rating))
                display_reviews(reviews)
            else:
                print("Please enter a valid rating between 1-5.")
        elif choice == "5":
            review_id = input("Enter review ID to delete: ").strip()
            if review_id.isdigit():
                if Review.delete(db, int(review_id)):
                    print("Review deleted successfully!")
                else:
                    print("Review not found.")
            else:
                print("Please enter a valid ID.")
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

def search_menu(db):
    while True:
        print("\n🔍 SEARCH")
        print("1. Search books by title")
        print("2. Search books by genre")
        print("3. Search authors by name")
        print("4. Find highly rated books (4+ stars)")
        print("5. Back to main menu")
        
        choice = input("> ")
        
        if choice == "1":
            title = input("Enter book title to search: ").strip()
            if title:
                books = Book.find_by_title(db, title)
                display_books(books, show_details=True)
            else:
                print("Please enter a title to search.")
        elif choice == "2":
            genre = input("Enter genre to search: ").strip()
            if genre:
                books = Book.find_by_genre(db, genre)
                display_books(books, show_details=True)
            else:
                print("Please enter a genre to search.")
        elif choice == "3":
            name = input("Enter author name to search: ").strip()
            if name:
                authors = Author.find_by_name(db, name)
                display_authors(authors)
            else:
                print("Please enter a name to search.")
        elif choice == "4":
            # Find books with average rating >= 4
            books = Book.get_all(db)
            highly_rated = [book for book in books if book.reviews and book.average_rating >= 4]
            display_books(highly_rated, show_details=True)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()