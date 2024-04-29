from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=66)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class Article(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category)
    title=models.CharField(max_length=40)
    body=models.TextField()
    image=models.ImageField(upload_to='image/articles')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    slug=models.SlugField(null=True,unique=True,blank=True)
    def get_absolute_url(self):
        return reverse('blog:detail',args=[self.slug])
    def Meta(self):
        ordering = ("-created",)
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug=slugify(self.title)
        super(Article,self).save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    parent=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name="replied")

    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[:22]


class Message(models.Model):
    title=models.CharField(max_length=100)
    text=models.TextField()
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes",verbose_name="کاربر")
    article=models.ForeignKey(Article,on_delete=models.CASCADE,related_name="likes",verbose_name="مقاله")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}-{self.article.title}"
    class Meta:
        verbose_name="لایک"
        verbose_name_plural="لایک ها"
        ordering = ("-created_at",)

































































































