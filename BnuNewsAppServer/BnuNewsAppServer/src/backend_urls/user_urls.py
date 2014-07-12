from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuNewsAppServer.src.backend_views.user_views',
    (r'^login$', 'login_action'),
    (r'^get_user_summary$', 'get_user_summary_action'),

)
