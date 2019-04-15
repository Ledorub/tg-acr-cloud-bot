from django.urls import path
from acr_bot import views
from acr_bot.bot.config import token

urlpatterns = [
    path(f'{token}/', views.handle_request, name='handle_request')
]
