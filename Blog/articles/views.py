from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Article
from .forms import LoginForm, UserRegistration, ArticleRegistrationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.

def article_list(request):
    article_list = Article.objects.all().order_by('-published')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request=request, template_name='article.html', context={'article_list':articles, 'page': page})


def article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request=request, template_name='details.html', context={'article':article})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])

            if user is not None:
                login(request=request, user=user)
                return HttpResponse("You are authenticated")
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    
    return render(request=request, template_name='account/login.html', context={'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()

            return render(request, 'account/register_done.html', {'user_form': user_form})
    else:
        user_form = UserRegistration()

    return render(request, 'account/register.html', {'user_form': user_form})

def user_logout(request):
    try:
        logout(request)
    except BaseException as e:
        return HttpResponse(f'Error during logout: {str(e)}')
    
    return render(request=request, template_name='account/logout.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change.html', {'form': form})

@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

@login_required
def article_form(request):
    if request.method == 'POST':
        article_form = ArticleRegistrationForm(request.POST)

        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()

            return redirect('article_list')
    else:
        article_form = ArticleRegistrationForm()
    return render(request, 'account/add_article.html', {'article_form': article_form})

@login_required
def update_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ArticleRegistrationForm(request.POST or None, instance=article)

    if form.is_valid():
        form.save()
        return redirect('article_list')

    return render(request, 'account/update.html', {'form': form})

@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.delete()
    return redirect('article_list')

