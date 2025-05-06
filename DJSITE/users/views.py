from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#from orders.models import Order


def register(request):#заход в регистр вам дается форма потом заполн и отправл ее и проверка на валид(если все добра) и созд, сохр нового юзера
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:login')
        else:
            form = UserRegistrationForm
        
        return render(request, 'users/register.html', {'form': form})#3 контекст вот рендер указ какой шаблон будет рендериться
    

def user_login(request):
    if request.method ==  'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email') #Если форма прошла валидацию, данные помещаются в словарь cleaned_data. Теперь вы можете безопасно использовать эти данные вот для чего cl_data
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:catalog')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})
       
@login_required(login_url='/users/login') #это означ что ток авториз могут выйти из акка
def user_logout(request):
    logout(request)
    return redirect('users:login') 

