from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    with app.app_context():
        book_db = Book.query.all()
    return render_template("index.html",
                           books=book_db)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form.get("b_name"),
                            author=request.form.get("a_name"),
                            rating=request.form.get("rating"))
            db.session.add(new_book)
            db.session.commit()
            return redirect("/")

    else:
        return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get('id')
    book_data = db.get_or_404(Book, book_id)
    if request.method == "POST":
        new_rating = request.form.get("rating")
        try:
            new_rating = float(new_rating)
            book_data.rating = new_rating
            db.session.commit()
            return redirect("/")
        except ValueError:
            return render_template("edit.html", book=book_data, error="Invalid rating")
    return render_template("edit.html",
                           book=book_data)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    book_id = request.args.get('id')
    book_data = db.get_or_404(Book, book_id)
    if request.method == "GET":
        try:
            db.session.delete(book_data)
            db.session.commit()
            return redirect("/")
        except ValueError:
            return render_template("index.html", books=Book.query.all(), error="Deletion not successfull")


if __name__ == "__main__":
    app.run(debug=True)

