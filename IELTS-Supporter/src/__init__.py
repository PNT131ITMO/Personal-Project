from flask import Flask
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

bcrypt = Bcrypt()
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='../templates',static_folder='../static')

    app.config.from_object('src.config.Config')
    app.config.from_pyfile('config.py', silent=True)


    # Initialize extensions
    bcrypt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from src.routes.auth import auth_bp
    from src.routes.profile import profile_bp
    from src.routes.vocabulary import vocabulary_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(vocabulary_bp)

    # Initialize services
    from src.services.database import init_db
    init_db(app)

    # Register socket handlers
    from src.sockets.handlers import init_socket_handlers
    init_socket_handlers(socketio)

    return app, socketio