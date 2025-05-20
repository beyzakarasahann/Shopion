from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class SupportCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Açık'),
        ('answered', 'Yanıtlandı'),
        ('closed', 'Kapalı'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(SupportCategory, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    image = models.ImageField(upload_to='support_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    answer = models.TextField(blank=True, null=True)
    answered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.answer and not self.answered_at:
            self.answered_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} – {self.user.username}"
