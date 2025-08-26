from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from lib.db.session import Base
import enum

class ReadingStatus(enum.Enum):
    UNREAD = "unread"
    READING = "reading"
    FINISHED = "finished"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    pages = Column(Integer)
    status = Column(Enum(ReadingStatus), default=ReadingStatus.UNREAD)
    author_id = Column(Integer, ForeignKey('authors.id'))
    
    # Relationships
    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"
    
    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    @classmethod
    def create(cls, db, title, author_id, genre=None, pages=None, status=ReadingStatus.UNREAD):
        book = cls(title=title, author_id=author_id, genre=genre, pages=pages, status=status)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    
    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()
    
    @classmethod
    def find_by_id(cls, db, book_id):
        return db.query(cls).filter(cls.id == book_id).first()
    
    @classmethod
    def find_by_title(cls, db, title):
        return db.query(cls).filter(cls.title.ilike(f"%{title}%")).all()
    
    @classmethod
    def find_by_author(cls, db, author_id):
        return db.query(cls).filter(cls.author_id == author_id).all()
    
    @classmethod
    def find_by_genre(cls, db, genre):
        return db.query(cls).filter(cls.genre.ilike(f"%{genre}%")).all()
    
    @classmethod
    def delete(cls, db, book_id):
        book = cls.find_by_id(db, book_id)
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
    
    def update_status(self, db, status):
        self.status = status
        db.commit()
        db.refresh(self)