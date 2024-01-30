from .models import Category


def category_list(request):
    global_list = Category.objects.all()
    return{
        'global_lista' : global_list
    }

# def category_list(request):
#     global_list = Category.objects.all()
#     global_list={
#         'global_lista' : global_list
#     }
#     return global_list
