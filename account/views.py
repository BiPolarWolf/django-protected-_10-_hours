from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import redirect, render
from django_email_verification import send_email

User = get_user_model()


from .forms import UserCreateForm ,LoginForm ,UserUpdateForm


def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            #create new User

            user = User.objects.create(email=user_email, username=user_username, password=user_password)

            user.is_active = False
            send_email(user)
            return redirect('account:email-verification-sent')   

    else:
        form = UserCreateForm()
        return render(request, 'account/registration/register.html', {'form': form})
    

def email_verification_sent(request):
    return render(request, 'account/email/email-verification-sent.html')


def login_user(request):
    form = LoginForm()

    if request.user.is_authenticated:
            return redirect('shop:products')

    if request.method == 'POST':
        
        form = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            print('Vse kruto')
            login(request, user)
            return redirect('account:dashboard')
        else:
            print('incorrect username or password')
            messages.info('Username or password is incorrect')
            return redirect('account:login')

    return render(request,'account/login/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('shop:products')

@login_required(login_url='account:login')
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')

@login_required(login_url='account:login')
def profile_management(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {'form': form}
    return render(request, 'account/dashboard/profile_management.html', context)


@login_required(login_url='account:login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    return render(request,'account/dashboard/account_delete.html')