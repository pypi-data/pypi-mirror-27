from django.conf.urls import url, include
from app.views import UserView, UserListView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='My API title', description='API description', public=False)),
    url(r'^user/$', UserListView.as_view()),
    url(r'^user/(?P<username>.+)/$', UserView.as_view()),
]
