import time
from flask import redirect, render_template, send_file, request, session
from flask import flash, url_for, Blueprint
from .auth import sign_up, log_in
from .fire import add_new_post_record, get_n_posts_record

catpics = Blueprint('catpics', __name__, template_folder='templates', static_folder='statics')

@catpics.route('/')
def index():
    username: str | None = session.get('username', None)
    if not username:
        return redirect(url_for('catpics.not_logged_in'))
    posts = get_n_posts_record(10)
    return render_template('catpics/index.html', login=True, username=username, posts=posts)

@catpics.route('/not-logged-in')
def not_logged_in():
    posts = get_n_posts_record(10)
    return render_template('catpics/index.html', login=False, username='', posts=posts)

@catpics.route('/statics/<filename>')
def send_static_files(filename: str):
    return send_file(f'statics/catpics/{filename}')

@catpics.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'GET' == request.method:
        return render_template('catpics/login.html')
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if not username or not password:
            flash(message='must provide username and password', category='error')
            return render_template('catpics/login.html')

        status_code, user_id = log_in(username=username, password=password)
        if 400 == status_code:
            flash('This account does not exists. Create New Account', 'warning')
            return redirect(url_for('catpics.signup_page'))

        session['username'] = username
        session['id'] = user_id
        return redirect(url_for('catpics.index'), code=303)


@catpics.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if 'GET' == request.method:
        return render_template('catpics/signup.html')
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if not username or not password:
            flash(message='must provide username and password', category='error')
            return render_template('catpics/signup.html')

        res, status_code = sign_up(username, password)

        if 400 <= status_code:
            flash(message=res, category='error')
            return render_template('catpics/signup.html')
            
        session['username'] = username
        session['id'] = res.get('id')

        return redirect(url_for('catpics.index'), code=303)

@catpics.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if 'GET' == request.method:
        username = session.get('username')
        user_id = session.get('id')
        if not username and not user_id:
            flash(message='You have to log in first to upload', category='info')
            return redirect(url_for('catpics.login_page'))
        return render_template('catpics/upload.html')

    username: str|None = session.get('username')
    user_id: str|None = session.get('id')
    if not username and not user_id:
        flash(message='You must login to upload', category='warning')
        return redirect(url_for('catpics.login_page'))

    file = request.files.get('file')
    if not file:
        flash(message='please select a file to upload', category='warning')
        # return jsonify({'message': 'please select a file to upload'}), 400
    status_code, message = add_new_post_record(username=username, user_id=user_id, filename=file.filename, file_binary=file)
    flash(message=message, category='info')
    time.sleep(5)
    if 200 == status_code:
        return redirect(url_for('catpics.index'))
    return redirect(url_for('catpics.upload_page'))


