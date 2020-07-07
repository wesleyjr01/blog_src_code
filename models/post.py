import uuid
import os
from markdown import markdown
from datetime import datetime
from googletrans import Translator
from typing import List, Dict
import pymongo

from common.database import Database
from helper import apology


class Post:

    collection = "posts"

    def __init__(
        self,
        en_title,
        en_raw_text,
        username,
        user_id,
        pt_title=None,
        en_md_text=None,
        pt_md_text=None,
        _id=None,
        date=None,
    ):
        self.en_title = en_title
        self.en_raw_text = en_raw_text
        self.username = username
        self.user_id = user_id
        self.pt_title = (
            pt_title or Translator().translate(self.en_title, dest="pt").text
        )
        self.en_md_text = en_md_text or markdown(
            self.en_raw_text, extensions=["fenced_code"]
        )
        self.pt_md_text = markdown(
            Translator().translate(self.en_md_text, dest="pt").text,
        )
        self._id = _id or uuid.uuid4().hex
        self.date = date or datetime.now().strftime("%d-%b-%Y %H:%M")

    def json(self):
        return {
            "_id": self._id,
            "en_title": self.en_title,
            "en_raw_text": self.en_raw_text,
            "en_md_text": self.en_md_text,
            "pt_title": self.pt_title,
            "pt_md_text": self.pt_md_text,
            "username": self.username,
            "user_id": self.user_id,
            "date": self.date,
        }

    def valid_post(self):
        """
        Check where the title and post body text are valid.
        """

        # Ensure title was submitted
        if not self.en_title:
            return False, "must provide a title"

        # Ensure title was submitted
        elif not self.en_raw_text:
            return False, "must provide a text body"

        elif self.username != os.environ.get("ADMIN_USR"):
            return False, "only admin can make new posts."

        else:
            return True, "Post submitted successfully!"

    def insert_to_db(self):
        """
        Register a new post, in case the username is the admin only.
        """

        admin = os.environ.get("ADMIN_USR")
        if not self.username == admin:
            return apology("Permission denied.")
        else:
            Database.insert(self.collection, self.json())

    @classmethod
    def get_posts(cls, username) -> List[Dict]:
        """
        Find the username in the database, and return None if no user with
        the username key was found, else return a list of dictionaries containing
        the blog posts.
        """
        rows = Database.find(cls.collection, {"username": username}).sort(
            "date", pymongo.DESCENDING
        )
        posts = [Post(**row).json() for row in rows]
        return posts

    @classmethod
    def get_by_id(cls, _id) -> Dict:
        """
        Find the username in the database, and return None if no user with
        the username key was found, else return a list of dictionaries containing
        the blog posts.
        """
        row = Database.find_one(cls.collection, {"_id": _id})
        return row

    @classmethod
    def delete_post(cls, _id) -> None:
        """
        Delete one post by it's _id
        """
        Database.remove(cls.collection, {"_id": _id})
