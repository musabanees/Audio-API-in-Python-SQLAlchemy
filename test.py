import requests
from datetime import datetime
BASE = 'http://127.0.0.1:5000/'
# x = '12/04/23'
x =  "2023-06-29 08:15:27.243860"
audio_list = ['song1' , 'song2' , 'song3', 'song4' , 'song' , 'song6' , 'song7' , 'song8' , 'song9' , 'spng10' ]

# --------------- Song Testing -----------------------
print("Post Request for Songs")
response = requests.post(BASE + 'Song/14' , {'Name':'High Sky' , 'Duration':9109 , 'Uploadtime':x})
print(response.json())

print("Get Request for Songs")

response = requests.get(BASE + 'Song/14')
print(response.json())

print("Patch (Update) Request for Songs")

response = requests.patch(BASE + 'Song/14' , {'Duration':122 })
print(response.json())

print("Delete Request for Songs")

response = requests.delete(BASE + 'Song/14')
print(response.json())


# response = requests.post(BASE + 'Podcast/1' , {'Name':'podcast_name11' , 'Duration':912 , 'Uploadtime':x , 'Host':'Podcast_host_11' , 'Participant':audio_list})
# print(response.json())

# input()

# response = requests.get(BASE + 'Podcast/1')
# print(response.json())

# input()

# response = requests.patch(BASE + 'Podcast/20' , {'Participant':audio_list })
# print(response.json())

# input()

# response = requests.get(BASE + 'Podcast/20')
# print(response.json())

# data = [{'Name':'Audiobook2' ,'Title':'Audiobook_title2','Author':'Audiobook_author2','Narrator':'Audiobook_narr2', 'Duration':9109 , 'Uploadtime':x},
# {'Name':'Audiobook2' ,'Title':'Audiobook_title2','Author':'Audiobook_author2','Narrator':'Audiobook_narr2', 'Duration':9109 , 'Uploadtime':x},
# {'Name':'Audiobook3' ,'Title':'Audiobook_title2','Author':'Audiobook_author3','Narrator':'Audiobook_narr3', 'Duration':9109 , 'Uploadtime':x}]
# count = 2
# for i in data:
#     response = requests.post(BASE + 'Audiobook/' + str(count) , i)
#     print(response.json())
#     count = count+1


# input()

# response = requests.get(BASE + 'Audiobook/3')
# print(response.json())

# input()

# response = requests.delete(BASE + 'Audiobook/3')
# print(response.json())

# input()

# response = requests.get(BASE + 'Audiobook/3')
# print(response.json())