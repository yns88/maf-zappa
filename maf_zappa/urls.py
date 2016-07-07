from django.conf.urls import include, url
import anime.urls

urlpatterns = [
    url(r'^', include(anime.urls), name='anime')
]
