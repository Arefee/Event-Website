from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, validators, PasswordField, DateField, TimeField, IntegerField
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_login import current_user , login_user , logout_user, login_required, login_manager

UPLOAD_FOLDER = os.path.basename('uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'events'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM event ORDER BY startdate")
    event = cur.fetchall()
    if result > 0:
        return render_template('index.html', event=event)
    else:
        msg = 'رویدادی وجود ندارد'
        return render_template('index.html', msg=msg)
    cur.close()
    return render_template('index.html')


class RegisterForm(Form):
    name = StringField('name', [validators.Length(min=1, max=20)])
    lastname = StringField('lastname', [validators.Length(min=1, max=20)])
    username = StringField('username', [validators.Length(min=4, max=20)])
    email = StringField('email', [validators.Length(min=6, max=40)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='*')])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO  user (name, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                        (name, lastname, username, email, password))

        mysql.connection.commit()
        cur.close()

        flash('عضویت با موفقیت انجام شد', 'success')
        redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM user WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if User(username, password):
                session['logged_in'] = True
                session['username'] = username


                return redirect('event')
            else:
                error = 'Invalid login'
                return render_template('login.html')
            cur.close()
        else:
            error = 'نام کاربری پیدا نشد'
            return render_template('login.html', error=error)
    return render_template('login.html')

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('شما از صفحه کاربری خارج شده اید', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard/<string:username>')
@is_logged_in
def dashboard(username):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    return render_template('dashboard.html', user=user)

@app.route('/event')
@is_logged_in
def event():
    import logging
    logging.debug('test'*10)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM event ORDER BY startdate")
    event = cur.fetchall()

    cur.execute("SELECT * FROM user where username=%s", [session['username']])
    user = cur.fetchone()

    logging.error('test', user, session, session['username'])


    if result > 0:
        return render_template('events.html', event=event, user=user)
    else:
        msg = 'رویدادی وجود ندارد'
        return render_template('events.html', msg=msg, user=user)
    cur.close()

@app.route('/show_event/<string:username>/<string:id>')
@is_logged_in
def show_event( id , username):
    import logging
    logging.error('test'*10)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s",[username])
    user = cur.fetchone()
    result = cur.execute("SELECT * FROM event WHERE eventID = %s", [id])
    event = cur.fetchone()
    return render_template('show_event.html', event=event, user=user)

@app.route('/event/notification/<string:username>')
@is_logged_in
def notification(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    cur.execute("SELECT * FROM event")
    event = cur.fetchone()
    cur.execute("SELECT * FROM ticket WHERE username = %s", [username])
    ticket = cur.fetchall()
    return render_template('notification.html', user=user, ticket=ticket, event=event)


@app.route('/show_event/<string:username>/<string:id>/request')
@is_logged_in
def request_speaker(id , username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    result = cur.execute("SELECT * FROM event WHERE eventID = %s", [id])
    event = cur.fetchone()
    return  render_template('request.html', user=user, event=event)

@app.route('/show_event/<string:username>/<string:id>/ticket')
@is_logged_in
def request_ticket(username, id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    result = cur.execute("SELECT * FROM event WHERE eventID = %s", [id])
    event = cur.fetchone()
    cur.execute("INSERT INTO ticket (username , eventID) VALUES (%s, %s)", (username, id))
    mysql.connection.commit()
    cur.close()
    return render_template('ticket_b.html', user=user, event=event)

@app.route('/show_event/<string:username>/<string:id>/booked_ticket')
@is_logged_in
def booked_ticket(username, id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    cur.execute("SELECT * FROM event WHERE eventID = %s", [id])
    event = cur.fetchone()
    cur.execute("SELECT * FROM ticket WHERE eventID = %s", [id])
    ticket = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('booked_ticket.html', user=user, event=event, ticket=ticket)


@app.route('/delete_event/<string:id>', methods=['POST'])
@is_logged_in
def delete_ticket(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ticket WHERE ticketID = %s ", [id])
    mysql.connection.commit()
    cur.close()

    flash('درخواست شرکت در روایداد رد شد ', 'success')
    return redirect(url_for('event'))

@app.route('/createEvent/<string:username>', methods=['GET', 'POST'])
@is_logged_in
def createEvent(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    form = eventForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        startdate = form.startdate.data.strftime('%Y-%m-%d')
        enddate = form.enddate.data.strftime('%Y-%m-%d')
        starttime = form.starttime.data
        endtime = form.endtime.data
        ticketprice = form.ticketprice.data
        place = form.place.data
        description = form.description.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO  event (Title, startdate, enddate, starttime, endtime, Ticketprice, place, Description) VALUES ( %s, %s, %s, %s,%s, %s, %s, %s)",
                    (title, startdate, enddate, starttime, endtime, ticketprice,  place, description))

        mysql.connection.commit()
        cur.close()

        flash('رویداد با موفقیت ثبت شد', 'success')
        redirect(url_for('event'))

    return render_template('createEvent.html', form=form , user=user)

@app.route('/editEvent/<string:username>/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def editEvent(username, id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    result = cur.execute("SELECT * FROM event WHERE eventID = %s", [id])
    event = cur.fetchone()
    form = eventForm(request.form)
    form.title.data = event['Title']
    form.startdate.data = event['startdate']
    form.enddate.data = event['enddate']
    form.starttime.data = event['starttime']
    form.endtime.data = event['endtime']
    form.ticketprice.data = event['Ticketprice']
    form.place.data = event['place']
    form.description.data = event['Description']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        starttime = request.form['starttime']
        endtime = request.form['endtime']
        ticketprice = request.form['ticketprice']
        place = request.form['place']
        description = request.form['description']
        cur = mysql.connection.cursor()
        app.logger.info(title)

        cur.execute("UPDATE event SET Title=%s, startdate=%s, enddate=%s, starttime=%s, endtime=%s, Ticketprice=%s, place=%s, Description=%s WHERE eventID=%s",
                    (title, startdate, enddate, starttime, endtime, ticketprice,  place, description, id))

        mysql.connection.commit()
        cur.close()

        flash('رویداد با موفقیت ویرایش شد', 'success')
        redirect(url_for('event'))

    return render_template('editEvent.html', form=form, user=user, event=event)

@app.route('/setting/<string:username>', methods=['GET', 'POST'])
@is_logged_in
def setting(username):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    form = RegisterForm(request.form)
    form.name.data = user['name']
    form.lastname.data = user['lastname']
    form.email.data = user['email']
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        cur = mysql.connection.cursor()
        app.logger.info(name)

        cur.execute("UPDATE user SET name=%s, lastname=%s, email=%s WHERE username=%s",
                        (name, lastname, email, username))

        mysql.connection.commit()
        cur.close()

        flash('ویرایش اطلاعات کاربری انجام شد', 'success')
        redirect(url_for('event'))
    return render_template('setting.html', form=form, user=user)

@app.route('/delete_event/<string:id>', methods=['POST'])
@is_logged_in
def delete_event(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM event WHERE eventID = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('رویداد حذف شد ', 'success')
    return redirect(url_for('event'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class eventForm(Form):
    title = StringField('title', [validators.Length(min=1, max=500)])
    startdate = DateField('startdate', format='%Y-%m-%d')
    enddate = DateField('enddate', format='%Y-%m-%d')
    starttime = TimeField('timestart')
    endtime = TimeField('endstart')
    ticketprice = IntegerField('ticketprice')
    place = StringField('place', [validators.Length(min=1)])
    # poster = StringField('poster', [validators.Length(min=1)])
    description = TextAreaField('description', [validators.Length(min=1)])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/editEvent/<string:username>/<string:id>/upload', methods=['GET', 'POST'])
@is_logged_in
def upload_poster(username, id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM event WHERE eventID = %s", [id])
    event = cur.fetchone()
    result = cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("update event SET poster=%s WHERE eventID=%s", (url_for('uploaded_file', filename=filename),id))
            mysql.connection.commit()
            cur.close()
            redirect(url_for('event'))
    return render_template('upload_poster.html', event=event , user=user)

@app.route('/setting/<string:username>/upload', methods=['GET', 'POST'])
@is_logged_in
def upload_file(username):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM user WHERE username = %s", [username])
    user = cur.fetchone()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("update user SET image=%s WHERE username=%s", (url_for('uploaded_file', filename=filename),username))
            mysql.connection.commit()
            cur.close()
            redirect(url_for('event'))
            # return redirect(url_for('uploaded_file', filename=filename))
    return render_template('uploads_profile.html', user=user)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/404')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=404)

@app.route('/403')
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', e=403)

if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)






