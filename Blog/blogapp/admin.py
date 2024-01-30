from django.contrib import admin
from .models import Category, Author, Post, Comment

# Register your models here.
@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'upload_image', 'date_created', 'updated_on', 'author', 'category', 'status')


@admin.register(Category)
class categoryadmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Author)
class Authoradmin(admin.ModelAdmin):
    list_display = ('display_name', 'profile', 'user')



@admin.register(Comment)
class Commadmin(admin.ModelAdmin):
    list_display = ('post', 'comment_body', 'commenter_name', 'date_created', 'user')



# admin.site.register(Post)


# Register your models here.
