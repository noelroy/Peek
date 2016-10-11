from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .forms import UserForm
from .models import Category, Tags, Quotes, QuotesTags
from django.contrib.auth.decorators import login_required

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'quotes/login.html')
    else:
        return render(request, 'quotes/index.html')


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
                    return render(request, 'quotes/index.html')
                else:
                    return render(request, 'quotes/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'quotes/login.html', {'error_message': 'Invalid login'})
        return render(request, 'quotes/login.html')
    else:
        return render(request, 'quotes/index.html')


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
        return render(request, 'quotes/index.html')


@login_required(login_url='/quotes/login_user/')
def quote_list(request):
    quotes = Quotes.objects.order_by('created_date')
    return render(request, 'quotes/quotes_list.html', {'quote_list': quotes})


@login_required(login_url='/quotes/login_user/')
def quote_detail(request, pk):
    quote = get_object_or_404(Quotes, pk=pk)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})
