from django.contrib import admin
from django.urls import path,include 
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls), 
    path("dashboard/",include("dashboard.urls",namespace="dashboard")),
    path("site_dashboard/",include("site_dashboard.urls",namespace="site_dashboard")),

    path("api/user/",include("users.urls"))

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


