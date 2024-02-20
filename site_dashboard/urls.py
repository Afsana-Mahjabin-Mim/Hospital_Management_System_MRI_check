from django.urls import path 

from .views import *

app_name="site_dashboard"

urlpatterns=[
    path("",MainDashBoardView.as_view(),name="main_dashboard"),

    path("site_contact/",SiteContactView.as_view(),name="site_contact"),
    


]
