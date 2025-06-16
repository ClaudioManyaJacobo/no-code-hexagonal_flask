from flask import request, redirect, url_for, session

class CommentController:
    def __init__(self, comment_service):
        self.comment_service = comment_service

    def delete(self, comment_id):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))

        if self.comment_service.delete_comment(comment_id, session['user_id']):
            return redirect(request.referrer or url_for('movie.index'))
        else:
            return "No autorizado para eliminar este comentario", 403
