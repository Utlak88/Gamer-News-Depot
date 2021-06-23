from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from homepage import views

app_name = "homepage"
urlpatterns = [
    path("developers/", views.dev_list, name="devlist"),
    path("developers/<slug:slug>", views.dev_view, name="dev"),
    path("game_news/", views.gamenews, name="gamenews"),
    path("", views.dev_view, name="dev"),
    path("developer_news/", views.devgamesfunct, name="devall"),
    path("my_favorites/", views.dev_user, name="devuser"),
    path("about/", views.about, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
