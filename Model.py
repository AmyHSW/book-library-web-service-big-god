from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
import enum

db = SQLAlchemy()


class User(db.Model):
    UserId = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(80), unique=True, nullable=False)
    PassWord = db.Column(db.String(80), unique=False, nullable=False)
    
    def serialize(self):
        res = Serializer.serialize(self)
        return res


class Author(db.Model):
    AutherID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), unique=False, nullable=False)
    LastName = db.Column(db.String(80), unique=False, nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class Genre(enum.Enum):
    Science = 'Science'
    Horror = 'Horror'


class List(db.Model):
    ListId = db.Column(db.Integer, primary_key=True)
    ListName = db.Column(db.String(80), unique=False, nullable=False)
    Created = db.Column(db.DateTime, unique=False, nullable=True)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    OwnerID = db.Column(db.Integer, db.ForeignKey(User.UserId),nullable=False)
    BookName = db.Column(db.String(80), unique=False, nullable=False)
    PublishDate = db.Column(db.DateTime, unique=False, nullable=False)
    LoanedOut = db.Column(db.Boolean, unique=False, nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class Note(db.Model):
    NoteId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookID),nullable=False)
    Content = db.Column(db.String(300), unique=False, nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class LoanHistory(db.Model):
    LoanId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookID),nullable=False)
    BorrowerId = db.Column(db.Integer, db.ForeignKey(User.UserId),nullable=False)
    Due = db.Column(db.DateTime, unique=False, nullable=True)
    ActualReturnDate = db.Column(db.DateTime, unique=False, nullable=True)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class BookToAuthors(db.Model):
    BookToAuthorsMapId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookID),nullable=False)
    AutherID = db.Column(db.Integer, db.ForeignKey(Author.AutherID),nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class BookToGenres(db.Model):
    BookToGenresId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookID),nullable=False)
    Genre = db.Column(db.Enum(Genre))

    def serialize(self):
        res = Serializer.serialize(self)
        return res


class ListToBooks(db.Model):
    ListToBooks = db.Column(db.Integer, primary_key=True)
    ListId = db.Column(db.Integer, db.ForeignKey(List.ListId),nullable=False)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookID),nullable=False)

    def serialize(self):
        res = Serializer.serialize(self)
        return res


# Serializer that converts class objects to json
class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
