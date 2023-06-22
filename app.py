from flask import Flask, render_template, request, flash, url_for, session, abort, redirect

app = Flask(__name__)

menu = [{"name": "Installation", "url": "install-flask"},
        {"name": "First application", "url": "first-app"},
        {"name": "Feedback", "url": "contact"}]

app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

@app.route('/')
def index():
    return render_template('index.html', menu=menu)



@app.route('/about')
def about():
    return render_template('about.html', title="About the site", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)
    return f'User profile: {username}'


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title="Authorization", menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found', menu=menu), 404


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash("The message has been sent", category='success')
        else:
            flash("Send error", category='error')

    return render_template('contact.html', title="Feedback", menu=menu)


if __name__ == "__main__":
    app.run(debug=True,
            use_reloader=False,
            )
