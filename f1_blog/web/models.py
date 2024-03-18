from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MAX_LENGTH = 30

    first_name = models.CharField(
                                max_length=FIRST_NAME_MAX_LENGTH,
                                blank=True,
                                null=True
                                  )

    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH,
                                 blank=True,
                                 null=True
                                 )

    date_of_birth = models.DateField(blank=True,
                                     null=True
                                     )

    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE,
                                primary_key=True
                                )