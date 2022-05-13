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


# https://github.com/PrettyPrinted/youtube_video_code/blob/master/2019/08/08/Flask%20REST%20API%20Example%20With%20Pluggable%20Views%20and%20MethodView/api_demo/app.py
