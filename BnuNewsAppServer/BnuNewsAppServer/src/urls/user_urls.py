from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuNewsAppServer.src.views.user_views',
    (r'^register$', 'register_action'),
    (r'^login$', 'login_action'),
    (r'^update_user_profile$', 'update_user_profile_action'),

)
