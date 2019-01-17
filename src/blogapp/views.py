from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import category,article,author, comment
from django.contrib.auth import authenticate,login, logout
from .forms import createForm, registerUser, createAuthor, categoryForm, commentForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages



# Create your views here.

def index(request):
    post= article.objects.all()
    search=request.GET.get('q')
    if search:
        post=post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)

        )
    paginator = Paginator(post, 4)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_aritle = paginator.get_page(page)
    contex={
        "post":total_aritle,
    }
    return render(request,'index.html', contex)

def getauthor (request, name):
    post_author=get_object_or_404(User, username=name) # don't working author button
    auth=get_object_or_404(author, name=post_author.id)
    post=article.objects.filter(article_author=auth.id)
    contex = {
        'auth':auth,
        'post': post,
    }
    return render(request, 'profile.html', contex)

def getsingle (request, id):
    post = get_object_or_404(article, id=id)
    first=article.objects.first()
    last=article.objects.last()
    getComment=comment.objects.filter(post=id)
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    form=commentForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.post=post
        instance.save()
        messages.success(request, 'Comment success')
        return redirect('profile')
       # return redirect('single_postid/<int:id>')  Vobon da need.
    contex = {
        'post': post,
        'first': first,
        'last' : last,
        'related':related,
        'form':form,
        'comment':getComment,
    }
    return render(request, 'single.html', contex)


def gettopic (request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category=cat.id)
    contex = {
        'post': post,
        'cat': cat,

    }
    return render(request, 'category.html', contex)


def getlogin (request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            user=request.POST.get('user')
            password=request.POST.get('pass')
            auth=authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return  redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Email or Password mismatch')
                return render(request, 'login.html')
    contex = {

    }
    return render(request, 'login.html', contex)

def getlogout (request):
    logout(request)
    # contex = {
    #     'msg':'Please login'
    # }
    # return render(request, 'login.html', contex)
    return redirect('login')


def getcreate (request):
    if request.user.is_authenticated:
        #auth_user=get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.article_author=auth_user
            instance.save()
            messages.success(request, 'Post success')
            return redirect('profile')
        contex = {
            'form': form
        }
        return render(request, 'create.html', contex)
    else:
        return redirect('login')


def getupdate(request, id):
    if request.user.is_authenticated:
        #auth_user=get_object_or_404(author, name=request.user.id)
        post=get_object_or_404(article, id=id)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.article_author=auth_user
            instance.save()
            messages.success(request, ' Article Update is Successfully ')
            return redirect('profile')
        contex = {
            'form': form
        }
        return render(request, 'create.html', contex)
    else:
        return redirect('login')

def getdelete(request, id):
    if request.user.is_authenticated:
        post=get_object_or_404(article, id=id)
        post.delete()
        messages.warning(request, ' Article  is Deleted ')
        return redirect('profile')
    else:
        return redirect('login')

def getprofile (request):
    if request.user.is_authenticated:
        user=get_object_or_404(User, id=request.user.id)
        post=article.objects.filter(article_author=user.id)
        contex = {
            'post':post,

        }
        return render(request, 'profile_view.html', contex)
    else:
       return redirect('login')

# def getprofile (request):
#     if request.user.is_authenticated:
#         user=get_object_or_404(User, id=request.user.id)
#         author_profile=author.objects.filter(name=user.id)
#         if author_profile:
#             author_user=get_object_or_404(author, name=request.user.id)
#             post=article.objects.filter(article_author=author_user.id)
#             contex = {
#                 'post':post,
#                 'user':author_user,
#             }
#             return render(request, 'profile_view.html', contex)
#         else:
#             form =createAuthor(request.POST or None, request.FILES or None)
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.name=user
#                 instance.save()
#                 messages.success(request, ' New Author Post  is Successfully  saved ')
#                 return redirect('profile')
#             contex = {
#                 'form': form,
#             }
#             return render(request, 'createAuthor.html', contex)
#     else:
#        return redirect('login')


def getregister(request):
    form=registerUser(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request, ' Register Successfully Completed')
        return redirect('login')
    contex = {
        'form': form,
    }
    return render(request, 'register.html', contex)


