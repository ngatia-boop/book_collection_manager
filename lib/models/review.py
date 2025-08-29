from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from lib.db.session import Base

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    book_id = Column(Integer, ForeignKey('books.id'))
    
    # Relationship
    book = relationship("Book", back_populates="reviews")
    
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_bounds'),
    ) #Table constraints(tuples)
    
    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"
    
    @classmethod
    def create(cls, db, book_id, rating, comment=None):
        review = cls(book_id=book_id, rating=rating, comment=comment)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    
    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()
    
    @classmethod
    def find_by_id(cls, db, review_id):
        return db.query(cls).filter(cls.id == review_id).first()
    
    @classmethod
    def find_by_book(cls, db, book_id):
        return db.query(cls).filter(cls.book_id == book_id).all()
    
    @classmethod
    def find_by_rating(cls, db, min_rating):
        return db.query(cls).filter(cls.rating >= min_rating).all()
    
    @classmethod
    def delete(cls, db, review_id):
        review = cls.find_by_id(db, review_id)
        if review:
            db.delete(review)
            db.commit()
            return True
        return False