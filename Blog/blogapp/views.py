from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import View, ListView, DetailView
from .models import Post, Category, Author, Comment, User
import pdb

# Create your views here.
class Blog_post(View):

    def get(self, request):
      
        try:
            Myuser = Author.objects.get(user=request.user)
        except: Myuser = None

        if request.user.is_authenticated:
            if not Myuser:
                # return HttpResponse('Kindly update your Profile')
             return redirect('beauthor')
        
        try:
            post_category = Post.objects.filter(category__name='Featured post', status='approved').latest('date_created')
        except: post_category=None
        
        # post = Post.objects.all()
        approved_post = Post.objects.filter(status='approved')
        pending_post = Post.objects.filter(status='pending')

        try:
            userpendingposts = Post.objects.filter(author=request.user, status='pending')
        except:userpendingposts=None
        
        try:
            userposts = Post.objects.filter(author=request.user, status='approved')
        except: userposts = None
        
        # engaging = Comment.objects.all()

        engagement_counts = {
            'user_engaging': Comment.objects.filter(post__author=request.user).count() if request.user.is_authenticated else 0,
            'total_engaging': Comment.objects.all().count() if request.user.is_staff else 0
        }
        

        
        # pdb.set_trace()
        context = {
            'allpost': approved_post,
            'post_category': post_category,
            'pending': pending_post,
            'userpendingpost': userpendingposts,
            'userpost': userposts,
            'engagement_counts': engagement_counts,
            'total_engaging': Comment.objects.all().count() if request.user.is_staff else 0,
            
        }
           

        return render(request, 'index.html', context=context)


    def post(self, request):
        return render(request, 'index.html')
    



class Blog_Details(ListView):
    def get(self, request, pk):
        post_details = get_object_or_404(Post, pk=pk)

        context = {
            'post_details': post_details
        }

        return render(request, 'details.html', context=context)
        
    

    def post(self, request, pk):
        post_details = Post.objects.get(pk=pk)
        # post_details = Post.objects.get(pk=pk)
        post_details = get_object_or_404(Post, pk=pk)
        
        context = {
           'post_details': post_details
        }

        return render(request, 'details.html', context=context)
    

    
class Featured_blog(ListView):
    def get(self, request, pk):
        featured = get_object_or_404(Post, pk=pk)

        context = {
           'allpost': featured
        }

        return render(request, 'index.html', context=context)
    


    def post(self, request):
        
        return render(request, 'index.html') 
    



class Category_list(DetailView):
    def get(self, request, category_slug):
        catlist = Category.objects.get(slug=category_slug)
        category_by_post = Post.objects.filter(category=catlist, status='approved')

        contexta={
            'list': catlist,
            'category_by_post': category_by_post,
        }

        return render(request, 'category/cat_list.html', context=contexta)
    
    
    def post(self, request):
        return render(request, 'category/cat_list.html')


