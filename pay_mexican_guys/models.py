from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class WhoPays(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Who pays?"
        verbose_name_plural = "Who pays?"

    def save(self, *args, **kwargs):
        if not self.pk and WhoPays.objects.exists():
            raise ValidationError('Only one person can pay the mexicans')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username
