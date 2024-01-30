from django.urls import path
from .views import Create_userpost, Comments, Edit_userpost, Delete_userpost, Pendingpage, ApprovePost, UnapprovePost, Delete_comments, CreateCategory, DeleteCategory


urlpatterns = [
    path("", Create_userpost.as_view(), name='createpost'),
    path("editpost/<int:pk>/", Edit_userpost.as_view(), name='editor'),
    path("penpager/<int:pk>/", Pendingpage.as_view(), name='penpage'),
    path("commen/<int:pk>/", Comments.as_view(), name='commentas'),
    path("deletapost/<int:pk>/", Delete_userpost.as_view(), name='deleta'),
    path("deletacomm/<int:pk>/", Delete_comments.as_view(), name='commdeleta'),
    path("approvepost/<int:pk>/", ApprovePost.as_view(), name='approver'),
    path("unapprovepost/<int:pk>/", UnapprovePost.as_view(), name='unapprover'),
    path("cat", CreateCategory.as_view(), name='catcreator'),
    path("deletacat/<int:pk>/", DeleteCategory.as_view(), name='catdeleta'),
]