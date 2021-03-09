import datetime
from datetime import date
from flask_restful import  abort , reqparse
import argparse





def song_length(song_name):
    if len(str(song_name)) >= 100:
        abort(400 , message="Length Should be less than 100...")
    if song_name is None:
        abort(400 , message="Name is Required...")

    return str(song_name)

def convert_list_to_string(value):
    result = ''
    if value != None:
        if len(value) > 10:
            abort(400 , message="List must be less than 10...")
        else:
            for i in value:
                temp = song_length(i) + ','
                result = result + temp
            return result


def duration_positive(value):
    ivalue = int(value)
    if ivalue <=0:
        abort(400 , message="%s is an invalid positive int value...")

    return int(value)


def check_datetime(value):
    print("in chcekc 2 dunctionm")
    date_time_str = str(value)
    today_date = datetime.datetime.today().strftime("%Y-%m-%d")
    print("today date: ",today_date)
    try:
        print("in try...")
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        

    except:
        print("in except...")
        raise argparse.ArgumentTypeError("%s Datetime is not in proper format, it should be %Y-%m-%d %H:%M:%S.%f" % value)
    

    
    var_split = str(date_time_obj.date()).split('-')
    if int(var_split[0]) < int(today_date.split('-')[0]) or int(var_split[1]) > 12:
        raise argparse.ArgumentTypeError("%s Error! Year shouldnt be less than current..." % value)
    if int(var_split[0]) >= int(today_date.split('-')[0]) and int(var_split[1]) < int(today_date.split('-')[1]):
        raise argparse.ArgumentTypeError("%s Error! Month shouldn't be less than Current Month..." % value)
    print("end....")
    
    return str(date_time_obj)


def SongParseRequest(request_condition):

    songs_request_args = reqparse.RequestParser()
    songs_request_args.add_argument('Name' , type=song_length , required= False if request_condition == 'Patch' else True)
    songs_request_args.add_argument('Duration' , type=duration_positive, required= False if request_condition == 'Patch' else True)
    songs_request_args.add_argument('Uploadtime' , type=check_datetime , required= False if request_condition == 'Patch' else True)

    return songs_request_args

def PodcastParseRequest(request_condition):

    podcast_request_args = reqparse.RequestParser()
    podcast_request_args.add_argument('Name' , type=song_length , required= False if request_condition == 'Patch' else True)
    podcast_request_args.add_argument('Duration' , type=duration_positive, required= False if request_condition == 'Patch' else True)
    podcast_request_args.add_argument('Uploadtime' , type=check_datetime , required= False if request_condition == 'Patch' else True)
    podcast_request_args.add_argument('Host' , type=song_length , required= False if request_condition == 'Patch' else True)
    podcast_request_args.add_argument('Participant' , type=str , action='append' , required= False)


    return podcast_request_args

def AudioBookParseRequest(request_condition):

    AudioBook_request_args = reqparse.RequestParser()
    AudioBook_request_args.add_argument('Title' , type=song_length, required= False if request_condition == 'Patch' else True)
    AudioBook_request_args.add_argument('Author' , type=song_length , required= False if request_condition == 'Patch' else True)
    AudioBook_request_args.add_argument('Narrator' , type=song_length , required= False if request_condition == 'Patch' else True)
    AudioBook_request_args.add_argument('Duration' , type=duration_positive , required= False if request_condition == 'Patch' else True)
    AudioBook_request_args.add_argument('Uploadtime' , type=check_datetime , required= False if request_condition == 'Patch' else True)

    return AudioBook_request_args

