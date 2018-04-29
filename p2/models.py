from datetime import datetime
import views


class User(views.db.Model):
    __tablename__ = "users"
    username = views.db.Column('username', views.db.String(20), primary_key=True)
    password = views.db.Column('pwd', views.db.String(20))
    email = views.db.Column('email', views.db.String(50), unique=True, index=True)
    admin = 1

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def is_admin(self):
        return self.admin == 0

    def __repr__(self):
        return '<User %r>' % self.username


class Post(views.db.Model):
    __tablename__ = "posts"
    post_id = views.db.Column('post_id', views.db.Integer, primary_key=True)
    username = views.db.Column('username', views.db.String(20), views.db.ForeignKey('users.username'), nullable=False)
    user = views.db.relationship('User')
    create_time = views.db.Column('create_time', views.db.DateTime)
    modify_time = views.db.Column('modify_time', views.db.DateTime)
    content = views.db.Column('content', views.db.String(500))

    def modify(self, content):
        self.content = content
        self.modify_time = datetime.utcnow()

    def __repr__(self):
        return '<Post %r>' % self.post_id
