from flask import Flask, render_template, request

app = Flask(__name__)

menu = [{"name": "Installation", "url": "install-flask"},
        {"name": "First application", "url": "first-app"},
        {"name": "Feedback", "url": "contact"}]


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title="About the site", menu=menu)


@app.route("/profile/<string:user_name>/<string:path>")
def profile(user_name, path):
    return f"User: {user_name}, path: {path}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        x = request.form['username']
    return render_template('contact.html', title="Feedback", menu=menu)


if __name__ == "__main__":
    app.run(debug=True,
            use_reloader=False,
            )
