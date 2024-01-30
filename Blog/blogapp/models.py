from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    # slug = models.SlugField(unique=True, blank=True, max_length=300, default='sky')

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class Author(models.Model):
    profile = models.ImageField(upload_to='profile')
    display_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=255, blank=True, null=True)
    facebook_handle = models.CharField(max_length=255, blank=True, null=True)
    google_plus_handle = models.CharField(max_length=255, blank=True, null=True)
    instagram_handle = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.display_name



post_status = (

    ('pending', "pending"),
    ('delete', "delete"),
    ('approved', "approved")
)

class Post(models.Model):
    title = models.CharField(max_length=300)
    body = RichTextField(blank=True, null=True)
    # body = models.TextField(max_length=1000)
    upload_image = models.ImageField(upload_to='post')
    date_created = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    status = models.CharField(choices=post_status,default='pending',max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']

#        OR
  
    # class Meta:
    #     ordering = [''-comments__count'']    This would order posts by number of comments in descending order
           


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=500)
    commenter_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE, default=10)

    def __str__(self):
        return self.comment_body
    
    class Meta:
        ordering = ['-date_created']  
    
    


