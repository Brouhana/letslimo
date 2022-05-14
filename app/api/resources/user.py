from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus


class UserResource(MethodView):
    def get(self, company_id, user_id):
        args = request.args.get('user_type')
        return args, HTTPStatus.OK

    def post(self):
        return "Create a new user"

    def put(self, company_id, user_id):
        return "Update user"

    def delete(self, company_id, user_id):
        return "Delete user"
