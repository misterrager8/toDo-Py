from flask_login import UserMixin
from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from modules import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    date_joined = Column(DateTime)
    bullets = relationship("Bullet", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Bullet(db.Model):
    __tablename__ = "bullets"

    # Generic attrs
    type_ = Column(Text)  # ["Task", "Event", or "Note"]
    content = Column(Text)
    date_created = Column(DateTime)
    pinned = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    # Task attrs
    done = Column(Boolean)
    date_done = Column(DateTime)

    # Event attrs
    event_date = Column(DateTime)

    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)

    def bullet_color(self):
        if self.type_ == "Event":
            return "#12664F"
        elif self.type_ == "Task":
            return "#320D6D"
        elif self.type_ == "Note":
            return "#FFD447"
