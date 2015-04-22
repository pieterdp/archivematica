
from django.conf.urls import patterns, url

urlpatterns = patterns('components.arrange.views',
    url(r'^$', 'index', name='arrange_index')
)
