from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import yt_to_mp3, transcription, summarize, login_required, embed

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.secret_key = "f7ad503648cf4b68b9ca7334d8ff8596"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

db = SQL("sqlite:///database.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # Set defualt value for variables
    services = ("Summarize", "Transcribe", "Convert youtube to mp3")
    transcript, summary, filepath = "", "", ""

    if request.method == "POST":

        # Get url
        url = request.form.get("url")
        if not url:
            flash("Please provide a youtube url")
            return render_template("index.html", services=services)
        
        # Get service type
        type = request.form.get("service")
        if not type or type not in services:
            flash("Please select service type you want to use")
            return render_template("index.html", services=services)
        
        id = session['user_id']
        date = datetime.datetime.now()
        
        # first insert id to create number
        number = db.execute("INSERT INTO activities (user_id, youtube_url, date, type) VALUES (?, ?, ?, ?)", id, url ,date, type)
        
        # yt to mp3
        try:
            title = yt_to_mp3(link=url, name=number, id=id)
        except:
            flash("Please provide an valid youtube url")
            return redirect("/")
        
        filepath = f"static/files/{id}/{number}.mp3"

        # insert title and filepath to the row
        db.execute("UPDATE activities SET title = ?, mp3_filepath = ? WHERE user_id = ? AND number = ?", title, filepath, id, number)

        if type != "Convert youtube to mp3":
            # Transcript mp3 file
            transcript = transcription(filepath)

            # Insert transcript to the row
            db.execute("UPDATE activities SET transcript = ? WHERE user_id = ? AND number = ?", transcript, id, number)

            if type != "Transcribe":
                # summarize
                summary = summarize(transcript)

                # Insert summary text into the row
                db.execute("UPDATE activities SET summary = ? WHERE user_id = ? AND number = ?", summary, id, number)

       
        return render_template("index.html", url=embed(url), transcript=transcript, summary=summary, mp3=filepath, services=services)
    else:
        print(session['user_id'])
        return render_template("index.html", services=services)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "Invalide"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "Must provide password"

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return "Invalide"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Get username and password
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return "invalide"

        if password != confirmation:
            return "invalide"

        # Quary database for usernames
        usernames = db.execute("SELECT username FROM users")
        usernames = [i['username'] for i in usernames]

        # Ensure username have not registered before
        if username in usernames:
            return"invalide"

        # Insert new username and password in the user dataset.
        new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Log User In
        session["user_id"] = new_user

        return redirect("/")
    else:
        return render_template("register.html")
    
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/history")
@login_required
def history():
    activities = db.execute("SELECT * FROM activities WHERE user_id = ?", session['user_id'])
    return render_template("history.html", activities=activities)

@app.route("/view", methods=["GET", "POST"])
@login_required
def view():

    id = session['user_id']

    number = int(request.args.get("number", "world"))
    id_number = [i['number'] for i in db.execute("SELECT number FROM activities WHERE user_id = ?", id)]

    # Show error when user not request their number
    if number in id_number:
        # Get row
        row = db.execute("SELECT * FROM activities WHERE user_id = ? AND number = ?", id, number)[0]

        # Render
        return render_template("view.html", url=embed(row['youtube_url']), transcript=row['transcript'], summary=row['summary'], mp3=row['mp3_filepath'])
    else:
        return "error"

@app.route("/delete")
@login_required
def delete():

    id = session['user_id']

    number = int(request.args.get("number", 0))
    id_number = [i['number'] for i in db.execute("SELECT number FROM activities WHERE user_id = ?", id)]

    # Show error when user not request their number
    if number in id_number:
        
        # Delete the row
        db.execute("DELETE FROM activities WHERE number = ?", number)

        # Render history
        activities = db.execute("SELECT * FROM activities WHERE user_id = ?", session['user_id'])
        return render_template("history.html", activities=activities)
    else:
        return "error"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5002)
