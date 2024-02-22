from django.shortcuts import render
from django.views import View 

# Create your views here.



"""
        ------------ Site Dashboard View ------------
"""

class MainDashBoardView(View):
    def get(self,request):
        return render(request, "webpage/index.html")


"""
        ------------ Contact View ------------
"""

class SiteContactView(View):
    def get(self,request):
        return render(request, "webpage/contact.html")



"""
        ------------ Portfoilo Details View ------------
"""

class PortfolioDetailsView(View):
    def get(self,request):
        return render(request, "webpage/portfolio-details.html")




"""
        ------------ Blog View ------------
"""

class BlogSingleView(View):
    def get(self,request):
        return render(request, "webpage/blog-single.html")



"""
        ------------ 404 View ------------
"""

class Four0FourView(View):
    def get(self,request):
        return render(request, "webpage/404.html")



"""
        ------------ About Us View ------------
"""

class AboutUsView(View):
    def get(self,request):
        return render(request, "webpage/about-us.html")
    


