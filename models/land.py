from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Land(Base):
    __tablename__ = 'lands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plants = relationship('Plant', back_populates='land')
