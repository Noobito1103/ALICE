from flask import Blueprint, flash, render_template, redirect, request, url_for
view = Blueprint('view',__name__)

# @view.route('/')
# def startpage():
#     return render_template('startpage.html')

#Username = "admin"
#Password = "admin"

@view.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash("Invalid credentials")
        else:
            return redirect(url_for('view.home'))
    return render_template('login.html', error = error)

@view.route('/home')
def home():
    error = None
    return render_template('home.html',error = error)

@view.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    return render_template('signup.html', error = error)

@view.route('/play')
def play():
    error = None
    return render_template('play.html', error = error)

@view.route('/play/singleplayer')
def singleplayer():
    error = None
    return render_template('singleplayer.html', error = error)

@view.route('/play/multiplayer')
def multiplayer():
    error = None
    return render_template('multiplayer.html', error = error)

