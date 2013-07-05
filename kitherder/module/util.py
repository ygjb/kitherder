# module/util.py
def create_user(email):
    return User.objects.create_user(email, email)