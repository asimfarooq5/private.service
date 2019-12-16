from flask import Flask, render_template, request, session, redirect, make_response
from flask_admin.menu import MenuLink
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
db.init_app(app)
api = Api(app)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.String(100), nullable=False)


class SendContent(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('number', type=str, help='Number', required=False)
        parser.add_argument('content', type=str, help='Content', required=True)
        parser.add_argument('datetime', type=str, help='Date & Time', required=False)
        args = parser.parse_args(strict=True)
        custom_args = {}
        for k, v in args.items():
            if v:
                custom_args.update({k: v})

        content = Content(**custom_args)
        db.session.add(content)
        db.session.commit()

        return "OK", 200


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'private':
        session['logged_in'] = True
        resp = make_response(redirect('/content'))
        resp.set_cookie('username', request.form['username'])
        return redirect('/content')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('login.html')


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if session.get('logged_in'):
            if request.cookies.get('username'):
                return redirect('/content')
        if not session.get('logged_in'):
            return render_template('login.html')
        return super().index()


class ContentModelView(ModelView):
    can_edit = False
    can_create = False
    column_list = ('content',)

    def is_accessible(self):
        if session.get('logged_out'):
            return False
        if session.get('logged_in'):
            return True


admin = admin.Admin(app, name='Home', index_view=MyAdminIndexView(name=' '), template_mode='bootstrap3', url='/admin')
admin.add_view(ContentModelView(Content, db.session, url='/content', ))
api.add_resource(SendContent, '/api/content/')
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
