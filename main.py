# from game import Game
# import socketio
# import tornado
# from aiohttp import web
#
# from user.user import User
#
# game = Game()
# sio = socketio.AsyncServer(async_mode='aiohttp')
# app = web.Application()
# sio.attach(app)
#
#
# @sio.event
# def connect(sid, environ):
#     print("connected with socket id: ", sid)
#
#
# @sio.event
# async def user_login(sid, data: int):
#     """
#     first route to log in user
#     :param sid: autofilled
#     :param data: telegram user_id
#     :return: None
#     """
#     print(data)
#     await sio.save_session(sid, User(data))
#     game.user_go_online(await sio.get_session(sid))
#
#
# @sio.event
# async def disconnect(sid):
#     user_data: User = await sio.get_session(sid)
#     user_data.disconnect()
#     await sio.disconnect(sid)
#
#
# # @sio.event
# # async def data_element(sid, data):
# #     print(data)
# #     print(await sio.get_session(sid))
# #
# #
# # @sio.event
# # async def get_users(sid, data):
# #     print(await sio.get_session(sid))
#
#
# if __name__ == '__main__':
#     web.run_app(app)


from aiohttp import web
import socketio
import aiohttp_cors

sio = socketio.AsyncServer()
app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
   "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
       or

    )
  })

sio.attach(app)


async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def chat_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


# app.router.add_static('/static', 'static')
app.router.add_get('/', index)
for route in list(app.router.routes()):
    cors.add(route)
if __name__ == '__main__':
    web.run_app(app)
