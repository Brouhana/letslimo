from flask.views import MethodView


class UserResource(MethodView):
    def get(self, user_id):
        return "Get all users"

    def post(self):
        return "Create a new user"

    def put(self, user_id):
        return "Update user"

    def delete(self, user_id):
        return "Delete user"
