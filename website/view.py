from flask import Blueprint, render_template, redirect, request, url_for, session
from .database import User, GameData, ProfileData, Feedback
from . import db
import base64
from datetime import datetime

view = Blueprint('view',__name__)
log_messages = []


def currentTime():
    current_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    return current_time


@view.route('/')
def index():
    return redirect(url_for('view.login'))


@view.route('/admin', methods =['GET', 'POST'])
def admin():
    if 'admin' in session:
        adminUrl = url_for('view.admin')
        message = request.args.get('error', None)
        logs = log_messages
        data = User.query.all()
        feedback = Feedback.query.all()
        return render_template('admin.html', data = data, feedback = feedback, logs = logs, message = message, adminURL = adminUrl)
    else:
        return redirect(url_for('view.login'))


@view.route('/login', methods=['GET', 'POST'])
def login():
    invalidData = False
    current_time = currentTime()

    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "admin123":
            session['admin'] = 'admin'
            return redirect(url_for('view.admin'))
        
        else:
            username = request.form['username']
            password = request.form['password']

            checkUser = User.query.filter_by(username = username, password = password).first()
            
            if checkUser:
                session['user_id'] = checkUser._id
                log_messages.append(f"[{current_time}] User: {checkUser.username}, logged in")
                return redirect(url_for('view.home'))
            else:
                invalidData = True

    return render_template("login.html", boolean = True, invalidData = invalidData)      


@view.route('/play/lattice/<difficulty>')
def lattice(difficulty):
    return render_template('lattice.html', difficulty = difficulty)


@view.route('/play/operations/<type>/<difficulty>')
def operations(type, difficulty):
    return render_template('math.html', type = type, difficulty = difficulty)


@view.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        get_username = User.query.filter_by(_id = user_id).first()
        profileData = ProfileData.query.all()
        gameData = GameData.query.filter_by(userID = user_id).first()
        pics = []

        if get_username:
            if gameData:
                latScore = gameData.latScore
                addScore = gameData.addScore
                subScore = gameData.subScore
                mulScore = gameData.mulScore
                divScore = gameData.divScore
                mixScore = gameData.mixScore

            if profileData:
                for line in profileData:
                    if not line.profilePic == None:
                        img = base64.b64encode(line.profilePic).decode('utf-8')
                        pics.append(img)
        
            return render_template('home.html', user = get_username.username, data = profileData, img = pics, latScore = latScore, addScore = addScore, subScore = subScore, mulScore = mulScore, divScore = divScore, mixScore = mixScore)
        else:
            return redirect(url_for('view.login'))  
    else:
        return redirect(url_for('view.login'))
    

@view.route('/signup', methods =['GET', 'POST'])
def signup():
    current_time = currentTime()
    message = None
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        checkUser = User.query.filter_by(username = username).first()
        checkEmail = User.query.filter_by(email = email).first()

        if checkUser:
            message = "Username already taken"

        elif checkEmail:
            message = "Email is already registered"

        else:
            new_user = User(username = username, email = email, password = password)
            db.session.add(new_user)
            db.session.commit()

            new_user_id = new_user._id

            new_profile = ProfileData(userID = new_user_id, bannerColor = "#f1f1f1", usernameColor = "#000000", bioColor = "#000000", gameColor = "#000000")
            db.session.add(new_profile)
            db.session.commit()

            new_data = GameData(userID = new_user_id, latScore = 0, addScore = 0, subScore = 0, mulScore = 0, divScore = 0, mixScore = 0,  pastScore = 0, topScore = 0, totalScore = 0, rank = "Unranked")
            db.session.add(new_data)
            db.session.commit()

            log_messages.append(f"[{current_time}] New account: {new_user.username} has been created")
            message = "Account Successfully Created"

    return render_template('signup.html', message = message)


@view.route('/profile', methods = ['GET', 'POST'])
def profile():
    profileUrl = url_for('view.profile')
    username = None
    message = request.args.get('message', None)
    if 'user_id' in session:
        user_id = session['user_id']
        checkUser= User.query.filter_by(_id = user_id).first()
        profile_data = ProfileData.query.filter_by(userID = user_id).first()
        game_data = GameData.query.filter_by(userID = user_id).first()

        if checkUser:
            username = checkUser.username
            get_bio = profile_data.profileBio
            get_banColor = profile_data.bannerColor
            get_userColor = profile_data.usernameColor
            get_bioColor = profile_data.bioColor
            get_gameColor = profile_data.gameColor
            get_topScore = game_data.topScore
            get_pastScore = game_data.pastScore
            get_totalScore = game_data.totalScore
            if not profile_data.profilePic == None:
                get_pic = base64.b64encode(profile_data.profilePic).decode('utf-8')
            else: 
                get_pic = ""
            return render_template('profile.html', user = username, image_url = get_pic, bio = get_bio, bannerColor = get_banColor, userColor = get_userColor, bioColor = get_bioColor, gameColor = get_gameColor, top_score = get_topScore, past_score = get_pastScore, total_score = get_totalScore, message = message , profileURL = profileUrl)
        
        else:
            return redirect(url_for('view.login'))
    else:
        return redirect(url_for('view.login'))
    

@view.route('/play')
def play():
    if 'user_id' in session:
        user_id = session['user_id']
        checkUser= User.query.filter_by(_id = user_id).first()
        if checkUser:
            return render_template('play.html')
        else:
            return redirect(url_for('view.login'))
    else:
        return redirect(url_for('view.login'))
    

@view.route('/tutorial')
def tutorial():
    if 'user_id' in session:
        user_id = session['user_id']
        checkUser= User.query.filter_by(_id = user_id).first()
        if checkUser:
            return render_template('tutorial.html')
        else:
            return redirect(url_for('view.login'))
    else:
        return redirect(url_for('view.login'))
    

@view.route('/leaderboards')
def leaderboards():
    if 'user_id' in session:
        user_id = session['user_id']
        checkUser= User.query.filter_by(_id = user_id).first()
        totalScore = GameData.query.order_by(GameData.totalScore.desc()).limit(10).all()
        latScore = GameData.query.order_by(GameData.latScore.desc()).limit(10).all()
        addScore = GameData.query.order_by(GameData.addScore.desc()).limit(10).all()
        mulScore = GameData.query.order_by(GameData.mulScore.desc()).limit(10).all()
        subScore = GameData.query.order_by(GameData.subScore.desc()).limit(10).all()
        divScore = GameData.query.order_by(GameData.divScore.desc()).limit(10).all()
        mixScore = GameData.query.order_by(GameData.mixScore.desc()).limit(10).all()

        if checkUser:
            return render_template('leaderboards.html', totalScore = totalScore, latScore = latScore, addScore = addScore, mulScore = mulScore, subScore = subScore, divScore = divScore, mixScore = mixScore)
        else:
            return redirect(url_for('view.login'))
    else:
        return redirect(url_for('view.login'))
    

@view.route('/logout')
def logout():
    current_time = currentTime()
    if 'admin' in session:
        session.pop('admin', None)

    if 'user_id' in session:
        user_id = session['user_id']
        checkUser= User.query.filter_by(_id = user_id).first()
        log_messages.append(f"[{current_time}] User: {checkUser.username}, logged out")
        session.pop('user_id', None)

    return redirect(url_for('view.login'))


@view.route('/add_latscore', methods = ['POST'])
def add_latscore():
    current_time = currentTime()
    score_data = request.get_json()
    score_value = score_data['score']

    if 'user_id' in session:
        user_id = session['user_id']

        checkUserData = GameData.query.filter_by(userID = user_id).first()

        if checkUserData:
            if score_value:
                checkUserData.pastScore = score_value

                if score_value > checkUserData.topScore:
                    checkUserData.topScore = score_value
                
                checkUserData.latScore += score_value
            
            checkUserData.totalScore += score_value

            if checkUserData.totalScore < 2000:
                checkUserData.rank = "Unranked";
            elif checkUserData.totalScore < 3000:
                checkUserData.rank = "Beginner";
            elif checkUserData.totalScore < 5000:
                checkUserData.rank = "Amateur";
            elif checkUserData.totalScore < 8000:
                checkUserData.rank = "Expert";
            elif checkUserData.totalScore < 10000:
                checkUserData.rank = "Master";
            
            log_messages.append(f"[{current_time}] User: {checkUserData.user.username}, scored {score_value} points in lattice")
            db.session.commit()

    return "Successfully added to Database"


@view.route('/add_opscore', methods = ['POST'])
def add_opscore():
    current_time = currentTime()
    score_data = request.get_json()
    add_score = score_data.get('addition')
    sub_score = score_data.get('subtraction')
    mul_score = score_data.get('multiplication')
    div_score = score_data.get('division')
    mix_score = score_data.get('mixed')

    if 'user_id' in session:
        user_id = session['user_id']

        checkUserData = GameData.query.filter_by(userID = user_id).first()

        if checkUserData:
            if add_score is not None:
                checkUserData.addScore += add_score
                log_messages.append(f"[{current_time}] User: {checkUserData.user.username}, scored {add_score} points in addition")
            elif sub_score is not None:
                checkUserData.subScore += sub_score
                log_messages.append(f"[{current_time}] User: {checkUserData.user.username}, scored {sub_score} points in subtraction")
            elif mul_score is not None:
                checkUserData.mulScore += mul_score
                log_messages.append(f"[{current_time}] User: {checkUserData.user.username}, scored {mul_score} points in multiplication")
            elif div_score is not None:
                checkUserData.divScore += div_score
                log_messages.append(f"[{current_time}] User: {checkUserData.user.username}, scored {div_score} points in division")
            elif mix_score is not None:
                checkUserData.mixScore += mix_score
                log_messages.append(f"[{current_time}] User: {checkUserData.user.username}, scored {mix_score} points in mixed")

            checkUserData.totalScore = checkUserData.totalScore + checkUserData.addScore + checkUserData.subScore + checkUserData.mulScore + checkUserData.divScore + checkUserData.mixScore   

            if checkUserData.totalScore < 2000:
                checkUserData.rank = "Unranked";
            elif checkUserData.totalScore < 3000:
                checkUserData.rank = "Beginner";
            elif checkUserData.totalScore < 5000:
                checkUserData.rank = "Amateur";
            elif checkUserData.totalScore < 8000:
                checkUserData.rank = "Expert";
            elif checkUserData.totalScore < 10000:
                checkUserData.rank = "Master";
            
            db.session.commit()

    return "Successfully added to Database"


@view.route('/upload', methods ={'POST'})
def upload():
    current_time = currentTime()
    if 'user_id' in session:
        user_id = session['user_id']
        checkUser = User.query.filter_by(_id = user_id).first()
        profile_data = ProfileData.query.filter_by(userID = user_id).first()

        if checkUser:
            username = request.form['username'] 
            bio = request.form['bio']
            banner_color = request.form['bannerColor']
            username_color = request.form['usernameColor']
            bio_color = request.form['bioColor']
            game_color = request.form['gameColor']
            file = request.files['file']

            if file:
                file_content = file.read()
                profile_data.profilePic = file_content

            if User.query.filter_by(username = username).first():
                return redirect(url_for('view.profile', message = "Username is taken"))

            else:
                oldUsername = checkUser.username
                checkUser.username = username
                log_messages.append(f"[{current_time}] User: {oldUsername}, changed their username to {username}")

            profile_data.profileBio = bio

            if banner_color:
                profile_data.bannerColor = banner_color

            if username_color:
                profile_data.usernameColor = username_color

            if bio_color:
                profile_data.bioColor = bio_color

            if game_color:
                profile_data.gameColor = game_color
                
            db.session.commit()
                
    return redirect(url_for('view.profile'))


@view.route('/delete-row', methods ={'POST'})
def delete():
    current_time = currentTime()
    data = request.json
    userID = data['userID']
    user = User.query.get(userID)
    profile = ProfileData.query.filter_by(userID = userID).first()
    game = GameData.query.filter_by(userID = userID).first()

    if user:
        db.session.delete(user)
        db.session.delete(profile)
        db.session.delete(game)
        db.session.commit()
        log_messages.append(f"[{current_time}] User: {user.username}, has been deleted/banned")

    return redirect(url_for('view.admin'))


@view.route('/add_feedback', methods ={'GET', 'POST'})
def add_feedback():
    current_time = currentTime()
    if 'user_id' in session:
        user_id = session['user_id']
        checkUser = User.query.filter_by(_id = user_id).first()
        subject = request.args.get('subject')
        description = request.args.get('description')
        new_feedback = Feedback(userID = user_id, subject = subject, description = description)
        db.session.add(new_feedback)
        db.session.commit()

        log_messages.append(f"[{current_time}] User: {checkUser.username}, added a feedback")
    return "Successfully created feedback"


@view.route('/edit_user', methods ={'POST'})
def edit_user():
    current_time = currentTime()
    data = request.get_json()
    userID = data['user-id']
    username = data['username']
    email = data['email']
    password = data['password']
    checkUser = User.query.filter_by(_id = userID).first()
    oldUsername = checkUser.username
    otherRows = User.query.filter(User._id != userID).all()

    for row in otherRows:
        if row.username == username:
            return redirect(url_for('view.admin', error = "Username is taken"))
        elif row.email == email:
            return redirect(url_for('view.admin', error = "Email is already registered"))
        
    checkUser.username = username
    checkUser.email = email
    checkUser.password = password
    db.session.commit()
    log_messages.append(f"[{current_time}] User: {oldUsername}, changed their username to {username}")

    return redirect(url_for('view.admin'))
