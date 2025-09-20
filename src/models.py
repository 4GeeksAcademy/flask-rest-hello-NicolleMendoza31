from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean , ForeignKey , DateTime
from sqlalchemy.orm import Mapped, mapped_column ,  relationship
import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(250))
    caption: Mapped[str] = mapped_column(String(500))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(300))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")
