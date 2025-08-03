from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password1')
        #     user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('performance_list')
        else:
            messages.error(request, "Помилка реєстрації.")


    else:
        form = UserCreationForm()

    return render(request, 'auth_system/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('performance_list')
            else:
                messages.error(request, "Неправильний логін або пароль.")
        else:
            messages.error(request, "Невірно заповнена форма.")
    else:
        form = AuthenticationForm()

    return render(request, 'auth_system/login.html', {'form': form})
