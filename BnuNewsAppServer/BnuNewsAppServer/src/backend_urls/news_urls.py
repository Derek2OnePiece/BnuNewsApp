from django.conf.urls.defaults import patterns

urlpatterns = patterns('BnuNewsAppServer.src.backend_views.news_views',
    (r'^add_news$', 'admin_add_news_action'),
    (r'^get_news_detail$', 'admin_get_news_detail_action'),
    (r'^update_news$', 'admin_update_news_action'),
    (r'^list_news$', 'admin_list_news_action'),
    (r'^pub_news$', 'admin_pub_news_action'),
    (r'^cancel_pub_news$', 'admin_cancel_pub_news_action'),
    (r'^delete_news$', 'admin_delete_news_action'),
)
