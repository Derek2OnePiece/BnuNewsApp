from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuNewsAppServer.src.views.comment_views',
    (r'^add_comment$', 'add_comment_action'),
    (r'^get_comments$', 'get_comments_action'),

)
