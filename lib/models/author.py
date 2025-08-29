from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from lib.db.session import Base

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    biography = Column(Text)
    
    # One-to-many relationship with books
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"
    
    @classmethod
    def create(cls, db, name, biography=None):
        author = cls(name=name, biography=biography)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author
    
    @classmethod
    def get_all(cls, db):
        return db.query(cls).all() #returns list of author objects
    
    @classmethod
    def find_by_id(cls, db, author_id):
        return db.query(cls).filter(cls.id == author_id).first() #return list
    
    @classmethod
    def find_by_name(cls, db, name):
        return db.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
    
    @classmethod
    def delete(cls, db, author_id):
        author = cls.find_by_id(db, author_id)
        if author:
            db.delete(author)
            db.commit()
            return True
        return False