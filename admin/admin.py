python
from flask import Flask, render_template, request, redirect, url_for, session

from werkzeug.utils import secure_filename

import os
import requests
import base64
import uuid


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
# GITHUB SETTINGS
# =========================================

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_OWNER = "aaravtyagi057-lab"
GITHUB_REPO = "AaravVerse"
GITHUB_BRANCH = "main"


# =========================================
# CORS
# =========================================

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = (
        "https://aaravtyagi057-lab.github.io"
    )
    return response


# =========================================
# ADMIN LOGIN
# =========================================

USERNAME = "aarav"
PASSWORD = "090108"


# =========================================
# ADMIN LOGIN ROUTES
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


@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("dashboard.html")


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

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================
# UPLOAD FILE TO GITHUB
# =========================================

def upload_to_github(file, github_path):

    file_content = file.read()

    encoded_content = base64.b64encode(
        file_content
    ).decode("utf-8")

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/contents/"
        f"{github_path}"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "message": f"Upload {github_path}",
        "content": encoded_content,
        "branch": GITHUB_BRANCH
    }

    response = requests.put(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    return response


# =========================================
# UPLOAD PHOTO
# =========================================

@app.route("/upload-photo", methods=["POST"])
def upload_photo():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    subject = request.form.get("subject")
    content_type = request.form.get("content_type")
    chapter = request.form.get("chapter")

    if not subject or not content_type:
        return "Please select subject and content type!"

    files = request.files.getlist("photo")

    if not files:
        return "No photo selected!"

    # Notes & Important Questions = chapter-wise

    if content_type in ["notes", "important-questions"]:

        if not chapter:
            return "Please select a chapter!"

    # Homework & Important = direct folder

    elif content_type in ["homework", "important"]:

        chapter = None

    else:

        return "Invalid content type!"

    uploaded_count = 0

    for file in files:

        if file and file.filename != "":

            if allowed_file(file.filename):

                extension = file.filename.rsplit(
                    ".", 1
                )[1].lower()

                # Unique filename

                filename = f"{uuid.uuid4().hex}.{extension}"

                # Create GitHub path

                if content_type in [
                    "notes",
                    "important-questions"
                ]:

                    github_path = (
                        f"static/uploads/"
                        f"{subject}/"
                        f"{content_type}/"
                        f"chapter-{chapter}/"
                        f"{filename}"
                    )

                else:

                    github_path = (
                        f"static/uploads/"
                        f"{subject}/"
                        f"{content_type}/"
                        f"{filename}"
                    )

                # Upload to GitHub

                response = upload_to_github(
                    file,
                    github_path
                )

                if response.status_code in [200, 201]:

                    uploaded_count += 1

                else:

                    return (
                        f"GitHub upload failed! "
                        f"Status: {response.status_code}"
                    )

    if uploaded_count == 0:
        return "No valid photos were uploaded!"

    return redirect(url_for("dashboard"))


# =========================================
# GET CHAPTER-WISE CONTENT FROM GITHUB
# =========================================

@app.route(
    "/api/notes/<subject>/<content_type>/<chapter>"
)
def get_notes(subject, content_type, chapter):

    folder_path = (
        f"static/uploads/"
        f"{subject}/"
        f"{content_type}/"
        f"chapter-{chapter}"
    )

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/contents/"
        f"{folder_path}"
    )

    # AUTHENTICATED REQUEST
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(
        url,
        headers=headers,
        params={"ref": GITHUB_BRANCH},
        timeout=30
    )

    if response.status_code != 200:

        return {
            "error": "GitHub API failed",
            "status": response.status_code,
            "message": response.text
        }, response.status_code

    files = []

    for item in response.json():

        if item.get("type") == "file":

            filename = item.get("name", "")

            if allowed_file(filename):

                raw_url = (
                    f"https://raw.githubusercontent.com/"
                    f"{GITHUB_OWNER}/{GITHUB_REPO}/"
                    f"{GITHUB_BRANCH}/"
                    f"{folder_path}/{filename}"
                )

                files.append(raw_url)

    return files


# =========================================
# GET HOMEWORK / IMPORTANT TOPICS FROM GITHUB
# =========================================

@app.route(
    "/api/content/<subject>/<content_type>"
)
def get_content(subject, content_type):

    # Only allow these two

    if content_type not in ["homework", "important"]:

        return []

    folder_path = (
        f"static/uploads/"
        f"{subject}/"
        f"{content_type}"
    )

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/contents/"
        f"{folder_path}"
    )

    # AUTHENTICATED REQUEST
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(
        url,
        headers=headers,
        params={"ref": GITHUB_BRANCH},
        timeout=30
    )

    if response.status_code != 200:

        return {
            "error": "GitHub API failed",
            "status": response.status_code,
            "message": response.text
        }, response.status_code

    files = []

    for item in response.json():

        if item.get("type") == "file":

            filename = item.get("name", "")

            if allowed_file(filename):

                raw_url = (
                    f"https://raw.githubusercontent.com/"
                    f"{GITHUB_OWNER}/{GITHUB_REPO}/"
                    f"{GITHUB_BRANCH}/"
                    f"{folder_path}/{filename}"
                )

                files.append(raw_url)

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
