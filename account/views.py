from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import redirect, render
from django_email_verification import send_email

User = get_user_model()


from .forms import UserCreateForm


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
    return render(request, 'account/registration/email-verification-sent.html')