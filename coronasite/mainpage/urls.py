from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name="mainpage"
urlpatterns = [
    path('',views.index,name="index"),
    path('contacts',views.contacts,name="contacts"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
