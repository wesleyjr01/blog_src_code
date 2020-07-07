from flask import Flask, render_template, request, session, flash, redirect, url_for
import os
from dotenv import load_dotenv

from helper import apology, login_required, get_admin
from werkzeug.security import generate_password_hash
from models.user import User
from models.post import Post


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(64)

# Custom filter
app.jinja_env.filters["get_admin"] = get_admin


@app.route("/")
def index():
    admin_usr = os.environ.get("ADMIN_USR")
    posts = Post.get_posts(username=admin_usr)
    return render_template("home.html", posts=posts)


@app.route("/professional")
def prf():
    return render_template("professional.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<string:post_id>/<string:lang>")
def blog_post(post_id, lang):
    post = Post.get_by_id(_id=post_id)
    return render_template("post.html", post=post, lang=lang)


@app.route("/delete/<string:post_id>")
@login_required
def delete_post(post_id):
    admin_usr = os.environ.get("ADMIN_USR")
    if session["username"] == admin_usr:
        Post.delete_post(_id=post_id)
    else:
        return apology("Sorry, only users can delete posts.")
    return redirect(url_for('index'))


@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    if request.method == "POST":
        title = request.form.get("title")
        en_raw_text = request.form.get("content")
        user = User.get_user(session["username"])

        new_post = Post(title, en_raw_text, user["username"], user["_id"])
        check_result, message = new_post.valid_post()
        if check_result:
            new_post.insert_to_db()
            flash(message)
            return redirect(url_for('index'))
        else:
            return apology(message)

    else:
        return render_template("write.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        pwd_hash = generate_password_hash(password)

        user = User(username, pwd_hash)
        check_result, message = user.register_valid(confirmation)
        if check_result:
            user.insert_to_db()
            session["username"] = username
            flash(message)
            return redirect(url_for('index'))
        else:
            return apology(message)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any users
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        pwd_hash = generate_password_hash(password)

        user = User(username, pwd_hash)
        check_result, message = user.login_valid(password)
        if check_result:
            session["username"] = username
            flash(message)
            return redirect(url_for('index'))
        else:
            return apology(message)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any users
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
