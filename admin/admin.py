from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# =========================================
# SECRET KEY
# =========================================

app.secret_key = "my-school-portal-secret-key"


# =========================================
# CORS
# =========================================

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000"
    return response


# =========================================
# ADMIN LOGIN
# =========================================

USERNAME = "aarav"
PASSWORD = "090108"


# =========================================
# PHOTO UPLOAD SETTINGS
# =========================================

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================
# LOGIN
# =========================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Wrong username or password!"
        )

    return render_template("login.html")


# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# =========================================
# UPLOAD PHOTO
# =========================================

@app.route("/upload-photo", methods=["POST"])
def upload_photo():

    # Check login
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Get selections
    subject = request.form.get("subject")
    content_type = request.form.get("content_type")
    chapter = request.form.get("chapter")

    # =====================================
    # CHECK BASIC SELECTIONS
    # =====================================

    if not subject or not content_type:
        return "Please select subject and content type!"

    # =====================================
    # GET MULTIPLE PHOTOS
    # =====================================

    files = request.files.getlist("photo")

    if not files:
        return "No photo selected!"

    # =====================================
    # CHAPTER RULE
    # =====================================

    # Notes + Important Questions
    # require chapter

    if content_type in ["notes", "important-questions"]:

        if not chapter:
            return "Please select a chapter!"

    # Homework + Important
    # do NOT require chapter

    elif content_type in ["homework", "important"]:

        chapter = None

    else:

        return "Invalid content type!"

    # =====================================
    # CREATE UPLOAD PATH
    # =====================================

    if content_type in ["notes", "important-questions"]:

        upload_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            subject,
            content_type,
            f"chapter-{chapter}"
        )

    else:

        upload_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            subject,
            content_type
        )

    # Create folders automatically
    os.makedirs(upload_path, exist_ok=True)

    # =====================================
    # SAVE ALL PHOTOS
    # =====================================

    uploaded_count = 0

    for file in files:

        if file and file.filename != "":

            if allowed_file(file.filename):

                filename = secure_filename(file.filename)

                # Avoid empty filename
                if filename:

                    file.save(
                        os.path.join(
                            upload_path,
                            filename
                        )
                    )

                    uploaded_count += 1

    # =====================================
    # CHECK RESULT
    # =====================================

    if uploaded_count == 0:
        return "No valid photos were uploaded!"

    # Go back to dashboard
    return redirect(url_for("dashboard"))


# =========================================
# GET CHAPTER-WISE CONTENT
# =========================================

@app.route("/api/notes/<subject>/<content_type>/<chapter>")
def get_notes(subject, content_type, chapter):

    folder = os.path.join(
        app.config["UPLOAD_FOLDER"],
        subject,
        content_type,
        f"chapter-{chapter}"
    )

    if not os.path.exists(folder):
        return []

    files = []

    for filename in os.listdir(folder):

        if allowed_file(filename):

            files.append(
                f"/static/uploads/"
                f"{subject}/"
                f"{content_type}/"
                f"chapter-{chapter}/"
                f"{filename}"
            )

    return files


# =========================================
# GET HOMEWORK / IMPORTANT TOPICS
# =========================================

@app.route("/api/content/<subject>/<content_type>")
def get_content(subject, content_type):

    # Only allow these two
    if content_type not in ["homework", "important"]:
        return []

    folder = os.path.join(
        app.config["UPLOAD_FOLDER"],
        subject,
        content_type
    )

    if not os.path.exists(folder):
        return []

    files = []

    for filename in os.listdir(folder):

        if allowed_file(filename):

            files.append(
                f"/static/uploads/"
                f"{subject}/"
                f"{content_type}/"
                f"{filename}"
            )

    return files


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================
# START FLASK SERVER
# =========================================

if __name__ == "__main__":

    app.run(debug=True)