from flask import Flask
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
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
    number = db.Column(db.String(100), nullable=True)
    content = db.Column(db.String(10000), nullable=True)
    date = db.Column(db.String(100), nullable=True)


class SendContent(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('number', type=str, help='Number', required=False)
        parser.add_argument('content', type=str, help='Content', required=True)
        parser.add_argument('datetime', type=str, help='Date & Time', required=True)
        args = parser.parse_args(strict=True)
        custom_args = {}
        for k, v in args.items():
            if v:
                custom_args.update({k: v})

        content = Content(**custom_args)
        db.session.add(content)
        db.session.commit()

        return "OK", 200


class ContentModelView(ModelView):
    can_edit = False
    can_create = True
    column_list = ('content',)


admin = Admin(app, name='Sms', template_mode='bootstrap3')
admin.add_view(ContentModelView(Content, db.session, url='/content', ))

api.add_resource(SendContent, '/api/content/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
