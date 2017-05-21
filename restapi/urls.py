from django.conf.urls import url
from mainapi.views import upload_file,testui,getRequest,getRequest2,delete,put


#This is the place where the url schema is defined
#Notice how the functions from views module are imported and attached to
#different urls

urlpatterns = [
    url(r'^testui/$', testui,name="testui"),
    url(r'^upload/$', upload_file,name="upload"),
    url(r'^questions/(\d+)/$', getRequest),
    url(r'^questions/(\w+)/$', getRequest),
    url(r'^testui/search/$', getRequest2),
    url(r'^search/$', getRequest2),
    url(r'^delete/$',delete),
    url(r'^testui/delete/$',delete),
    url(r'^put/$',put),
    url(r'^add/$',put)
]
