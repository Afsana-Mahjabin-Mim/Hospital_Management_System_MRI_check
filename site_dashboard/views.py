from django.shortcuts import render
from django.views import View 

# Create your views here.



"""
        ------------ Site Dashboard View ------------
"""

class MainDashBoardView(View):
    def get(self,request):
        return render(request, "webpage/index.html")



class SiteContactView(View):
    def get(self,request):
        return render(request, "webpage/contact.html")
    


