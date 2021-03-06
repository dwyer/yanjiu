from __future__ import unicode_literals

from django.conf.urls import include, url

from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'phrases', views.PhraseViewSet)
router.register(r'terms', views.TermViewSet)
router.register(r'texts', views.TextViewSet)
router.register(r'translations', views.TranslationViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^audio/(.+)\.mp4', views.audio_view, name='audio_view'),
    url(r'^flash/', views.flash_view, name='flash_view'),
    url(r'^auth', include('rest_framework.urls', namespace='rest_framework')),
]
