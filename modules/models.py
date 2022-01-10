from flask_login import UserMixin
from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey, DateTime, text
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

    def get_all(self):
        return self.bullets.order_by(text("date_created desc"))

    def get_tasks(self):
        return self.bullets.filter(Bullet.type_ == "Task").order_by(Bullet.done, text("date_created desc"))

    def get_events(self):
        return self.bullets.filter(Bullet.type_ == "Event").order_by(text("event_date"))

    def get_notes(self):
        return self.bullets.filter(Bullet.type_ == "Note").order_by(text("date_created desc"))

    def get_pinned(self):
        return self.bullets.filter(Bullet.pinned == True)


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
