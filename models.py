from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import BaseModel


# Таблица жанров
class Genre(BaseModel):
    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True)
    name_genre = Column(String, nullable=False)

    # Связь с книгами
    books = relationship("Book", back_populates="genre")


# Таблица авторов
class Author(BaseModel):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    name_author = Column(String, nullable=False)

    # Связь с книгами
    books = relationship("Book", back_populates="author")


# Таблица городов
class City(BaseModel):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    name_city = Column(String, nullable=False)
    days_delivery = Column(Integer, nullable=False)

    # Связь с клиентами
    clients = relationship("Client", back_populates="city")


# Таблица клиентов
class Client(BaseModel):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    name_client = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('city.city_id'))
    email = Column(String, nullable=False)

    # Связи с другими таблицами
    city = relationship("City", back_populates="clients")
    buys = relationship("Buy", back_populates="client")


# Таблица книг
class Book(BaseModel):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    price = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)

    # Связи с другими таблицами
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    buy_books = relationship("BuyBook", back_populates="book")


# Таблица покупок
class Buy(BaseModel):
    __tablename__ = 'buy'

    buy_id = Column(Integer, primary_key=True)
    buy_description = Column(String)
    client_id = Column(Integer, ForeignKey('client.client_id'))

    # Связи с другими таблицами
    client = relationship("Client", back_populates="buys")
    buy_books = relationship("BuyBook", back_populates="buy")
    buy_steps = relationship("BuyStep", back_populates="buy")


# Таблица этапов покупки
class Step(BaseModel):
    __tablename__ = 'step'

    step_id = Column(Integer, primary_key=True)
    name_step = Column(String, nullable=False)

    # Связь с таблицей buy_step
    buy_steps = relationship("BuyStep", back_populates="step")


# Таблица покупаемых книг
class BuyBook(BaseModel):
    __tablename__ = 'buy_book'

    buy_book_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    amount = Column(Integer, nullable=False)

    # Связи с другими таблицами
    buy = relationship("Buy", back_populates="buy_books")
    book = relationship("Book", back_populates="buy_books")


# Таблица шагов покупки
class BuyStep(BaseModel):
    __tablename__ = 'buy_step'

    buy_step_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))
    date_step_beg = Column(DateTime, nullable=False)
    date_step_end = Column(DateTime)

    # Связи с другими таблицами
    buy = relationship("Buy", back_populates="buy_steps")
    step = relationship("Step", back_populates="buy_steps")
