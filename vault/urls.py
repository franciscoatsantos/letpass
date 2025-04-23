from django.urls import path
from vault.views import EntryListView

urlpatterns = [
    path('passwords/', EntryListView.as_view(), name='get_passwords'),
]