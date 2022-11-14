from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import socketio
import pymongo
from aiohttp import web

# create a Socket.IO server
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Tkinter"]
mycol = mydb["Rooms"]
mymes = mydb["Messages"]



# x = mycol.insert_one(mydict)

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)



@sio.event
async def join_room(sid,data):
    print("joined room")
    print(sid)
    print(data)
    mydict = data
    x=mycol.insert_one(mydict)
    print(x)
    await chatroom_users(data['room'])

@sio.event
async def chatroom_users(room):
    print("in users fetch")
    lists=[{}]
    num=0
    for x in mycol.find({"room":room}):
        print(x)
        dicts={'username':x['username'],'id':num}
        num=num+1
        print(x['username'])
        lists.append(dicts)
    await sio.emit(event = 'chatroom_users', data = lists)
    await fetchmes(room)

@sio.event
async def send_message(sid,data):
    print(data)
    x=mymes.insert_one(data)
    print(x)
    await receive_message(data)

@sio.event
async def receive_message(mes):
    print("recieving ",mes)
    sen={"username":mes['username'],"room":mes['room'],"message":mes['message'],"__createdtime__":mes['__createdtime__']}
    await sio.emit(event = 'receive_message', data = sen)

@sio.event
async def fetchmes(room):
    lists1=[{}]
    flag=False
    for x in mymes.find({"room":room}):
        print(x)
        flag=True
        dicts={'username':x['username'],'__createdtime__':x['__createdtime__'],"message":x['message']}
        
        lists1.append(dicts)
    print("lists is : ",lists1)
    
    await sio.emit(event = 'last_100_messages', data = lists1)

@sio.event
def leave_room(sid,data):
    mycol.delete_one({"username":data['username']})





@sio.event
def connect(sid, en):
    print('connect ', sid)
    

@sio.event
async def messagercv(sid,message):
    print("recieved from clie3nt : ",message)
    await sio.emit(event = 'receive', data = {'message': message})

@sio.event
def messagesnd(message):
    sio.emit(event = 'recieve', data = {'message': message})
    




web.run_app(app)






