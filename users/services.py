from .models import User

def change_status():
    user = User.objects.all()

    for i in user:
        i.is_staff = True
        i.save()