from django.shortcuts import render
from blog.models import Article
# Create your views here.

def home(request):
    articles=Article.objects.all()

    recent=Article.objects.all().order_by("-created")[:3]

    return render(request,"home_app/index.html",context={"articles":articles,"recent":recent})
