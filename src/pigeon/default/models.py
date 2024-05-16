import pigeon.database as db


class Metadata(db.Model):
    """
    Model containing metadata about Models in database
    """
    __tablename__ = '_metadata'
    table = db.Field(db.Text, primary_key=True)
    name = db.Field(db.Text, primary_key=True)
    type = db.Field(db.Text)
    autoincrement = db.Field(db.Text)
    default = db.Field(db.Text)
    nullable = db.Field(db.Boolean)
    primary_key = db.Field(db.Boolean)
    server_default = db.Field(db.Text)
    server_onupdate = db.Field(db.Text)
    unique = db.Field(db.Boolean)
    system = db.Field(db.Text)


class User(db.Model):
    """
    Default User Model for database
    """
    user_id = db.Field(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Field(db.String(16), nullable=False)
    email_address = db.Field(db.String(60))
    email_address_2 = db.Field(db.String(15))
    nickname = db.Field(db.String(50), nullable=True)
