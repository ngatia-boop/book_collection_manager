# Personal Book Collection Manager

A command-line interface (CLI) application for managing your personal book collection, tracking reading progress, and writing reviews.

## Features

- **Author Management**: Create, view, search, and delete authors
- **Book Tracking**: Add books with titles, genres, page counts, and reading status
- **Review System**: Rate books (1-5 stars) and add comments
- **Search Functionality**: Find books by title, genre, or author
- **Reading Progress**: Track whether books are unread, reading, or finished

## Installation

1. Clone the repository
2. Install dependencies: `pipenv install`
3. Enter virtual environment: `pipenv shell`
4. Initialize database: `python lib/debug.py`
5. Seed with sample data (optional): `python lib/db/seed.py`

## Usage

Run the application: `python lib/cli.py`

### Main Menu Options:
1. **Manage Authors**: CRUD operations for authors
2. **Manage Books**: Add, view, update status, and delete books
3. **Manage Reviews**: Create and view book reviews
4. **Search**: Find books and authors by various criteria

## Database Schema

- **Authors**: id, name, biography
- **Books**: id, title, genre, pages, status, author_id (FK)
- **Reviews**: id, rating, comment, book_id (FK)

## Relationships

- One Author → Many Books (one-to-many)
- One Book → Many Reviews (one-to-many)
- Books have computed average ratings from their reviews

## File Structure
```

lib/
├── cli.py # Main CLI interface
├── debug.py # Debug and testing script
├── helpers/ # Helper functions
├── models/ # SQLAlchemy models
│ ├── author.py
│ ├── book.py
│ └── review.py
└── db/ # Database configuration
├── session.py
└── seed.py
```


## Dependencies

- SQLAlchemy: ORM for database operations
- Alembic: Database migrations
- Faker: Generate sample data
- python-dotenv: Environment variable management

## Run the Application

# Initialize database
python lib/debug.py

# Seed with sample data (optional)
python lib/db/seed.py

# Run the CLI
python lib/cli.py

## AUTHOR
ANN NGATIA - MORINGA SCHOOL
