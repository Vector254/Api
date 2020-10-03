from app import db

class Quotes(db.Model):
    """This class represents the quotes table."""

    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    description = db.Column(db.String(255))
    author = db.Column(db.String(255))

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Quotes.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Quotes: {}>".format(self.name)