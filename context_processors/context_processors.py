from blog.models import Article,Category


def recent_article(request):
    recent_article=Article.objects.order_by('-created')[:3]
    categories=Category.objects.all()
    return {"recent_article":recent_article,"categories":categories}