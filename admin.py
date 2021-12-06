# from flask_admin.contrib import sqla
# from flask_admin.contrib.sqla import ModelView
# from flask import session, redirect, url_for, request


# class AdminView(sqla.ModelView):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.static_folder = 'static'

#     def is_accessible(self):
#         return current_user.is_authenticated
#         # print (session.get('username'))
#         # return session.get('username') == 'admin'

#     def inaccessible_callback(self, name, **kwargs):
#         if not self.is_accessible():
#             return redirect(request.args.get('next') or url_for('startPage'))