from django.shortcuts import render,get_object_or_404,redirect
from .models import Article, Category, Comment, Message, Like
from django.core.paginator import Paginator
from .forms import ContactUsForm,MessageForm
from django.views.generic.base import View
from django.views.generic import FormView,DetailView
from django.http import JsonResponse

# Create your views here.


def post_detail(request,slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        body=request.POST.get("body")
        parent_id=request.POST.get("parent_id")
        Comment.objects.create(body=body,article=article,user=request.user, parent_id=parent_id)

    return render(request,"blog/post-details.html",context={"article":article})



def posts_list(request):
    article=Article.objects.all()
    page_number=request.GET.get("page")
    paginator=Paginator(article,2)
    objects_list=paginator.get_page(page_number)
    return render(request,"blog/article_list.html",{"article":objects_list})


def category_detail(request,pk):
    category=get_object_or_404(Category,id=pk)
    article=category.article_set.all()
    return render(request,"blog/article_list.html",{"article":article })


def search(request):
    q=request.GET.get("q")
    article=Article.objects.filter(title__icontains=q)
    page_number = request.GET.get("page")
    paginator = Paginator(article, 2)
    objects_list = paginator.get_page(page_number)
    return render(request,"blog/article_list.html",{"article":objects_list})



def contact_us(request):
    if request.method == "POST":
        form=MessageForm(data=request.POST)
        if form.is_valid():
            # title=form.cleaned_data["title"]
            # text=form.cleaned_data["text"]
            # email=form.cleaned_data.get("email")
            # Message.objects.create(title=title,text=text,email=email)
            form.save()
            return redirect("blog:contact_us")
    else:
        form = MessageForm()
    return render(request,"blog/contact_us.html",{"form":form})



class ListView(View):
    queryset=None
    template_name=None
    def get(self,request):
        return render(request,self.template_name,{"object_list":self.queryset})

class ArticleList(ListView):
    queryset = Article.objects.all()
    template_name = "blog/articlelist2.html"


class ContactUsView(FormView):
    template_name = "blog/contact_us.html"
    form_class = MessageForm
    success_url = "/"
    def form_valid(self, form):
        form_data=form.cleaned_data
        Message.objects.create(**form_data)
        return super().form_valid(form)

class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/post-details.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.likes.filter(article__slug=self.object.slug,user_id=self.request.user.id).exists():
                context["is_liked"]=True
            else:
                context["is_liked"]=False
            return context
        else:
            return context


def like(request,slug,pk):
    if request.user.is_authenticated:
        try:
            like=Like.objects.get(article__slug=slug,user_id=request.user.id)
            like.delete()
            return JsonResponse({"response":"unliked"})
        except:
            Like.objects.create(article_id=pk,user_id=request.user.id)
            return JsonResponse({"response":"liked"})
    else:
        return redirect("account:login")
    return redirect("blog:detail",slug)