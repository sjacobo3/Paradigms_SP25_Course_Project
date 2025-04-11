from django.contrib import admin
from .models import Listing, Conversation, ConversationMessage

# Register your models here.
admin.site.register(Listing)
admin.site.register(Conversation)
admin.site.register(ConversationMessage)