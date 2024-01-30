from django.shortcuts import render, HttpResponse, redirect, get_list_or_404, get_object_or_404
from django. views.generic import View, UpdateView
from blogapp.models import Category, Post, Author, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.

categories = Category.objects.all()

# Creating user post views here;
class Create_userpost(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):

        context={
            'category': categories,
        }

        return render(request, 'crud/usercreate.html', context=context)
    
    
    def post(self, request):
        post_title = request.POST['title']
        body = request.POST['body']
        postimages = request.FILES.get('postimage')
        cate = request.POST['category']
        try:
            categories = Category.objects.get(slug = cate)
        except Category.DoesNotExist:
            messages.error(request, 'Category not found')
            return redirect('createpost')    

        create_post = Post.objects.create(title=post_title, body=body, upload_image=postimages, category=categories, 
                                          author=request.user)
        create_post.save()
        messages.success(request, 'Post created successfully. See pending posts')
        return redirect('home')
        # return HttpResponse('Post created successfully')
    

        # return render(request, 'crud/usercrud.html')




class CreateCategory(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'crud/catcreate.html')

    def post(self, request):
        category_name = request.POST['category']

        # Check if the category already exists
        if Category.objects.filter(name=category_name).exists():
            messages.error(request, 'Category already exists')
            return redirect('catcreator')

        # Create a new category
        create_category = Category(name=category_name)
        create_category.save()
        messages.success(request, 'Category created successfully')
        return redirect('home')




class Comments(View):
    def get(self, request, pk):
        return render(request, 'details.html', pk=pk)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)

        if not request.user.is_authenticated:
            return redirect('login')
    
        author = Author.objects.get(user=request.user)

        comment = request.POST['comment']
        error_message = None

        if not comment.strip():
            error_message = "Comment cannot be empty."

        if error_message:
            messages.error(request, 'Comment cannot be empty. Please enter a comment.')
            return redirect('details', pk=pk)
            

        create_comment = Comment.objects.create(post=post, user=author, comment_body=comment)
        if create_comment:
            messages.success(request, 'Comment created successfully')
            return redirect('details', pk=pk)

        return render(request, 'details.html', {'author': author})

    

    # def post(self, request, pk):
    #     post = Post.objects.get(pk=pk)
    #     author = Author.objects.get(user=request.user)
    #     # author = Author.objects.get(pk=pk)     was also working
    #     comment = request.POST['comment']
        
    #     create_comment = Comment.objects.create(post=post, user=author, comment_body=comment)
    #     if create_comment:
    #         return redirect('details', pk=pk)
        
    #     return render(request, 'details.html', {'author':author})
    


class Edit_userpost(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        post = get_list_or_404(Post, pk=pk)

        context = {
        'posts': post,
        'catagory': categories,
        }
        return render(request, 'crud/useredit.html', context=context)

    

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        author = Author.objects.get(user=request.user)
        post_title = request.POST['title']
        body = request.POST['body']
        postimages = request.FILES.get('postimage')
        
        try:
            category_slug = request.POST['category']
            categories = Category.objects.get(slug = category_slug)
        except Category.DoesNotExist:
            messages.error(request, 'Category Not Found, add category to edit')
            return redirect('details', pk=pk)
        
        # Update the existing post instance with the new data
        post.title = post_title
        post.body = body
        post.category = categories
        author = author
        
        if postimages:
            post.upload_image = postimages

        post.save()
        messages.success(request, 'Post edited successfully')
        return redirect('details', pk=pk)





class Delete_userpost(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        try:
            posts = get_list_or_404(Post, pk=pk)
        except Post.DoesNotExist:
            return HttpResponse('Post Not Found')
            
        context={
            'postdel': posts,
        }
        # messages.error(request, 'You are deleting this post?')
        return render(request, 'crud/userdelete.html', context=context)
    

    def post(self, request, pk):
        posts = get_object_or_404(Post, pk=pk)
        posts.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')
    



class Delete_comments(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        try:
            comments = get_list_or_404(Comment, pk=pk)
        except Post.DoesNotExist:
            return HttpResponse('Post Not Found')
            
        context={
            'commdel': comments,
        }
        return render(request, 'crud/commdelete.html', context=context)
    
    def post(self, request, pk):
        Comments = get_object_or_404(Comment, pk=pk)
        Comments.delete()
        messages.success(request, 'Comment deleted successfully')
        return redirect('home')
        


class DeleteCategory(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        # Retrieve the category by its ID
        category = get_object_or_404(Category, pk=pk)

        # Render a confirmation page
        return render(request, 'crud/delcat.html', {'category': category})

    def post(self, request, pk):
        # Retrieve the category by its ID
        category = get_object_or_404(Category, pk=pk)

        # Delete the category
        category.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect('home')


        

class Pendingpage(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        pending_posts = get_object_or_404(Post, pk=pk)
        if request.user.is_staff:
            pending_posts = Post.objects.filter(status='pending')
        else:
            pending_posts = Post.objects.filter(author=request.user, status='pending')

        return render(request, 'crud/pendingpage.html', {'pending_posts': pending_posts})
    

    def post(self, request, pk):
        pending_posts = get_object_or_404(Post, pk=pk) 
        if request.user.is_staff:
            try:
                pending_posts = get_object_or_404(Post, pk=pk)    
                if request.POST.get('approve'):
                    pending_posts.status = 'approved'
                    pending_posts.save()
            except: pending_posts = None 

        context =  {
            'pending_posts': pending_posts
            }      
        
        return redirect('crud/pendingpage.html', context=context, pk=pk)
    


class ApprovePost(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'post': post,
        }
        
        return render(request, 'crud/penapprove.html', context=context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.status = 'approved'
        post.save()
        messages.success(request, 'Post approved successfully')
        return redirect('home')
    

class UnapprovePost(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'post': post,
        }
        return render(request, 'crud/unapprove.html', context=context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.status = 'pending'
        post.save()
        messages.success(request, 'Post unapproved successfully. See pending posts')
        return redirect('home')
    




# def approve_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.status = 'approved'
#         post.save()
#         return HttpResponseRedirect('/admin/posts/')

#     return redirect({'admin:index'})                       Was returning template mismatch error
