from flask import Blueprint
from infrastructure.controllers.comment_controller import CommentController
from application.comment.comment_service import CommentService
from infrastructure.data_providers.comment_db_repository import CommentDbRepository

comment_bp = Blueprint('comment', __name__)
comment_service = CommentService(CommentDbRepository())
controller = CommentController(comment_service)

comment_bp.route('/comment/delete/<int:comment_id>', methods=['POST'])(controller.delete)
