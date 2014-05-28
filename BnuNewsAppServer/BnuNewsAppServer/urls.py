from django.conf.urls import patterns, include, url
from BnuNewsAppServer import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BNUNewsAppServer.views.home', name='home'),
    # url(r'^BNUNewsAppServer/', include('BNUNewsAppServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^appserver/user/', include('BnuNewsAppServer.src.urls.user_urls')),
    (r'^appserver/news/', include('BnuNewsAppServer.src.urls.news_urls')),
    (r'^appserver/comment/', include('BnuNewsAppServer.src.urls.comment_urls')),
    (r'^appserver/p/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH + '/images'}),

)
