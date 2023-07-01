from app import db
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from urllib.parse import urlparse


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("group.id"), default=0)

    bookmarks = db.relationship("Bookmark", back_populates="group")
    children = db.relationship("Group")

    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Group {self.name}>"


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    modified_on = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    group = db.relationship("Group", back_populates="bookmarks")

    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)

    @hybrid_property
    def formatted_url(self) -> str:
        scheme = "https" if urlparse(self.url).scheme != "http" else "http"
        url = urlparse(self.url)._replace(scheme=scheme).geturl()
        return url

    def __repr__(self):
        return f"<Bookmark {self.title}>"
