from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from front import views

# pylint: disable=C0103
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^autor/$', views.index, name='author_b'),
    url(r'^autor/(?P<author_id>[0-9]+)$', views.index, name='author'),
    url(r'^some_cards/$', views.get_some_cards, name='somecards'),
    url(r'^add_card/$', views.add_card, name='add_card'),
    url(r'^mycards/(?P<cards_hash>.+)$', views.my_cards, name='my_cards'),
    url(r'^mycards/$', views.my_cards, name='my_cards_b'),
    url(r'^shops/$', views.shops, name='shops'),
    url(r'^about/$', views.about,  name='about'),
    url(r'^count_change/$', views.my_card_count_change, name='my_card_count_change')
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
