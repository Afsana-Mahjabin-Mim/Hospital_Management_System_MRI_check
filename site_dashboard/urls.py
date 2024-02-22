from django.urls import path 

from .views import *

app_name="site_dashboard"

urlpatterns=[
    path("",MainDashBoardView.as_view(),name="main_dashboard"),

    path("site_contact/",SiteContactView.as_view(),name="site_contact"),
    path("portfolio-details/",PortfolioDetailsView.as_view(),name="portfolio_details"),
    path("blog-single/",BlogSingleView.as_view(),name="blog_single"),
    path("four_O_four/",Four0FourView.as_view(),name="four_O_four"),
    path("about_us/",AboutUsView.as_view(),name="about_us"),
    


]
