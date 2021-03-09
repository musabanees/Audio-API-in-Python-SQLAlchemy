#-------------------------- Libraries --------------------------------
from flask import Flask , request
from flask_restful import Api , Resource , abort ,reqparse,fields , marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date
from Functions import song_length , duration_positive , check_datetime , convert_list_to_string , SongParseRequest , PodcastParseRequest , AudioBookParseRequest
import argparse
import abc
# --------------------------------------------------------------------


request_condition = 'Patch'


resource_fields = {
    'id':fields.Integer,
    'Name':fields.String,
    'Duration':fields.Integer,
    'Uploadtime':fields.String,
}

resource_fields_Podcast = {
    'id':fields.Integer,
    'Name':fields.String,
    'Duration':fields.Integer,
    'Uploadtime':fields.String,
    'Host':fields.String,
    'Participant':fields.String
}

resource_fields_AudioBook = {
    'id':fields.Integer,
    'Title':fields.String,
    'Author':fields.String,
    'Narrator':fields.String,
    'Duration':fields.Integer,
    'Uploadtime':fields.String
}

# ----------------- SIINGLITON PATTERN FOR CREATING SINGLE INSTANCE OF FLASK AND DATABASE -------------------------
class CreateFlaskApp:

    __instance = None

    @staticmethod
    def getInstance():
        if CreateFlaskApp.__instance == None:
            CreateFlaskApp()
        return CreateFlaskApp.__instance

    def __init__(self):

        if CreateFlaskApp.__instance != None:
            raise Exception("Only single Object is Created..")
        else:
            self.app = Flask(__name__)
            self.api = Api(self.app)
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_Song.db'
            self.db = SQLAlchemy(self.app)
            CreateFlaskApp.__instance = self
       
    def create_flask_app(self):
        return self.app , self.api , self.db


flask_obj = CreateFlaskApp.getInstance()
app , api , db = flask_obj.create_flask_app()

# ------------------------------------------------------------------------------------------------------------------




#----------------- AUDIO TYPE DB MODELS CLASSES--------------------------
class SongModel(db.Model):
    __tablename__ = 'SongModel'
    id = db.Column(db.Integer , primary_key=True)
    Name = db.Column(db.String(100) , nullable=False)
    Duration = db.Column(db.Integer , nullable=False)
    Uploadtime = db.Column(db.String ,  nullable=False)

    def __repr__(self):
        return "Song(Name={Name} , Duration={Duration} , Uploadtime={Uploadtime})"


class PodcastModel(db.Model):
    __tablename__ = 'PodcastModel'
    id = db.Column(db.Integer , primary_key=True)
    Name = db.Column(db.String(100) , nullable=False)
    Duration = db.Column(db.Integer , nullable=False)
    Uploadtime = db.Column(db.String, nullable=False)
    Host = db.Column(db.String , nullable=False)
    Participant = db.Column(db.String , nullable=True)
    def __repr__(self):
        return "Podcast(Name={Name} , Duration={Duration} , Uploadtime={Uploadtime} , Host={Host} , Participant={Participant})"


class AudiobookModel(db.Model):
    __tablename__ = 'AudiobookModel'
    id = db.Column(db.Integer , primary_key=True)
    Title = db.Column(db.String(100) , nullable=False)
    Author = db.Column(db.String(100) , nullable=False)
    Narrator = db.Column(db.String(100) , nullable=False)
    Duration = db.Column(db.Integer , nullable=False)
    Uploadtime = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "Audiobook(Title={Title} , Author={Author} , Narrator={Narrator} , Duration={Duration} , Uploadtime={Uploadtime})"


# db.create_all()

# -----------------------------------------------------------------------





# ----------------------- AUDIO TYPE CLASSES ------------------------------


# ---------- INTERFACE CLASS-----------------------
class Songs_interface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self , song_id):
        pass
    def post(self , song_id):
        pass
    def patch(self ,song_id):
        pass
    def delete(self , song_id):
        pass

# ----------- DERIVED CLASSES --------------------


class Song(Resource):

    __metaclass__ = Songs_interface

    def __init__(self):
        request_condition = request.method

    @marshal_with(resource_fields)
    def get(self , song_id):
        result = SongModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='Song is Not present...')
        return result

    @marshal_with(resource_fields)
    def post(self , song_id):
        args = SongParseRequest(request_condition).parse_args()
        result = SongModel.query.filter_by(id=song_id).first()
        if result:
            abort(400 , message='Song is already exist...')
        result = SongModel(id=song_id , Name=args['Name'] , Duration=args['Duration'] , Uploadtime=args['Uploadtime'])
        db.session.add(result)
        db.session.commit()
        return result , 200

    @marshal_with(resource_fields)
    def patch(self , song_id):
        args = SongParseRequest(request_condition).parse_args()
        result = SongModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='Song doesnt exist...')
        if args['Name']:
            result.Name = args['Name']
        if args['Duration']:
            result.Duration = args['Duration']
        if args['Uploadtime']:
            result.Uploadtime = args['Uploadtime']
        db.session.commit()

        return result , 200

    @marshal_with(resource_fields)
    def delete(self , song_id):
        args = SongParseRequest(request_condition).parse_args()
        result = SongModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='Song doesnt exist...')
        SongModel.query.filter_by(id=song_id).delete()
        db.session.commit()

        return '' , 200


class Podcast(Resource ):

    __metaclass__ = Songs_interface

    def __init__(self):
        request_condition = request.method

    @marshal_with(resource_fields_Podcast)
    def get(self , song_id):
        result = PodcastModel.query.filter_by(id=song_id).first()
        print(result)
        if not result:
            abort(400 , message='Podcast Song is Not present...')
        return result

    @marshal_with(resource_fields_Podcast)
    def post(self , song_id):
        args = PodcastParseRequest(request_condition).parse_args()
        part_str = convert_list_to_string(args['Participant'])
        result = PodcastModel.query.filter_by(id=song_id).first()
        if result:
            abort(400 , message='Podcast Song is already exist...')
        result = PodcastModel(id=song_id , Name=args['Name'] , Duration=args['Duration'] , Uploadtime=args['Uploadtime'] , Host=args['Host'] , Participant=part_str)
        db.session.add(result)
        db.session.commit()
        return result , 200

    @marshal_with(resource_fields_Podcast)
    def patch(self , song_id):
        args = PodcastParseRequest(request_condition).parse_args()
        result = PodcastModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='Podcast Song doesnt exist...')
        if args['Name']:
            result.Name = args['Name']
        if args['Duration']:
            result.Duration = args['Duration']
        if args['Uploadtime']:
            result.Uploadtime = args['Uploadtime']
        if args['Host']:
            result.Host = args['Host']
        if args['Participant']:
            part_str = convert_list_to_string(args['Participant'])
            result.Participant = part_str
        db.session.commit()

        return result , 200

    @marshal_with(resource_fields_Podcast)
    def delete(self , song_id):
        args = PodcastParseRequest(request_condition).parse_args()
        result = PodcastModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='Podcast Song doesnt exist...')
        PodcastModel.query.filter_by(id=song_id).delete()
        db.session.commit()

        return '' , 200


class Audiobook(Resource):

    __metaclass__ = Songs_interface

    def __init__(self):
        request_condition = request.method

    @marshal_with(resource_fields_AudioBook)
    def get(self , song_id):
        result = AudiobookModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='AudioBook is Not present...')
        return result

    @marshal_with(resource_fields_AudioBook)
    def post(self , song_id):
        args = AudioBookParseRequest(request_condition).parse_args()
        result = AudiobookModel.query.filter_by(id=song_id).first()
        if result:
            abort(400 , message='AudioBook is already exist...')
        result = AudiobookModel(id=song_id , Title=args['Title'] , Author=args['Author'] , Narrator=args['Narrator'], Duration=args['Duration'], Uploadtime=args['Uploadtime'])
        db.session.add(result)
        db.session.commit()
        return result , 200

    @marshal_with(resource_fields_AudioBook)
    def patch(self , song_id):
        args = AudioBookParseRequest(request_condition).parse_args()
        result = AudiobookModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='AudioBook doesnt exist...')
        
        if args['Title']:
            result.Name = args['Title']
        if args['Author']:
            result.Name = args['Author']
        if args['Narrator']:
            result.Name = args['Narrator']
        if args['Duration']:
            result.Duration = args['Duration']
        if args['Uploadtime']:
            result.Uploadtime = args['Uploadtime']
        db.session.commit()

        return result , 200

    @marshal_with(resource_fields_AudioBook)
    def delete(self , song_id):
        args = AudioBookParseRequest(request_condition).parse_args()
        result = AudiobookModel.query.filter_by(id=song_id).first()
        if not result:
            abort(400 , message='AudioBook doesnt exist...')
        AudiobookModel.query.filter_by(id=song_id).delete()
        db.session.commit()

        return '' , 200


# -----------------------------------------------------------------------




api.add_resource(Song  , '/Song/<int:song_id>')

api.add_resource(Podcast , '/Podcast/<int:song_id>')

api.add_resource(Audiobook , '/Audiobook/<int:song_id>')

if __name__ == '__main__':
    app.run(debug=True)
