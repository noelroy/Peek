from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .forms import UserForm, QuoteForm, UserProfileForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction

from django.views import  generic
from django.views.generic.edit import UpdateView

from .models import Quotes, User

import requests

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'quotes/login.html')
    else:
        r = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=10')
        ranquote = r.json()
        ranquote = {'ranquote': ranquote}
        return render(request, 'quotes/index.html', ranquote)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'quotes/login.html', context)


def login_user(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('quotes:index')
                else:
                    return render(request, 'quotes/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'quotes/login.html', {'error_message': 'Invalid login'})
        return render(request, 'quotes/login.html')
    else:
        return redirect('quotes:index')


def register(request):
    if not request.user.is_authenticated():
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    return render(request, 'quotes/login.html', {'success_message': 'Your account has been successfully created'})
        context = {
            "form": form,
        }
        return render(request, 'quotes/register.html', context)
    else:
        return redirect('quotes:index')

@login_required(login_url='/quotes/login_user/')
def quote_list(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        quotes = Quotes.objects.filter(user=request.user).order_by('created_date')
        return render(request, 'quotes/quotes_list.html', {'quote_list': quotes})


#def quote_detail(request, pk):
#    if not request.user.is_authenticated():
#        return render(request, 'quotes/login.html')
#    else:
#        quote = get_object_or_404(Quotes, pk=pk)
#        return render(request, 'quotes/quote_detail.html', {'quote': quote})

def delete_quote(request, pk):
    quote = Quotes.objects.get(pk=pk)
    quote.delete()
    quotes = Quotes.objects.filter(user=request.user).order_by('created_date')
    return render(request, 'quotes/quotes_list.html', {'quote_list': quotes})

def create_quote(request):
    if not request.user.is_authenticated():
        return render(request, 'quotes/login.html')
    else:
        form = QuoteForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return render(request, 'quotes/quote_detail.html', {'quote': quote})
        context = {
            "form": form,
        }
        return render(request, 'quotes/quotes_form.html', context)

class QuoteUpdate(UpdateView):
    model = Quotes
    fields = ['quote_text','category_name']

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            user_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('quotes:profile_detail',request.user.pk)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'quotes/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request,pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = user.profile
    return render(request, 'quotes/profile.html', {'user': user, 'profile':user_profile})