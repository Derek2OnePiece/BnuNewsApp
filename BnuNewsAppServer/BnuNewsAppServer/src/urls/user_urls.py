from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuNewsAppServer.src.views.user_views',
    (r'^register$', 'register_action'),

)
