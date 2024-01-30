from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blogapp.models import Author
from blogapp.views import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
import pdb
from django.contrib import messages
from django.http import HttpResponseBadRequest
# from django.contrib.auth.decorators import login_required      This import isn't working for Anonymous user; line 87

# Create your views here.
class Signup(View):
    def get(self, request):
        return render(request, 'registration/signup.html')
    

    def post(self, request):
        userrrname = request.POST['username']
        useremail = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        passworda = request.POST['password']
        confirm_password = request.POST['password2']

        if passworda != confirm_password:
            messages.error(request, 'Password is not same')
            return render(request,'registration/signup.html')
            # return HttpResponse('Password is not same')
        
        if len(userrrname)<5:
            messages.error(request, 'Username must be more than 5 characters')
            return render(request,'registration/signup.html')
            # return HttpResponse('Username must be more than 5 characters')
        
        if User.objects.filter(username=userrrname).exists():
            messages.error(request, 'Username has already been taken')
            return render(request,'registration/signup.html')
            # return HttpResponse('Username has already been taken')
        
        if User.objects.filter(email=useremail).exists():
            messages.error(request, 'Email has already been taken')
            return render(request,'registration/signup.html')
            
        
        userz = User.objects.create_user(username=userrrname, email=useremail, first_name=firstname, last_name=lastname)
        userz.set_password(passworda)

        userz.save()
        
        userz = authenticate(request, username=userrrname, password=passworda)
        login(request, userz)


        # return HttpResponse('Account Creation, Successful!')
        # return render(request, 'registration/signup.html')
        return redirect('home')
        

        

class Login(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        userrrname = request.POST['username']
        passworda = request.POST['password']
        if not User.objects.filter(username=userrrname).exists():
            messages.error(request, 'username not found in our database')
            return render(request, 'registration/login.html')
            # return HttpResponse('Username not found,try again.')
        
        if passworda and userrrname:
            userz = authenticate(request, username=userrrname, password=passworda) 
            if userz:
                login(request, userz)
                messages.success(request, 'Welcome back!')
                return redirect('home')
            
            messages.error(request, 'Incorrect password, review your input')
            return render(request, 'registration/login.html')
        # return HttpResponse('Incorrect password, try again')        

        
        # return render(request, 'registration/login.html')
       


def Logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


# Or       

# class Logout(View):
#     def get(self, request):
#         logout(request)
#         return HttpResponse('Logout successful')



class BaseProfileView(View):
    def get_profile_info(self, user):
        try:
            author = Author.objects.get(user=user)
            profile_complete = bool(
                author.display_name
                and author.full_name
                and author.profession
                and author.about_me
                and author.twitter_handle
                and author.facebook_handle
                and author.google_plus_handle
                and author.instagram_handle
            )

            profile_info = {
                'profile_image_url': author.profile.url if author.profile else None,
                'display_name': author.display_name,
                'full_name': author.full_name,
                'profession': author.profession,
                'about_me': author.about_me,
                'twitter_handle': author.twitter_handle,
                'facebook_handle': author.facebook_handle,
                'google_plus_handle': author.google_plus_handle,
                'instagram_handle': author.instagram_handle,
                'author': author,
                'userpost': Post.objects.filter(author=user, status='approved'),
                'userpending': Post.objects.filter(author=user, status='pending'),
                'engagement_counts': {
                    'user_engaging': Comment.objects.filter(post__author=user).count(),
                    'total_engaging': Comment.objects.all().count() if user.is_staff else 0
                },
            }

            return {'profile_info': profile_info, 'profile_complete': profile_complete}

        except Author.DoesNotExist:
            return {}


class ProfilePage(LoginRequiredMixin, BaseProfileView):
    login_url = 'login'

    def get(self, request):
        context = self.get_profile_info(request.user)

        if not context:
            return redirect('editpro')
        
        return render(request, 'registration/profile.html', context=context)
    

    def post(self, request):
        # Process the submitted form data
        
        return redirect('registration/profile.html')


# class AuthorProfile(BaseProfileView):
#     def get(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         author = post.author
#         context = self.get_profile_info(author)
#         return render(request, 'registration/profile.html', context=context)


class Subprofile(LoginRequiredMixin, BaseProfileView):
    login_url = 'login'

    def get(self, request):
        context = self.get_profile_info(request.user)

        if not context:
            return redirect('editpro')

        return render(request, 'registration/subprofile.html', context=context)

    

class AuthorProfile(BaseProfileView):
    def get(self, request, pk):
        try:
            # Fetch the author associated with the post's user
            author = Author.objects.get(user=pk)
        except Author.DoesNotExist:
            # Handle non-existent author
            return redirect('404')

        # Get the profile information
        context = self.get_profile_info(author.user)

        # Render the profile page
        return render(request, 'registration/subprofile.html', context=context)




class EditProfilePage(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        
        # author = get_object_or_404(Author, user=request.user)
        try:
            author = Author.objects.get(user=request.user)
        except Author.DoesNotExist:
            # If the user is not an author, redirect them to the page to become an author
            return redirect('beauthor')

        context = {
            'profile_info': {
                'profile_image_url': author.profile.url if author.profile else None,
                'display_name': author.display_name,
                'full_name': author.full_name,
                'profession': author.profession,
                'about_me': author.about_me,
                'twitter_handle': author.twitter_handle,
                'facebook_handle': author.facebook_handle,
                'google_plus_handle': author.google_plus_handle,
                'instagram_handle': author.instagram_handle,
            },
            'form_data': {
            'display_name': author.display_name,   
            'Fullname': author.full_name,
            'Profession': author.profession,
            'body': author.about_me,
            'Twitter': author.twitter_handle,
            'Facebook': author.facebook_handle,
            'Google_plus': author.google_plus_handle,
            'Instagram': author.instagram_handle,
            },
        }

        return render(request, 'registration/profiledit.html', context=context)


    def post(self, request):
        profile_image = request.FILES.get('postimage')
        display_name = request.POST.get('displayname')
        full_name = request.POST.get('Fullname')
        profession = request.POST.get('Profession')
        body = request.POST.get('body')
        twitter = request.POST.get('Twitter')
        facebook = request.POST.get('Facebook')
        google_plus = request.POST.get('Google +')
        instagram = request.POST.get('Instagram')

        author = Author.objects.get(user=request.user)


        # Get all form fields to be validated
        fields = {
            'display_name': display_name,
            'full_name': full_name,
            'profession': profession,
            'about_me': body,
            'twitter_handle': twitter,
            'facebook_handle': facebook,
            'google_plus_handle': google_plus,
            'instagram_handle': instagram
        }       


        # Check if any field contains the 'none' value
        for field_name, field_value in fields.items():
            if field_value == 'none':
                # If 'none' is found, prevent form submission and raise an error
                # return render(request, 'registration/profiledit.html', {'fields': fields})
                # return HttpResponse(f'{field_name} field cannot be "none". You can leave it empty, if you choose to')
                messages.success(request, f'{field_name} field cannot be "none". You can leave it empty, if you choose to')


        # Process the uploaded profile image (if any)
        if profile_image:
            author.profile = profile_image
            author.save()

        # Update author information
        author.display_name = display_name
        author.full_name = full_name
        author.profession = profession
        author.about_me = body
        author.twitter_handle = twitter
        author.facebook_handle = facebook
        author.google_plus_handle = google_plus
        author.instagram_handle = instagram
        author.save()
        messages.success(request, 'Profile Updated Successfully')

        return redirect('profiler')




class BecomeAuthor(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        # try:
        #     author = Author.objects.get(user=request.user)
        # except Author.DoesNotExist:
            return render(request, 'registration/beauthor.html')
        
        
    def post(self, request):
        profile_image = request.FILES.get('postimage')
        display_name = request.POST.get('displayname')
        full_name = request.POST.get('Fullname')
        profession = request.POST.get('Profession')
        body = request.POST.get('body')
        twitter = request.POST.get('Twitter')
        facebook = request.POST.get('Facebook')
        google_plus = request.POST.get('Google +')
        instagram = request.POST.get('Instagram')
        try:
            author = Author.objects.get(user=request.user)
        except Author.DoesNotExist:
            author = Author(user=request.user)    

        # Process the uploaded profile image (if any)
        if profile_image:
            author.profile = profile_image
            author.save()

        # Update author information
        author.display_name = display_name
        author.full_name = full_name
        author.profession = profession
        author.about_me = body
        author.twitter_handle = twitter
        author.facebook_handle = facebook
        author.google_plus_handle = google_plus
        author.instagram_handle = instagram
        author.save()
        messages.success(request, 'Author Status Successful')


        return redirect('profiler')    





# https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#top      for djanjo user documentation fields
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#top   foy django login/logout Documentation


