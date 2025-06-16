from flask import Blueprint
from infrastructure.controllers.user_controller import UserController
from application.user.user_service import UserService
from infrastructure.data_providers.user_db_repository import UserApiRepository

user_bp = Blueprint('user', __name__)
user_service = UserService(UserApiRepository())
controller = UserController(user_service)

user_bp.route('/login', methods=['GET', 'POST'])(controller.login)
user_bp.route('/register', methods=['GET', 'POST'])(controller.register)
user_bp.route('/edit', methods=['GET', 'POST'])(controller.edit)
user_bp.route('/logout')(controller.logout)
