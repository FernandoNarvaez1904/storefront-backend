from django.contrib.auth.models import AbstractUser, Group


# Create your models here.
class User(AbstractUser):
    pass


class Role(Group):
    class Meta:
        proxy = True
        permissions = [
            ("add_permission_to_role", "Can add permissions to Roles")
        ]
