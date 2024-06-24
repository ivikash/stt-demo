from flask_socketio import SocketIO, join_room, leave_room, emit

socketio = SocketIO()


@socketio.on("join_room")
def on_join_room(data):
    room_id = data["room_id"]
    join_room(room_id)


@socketio.on("leave_room")
def on_leave_room(data):
    room_id = data["room_id"]
    leave_room(room_id)


@socketio.on("send_message")
def on_send_message(data):
    room_id = data["room_id"]
    message = data["message"]
    emit("receive_message", {"message": message}, room=room_id)
