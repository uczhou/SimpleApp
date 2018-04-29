from flask import Flask, url_for, flash, redirect, render_template, request, session, abort, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import models
from datetime import datetime
import sys

# flask app
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
@app.route('/index')
def index():
    '''
    This function is to return the home page.
    :return:
    '''
    return success_msg(200, 'Welcome, please login first.')


@app.route('/list', methods=['GET'])
@login_required
def list_jobs():
    '''
    This function is to list the posts. User login required.
    :return:
    '''
    posts = models.Post.query.order_by(models.Post.modify_time).all()
    res = dict()
    if posts is None:
        return error_msg(400, 'Bad Request')

    res['code'] = 201
    res['content'] = []
    for post in posts:
        username = post.username
        content = post.content
        post_id = post.post_id
        res['content'].append({'post_id': post_id, 'user': username, 'content': content})
    return jsonify(res)


@app.route('/search', methods=['POST'])
@login_required
def search_job():
    '''
    This function is to search the posts by username or post_id. User login required.
    :return:
    '''
    form = request.form
    username = form.get('username')
    post_id = form.get('post_id')

    if post_id is not None:
        try:
            post = models.Post.query.get(post_id)
            if post is None:
                return error_msg(400, 'Bad Request')
            res = dict()
            res['code'] = 200
            res['content'] = dict()
            res['content']['post_id'] = post_id
            res['content']['username'] = post.username
            res['content']['content'] = post.content
            return jsonify(res)
        except:
            return error_msg(400, 'Bad Request')
    elif username is not None:
        try:
            posts = models.Post.query.filter_by(username=username).all()
            if posts is None:
                return error_msg(400, 'Bad Request')
            res = dict()
            res['code'] = 200
            res['content'] = []
            for post in posts:
                tmp = dict()
                tmp['post_id'] = post.post_id
                tmp['username'] = post.username
                tmp['content'] = post.content
                res['content'].append(tmp)
            return jsonify(res)
        except:
            return error_msg(400, 'Bad Request')


@app.route('/delete', methods=['POST'])
@login_required
def delete_job():
    '''
    This function is to delete the post. User permission will be checked first.
    :return:
    '''
    form = request.form
    post_id = form.get('post_id')
    try:
        post = models.Post.query.get(post_id)
        if post is None:
            return error_msg(400, 'Bad Request')
        username = post.username
        if current_user.is_admin() or username == current_user.username:
            db.session.delete(post)
            db.session.commit()
            return success_msg(200, 'Delete post successfully.')
        else:
            return error_msg(401, 'Permission denied')
    except:
        return error_msg(400, 'Bad Request')


@app.route("/update", methods=['POST'])
@login_required
def update_job():
    '''
    This function is to update the post. User permission will be checked first.
    :return:
    '''
    form = request.form
    post_id = form.get('post_id')
    try:
        post = models.Post.query.get(post_id)
        if post is None:
            return error_msg(400, 'Bad Request')
        username = post.username
        if current_user.is_admin() or username == current_user.username:
            post.content = form.get('content')
            post.modify_time = datetime.utcnow()
            db.session.merge(post)
            db.session.commit()
            return success_msg(200, 'Update post successfully.')
        else:
            return error_msg(401, 'Permission denied')
    except:
        return error_msg(400, 'Bad Request')


@app.route("/add", methods=['POST'])
@login_required
def add_job():
    '''
    This function is to add post. User login required.
    :return:
    '''
    try:
        form = request.form
        post = models.Post(username=current_user.username, content=form.get('content'),
                           create_time=datetime.utcnow(), modify_time=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return success_msg(200, 'Add post successfully.')
    except:
        return error_msg(400, 'Bad Request')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This function is to login user.
    :return:
    '''
    if request.method == 'GET':
        res = dict()
        res['code'] = 201
        res['login format'] = ['username = yourusername', 'password = yourpassword']
        return jsonify(res)

    username = request.form['username']
    password = request.form['password']

    registered_user = models.User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return error_msg(400, 'Username or Password is invalid')
    login_user(registered_user, remember=True)
    return success_msg(200, 'Welcome {}'.format(username))


@app.route('/logout')
def logout():
    '''
    This function is to logout user.
    :return:
    '''
    logout_user()
    return success_msg(200, 'You have successfully logout.')


@login_manager.user_loader
def user_loader(user_id):
    try:
        return models.User.query.get(user_id)
    except:
        return None


def error_msg(code, msg):
    '''
    This is a helper function to return error page.
    :param code: python int, status code
    :param msg: python str, error message
    :return: json message
    '''
    res = dict()
    res['code'] = code
    res['error'] = msg
    return jsonify(res)


def success_msg(code, msg):
    '''
    This is a helper function to return success page.
    :param code: python int, status code
    :param msg: python str, success message.
    :return: json message
    '''
    res = dict()
    res['code'] = code
    res['content'] = msg
    return jsonify(res)


if __name__ == '__main__':
    port = 5000
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)
