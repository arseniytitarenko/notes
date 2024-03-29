from flask import Flask, render_template, redirect, abort, url_for, request
from forms import AddArticle, EditArticle
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'q23mroe0ewfaeq9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    date = db.Column(db.String)
    content = db.Column(db.String)
    source = db.Column(db.String)


app.app_context().push()
db.create_all()


@app.route('/')
def notes():
    sort = request.args.get('sort', 'id')
    direction = request.args.get('direction', 'asc')
    filter_author = request.args.get('author', '')
    filter_date = request.args.get('date', '')
    filter_resource = request.args.get('resource', '')
    filter_text = request.args.get('text', '')

    query = Article.query

    if filter_author or filter_date or filter_resource or filter_text:
        query = query.filter(
            (Article.author.ilike(f'%{filter_author}%')) if filter_author else True,
            (Article.date.ilike(f'%{filter_date}%')) if filter_date else True,
            (Article.source.ilike(f'%{filter_resource}%')) if filter_resource else True,
            (Article.content.ilike(f'%{filter_text}%')) if filter_text else True
        )

    if sort in ['id', 'title', 'author', 'date', 'content', 'source']:
        if direction == 'asc':
            query = query.order_by(getattr(Article, sort).asc())
        else:
            query = query.order_by(getattr(Article, sort).desc())

    arts = query.all()
    return render_template('notes.html', notes=arts, filter_author=filter_author, filter_date=filter_date,
                           filter_resource=filter_resource, filter_text=filter_text)

@app.route("/add", methods=["POST", "GET"])
def add():
    form = AddArticle()
    if form.validate_on_submit():
        new_arcticle = Article(title=form.title.data, author=form.author.data,
                               date=form.date.data, content=form.content.data, source=form.source.data)
        db.session.add(new_arcticle)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("add_article.html", form=form,
                                   message="Возникла ошибка, попробуйте ещё раз:")
        finally:
            db.session.close()
        return redirect("/")
    return render_template("add_article.html", form=form)


@app.route("/note/<int:id>", methods=["GET"])
def note(id):
    note = Article.query.get_or_404(id)
    lines = note.content.split("\n")
    return render_template('note.html', note=note, lines=lines)

@app.route("/delete/<int:id>")
def delete(id):
    art = Article.query.get(id)
    if art is None:
        abort(404, description="Такой статьи не существует")
    db.session.delete(art)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('notes'))

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    note = Article.query.get_or_404(id)
    form = EditArticle()
    if form.validate_on_submit():
        new_arcticle = Article(title=form.title.data, author=form.author.data,
                               date=form.date.data, content=form.content.data, source=form.source.data)
        db.session.add(new_arcticle)
        db.session.commit()
    db.session.delete(note)
    db.session.commit()
    form.title.data = note.title
    form.author.data = note.author
    form.source.data = note.source
    form.content.data = note.content
    return render_template("edit_article.html", form=form)


if __name__ == '__main__':
    app.run()
