import eventlet
import socketio

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)


# 事件处理函数的两种写法
# sid：每个客户端连接的唯一标识符，一个客户端发送的所有事件具有相同的sid值
@sio.event
def my_event(sid, data):
    pass

@sio.on('my custom event')
def another_event(sid, data):
    pass

# connetc函数 在客户端连接时自动调用 可用于验证用户身份等
# environ 为字典格式，包含请求信息、http头
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    # 若返回 False 则表示拒绝与客户端的联系
    # return False
    # 抛错，将所有参数通过拒绝消息发送给客户端
    raise ConnectionRefusedError('authentication failed')


# disconnect函数 在客户端断开连接时自动调用
@sio.event
def disconnect(sid):
    print('disconnect ', sid)


# socketio.Server.emit() 发送事件
# sio.emit('事件名',{'具体信息数据': '……'})
sio.emit('my event', {'data': 'foobar'})
# room 用于标识应接受该事件的客户端sid，需要设置客户端的sid，若省略则表示广播事件
sio.emit('my event', {'data': 'foobar'}, room='user_sid')
# callback 回调函数，将在客户端处理事件后调用该函数，客户端返回的任何值都将作为参数给予该回调函数。
# 若在广播的情况下使用回调，则服务端将有大量的调用次数
sio.emit('my event', {'data': 'foobar'}, callback=my_event)

# namespace 命名空间
# client 为每个连接制定不同的命名空间，来打开多个连接，命名空间将作为主机名和端口后的路径名
# http://example.com:8000/chat
@sio.event(namespace='/chat')
def my_custom_event(sid, data):
    pass

@sio.on('my custom event', namespace='/chat')
def my_custom_event(sid, data):
    pass


# socketio.Namespace 基于类的命名空间
# 注意：基于类的命名空间为单例，所以命名空间实例不能用于存储客户端的特定消息
class MyCustomNamespace(socketio.Namespace):
    # 服务器接受的任何事件，都将调用 on_ 前缀的事件名方法
    # 若接受到的事件名在类内无匹配on前缀方法，则忽略。
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    # my_event 事件触发 on_my_event 方法的执行
    def on_my_event(self, sid, data):
        self.emit('my_response', data)

sio.register_namespace(MyCustomNamespace('/test'))

# room 指定用户组
# socketio.Server.enter_room() 和 socketio.Server.leave_room()方法管理其中的客户端
@sio.event
def begin_chat(sid):
    sio.enter_room(sid, 'chat_users')

@sio.event
def exit_chat(sid):
    sio.leave_room(sid, 'chat_users')

# skip_sid 用于跳过该sid的客户端，不进行消息推送
@sio.event
def my_message(sid, data):
    sio.emit('my reply', data, room='chat_users', skip_sid=sid)

# session 用户信息存储和检索
# 注意：客户端断开连接时，会破坏用户会话的内容。
# 特别是，当客户端在意外断开与服务器的连接后重新连接时，不会保留用户会话内容。
@sio.event
def connect(sid, environ):
    username = environ
    # username = authenticate_user(environ)
    sio.save_session(sid, {'username': username})

@sio.event
def message(sid, data):
    session = sio.get_session(sid)
    print('message from ', session['username'])

# 基于上下文，管理session
@sio.event
def connect(sid, environ):
    username = environ
    # username = authenticate_user(environ)
    with sio.session(sid) as session:
        session['username'] = username

@sio.event
def message(sid, data):
    with sio.session(sid) as session:
        print('message from ', session['username'])

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)