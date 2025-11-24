import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)


def create_socket_app(app):
    """Cria ASGI app do Socket.IO acoplado ao FastAPI app."""
    return socketio.ASGIApp(sio, app)
