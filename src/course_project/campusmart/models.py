from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Listing Model
class Listing(models.Model):
    ''' This is a Listing model. '''
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Used', 'Used'),
        ('Fair', 'Fair'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    photo = models.ImageField(upload_to='listing_photos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.created_by}'s {self.title}"
# Conversation Model for Feature 3.3
class Conversation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
# ConversationMessage Model for Feature 3.3
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message by {self.created_by.username} on {self.created_at}"
#  Player model for Feature 4.1
class Player(models.Model):
    # extend the built-in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # declare additional_listings in order to persist past 24 hours
    additional_listings = models.PositiveIntegerField(default=0)
