from pigeon.shortcuts import db

class Bird(db.Model):
    name = db.Field(str, default="unknown")
    age = db.Field(int, default=0)
    species = db.Field(str, default="unknown")