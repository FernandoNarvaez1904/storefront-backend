from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class User(AbstractUser):
    pass


class Role(Group):
    class Meta:
        proxy = True

        permissions = [
            ("add_permission_to_role", "Can add permissions to Roles"),
            ("remove_permission_to_role", "Can remove permissions to Roles"),
            ("add_role_to_user", "Can add role to users"),
            ("remove_role_to_user", "Can remove role to users")
        ]
