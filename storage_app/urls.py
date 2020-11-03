from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import handle_records, handle_record

urlpatterns = {
    path('', handle_records, name='records'),
    path('<slug:key>', handle_record, name='unique_record')
}

urlpatterns = format_suffix_patterns(urlpatterns)
