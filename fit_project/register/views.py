from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            print("form is valid")
            form.save()

        return redirect("/")

    else:
        form = RegisterForm()

    return render(response,"register/register.html",{"form":form})


def login(response ):
    if response.user.is_authenticated:
        return redirect("/")

    if response.method == 'GET':

        if 'signup' in response.GET.values():
            signup = True
        else:
            signup = False

        context = ''
        form = RegisterForm()
        return render(response, 'registration/login.html', {'context': context, 'form':form, 'signup': signup})

    elif response.method == 'POST':

        if response.POST.get('Sign-in'):
            username = response.POST.get('loginUsername', '')
            username = username.strip()
            password = response.POST.get('password', '')
            user = authenticate(response, username=username, password=password)

            if user is not None:
                auth_login(response, user)
                return redirect("/")
                # Redirect to a success page

            else:
                context = 'Username or password does not match' # to display error
                form = RegisterForm()
                return render(response, 'registration/login.html', {'context': context,'form':form})
        else:

            form = RegisterForm(response.POST)
            err=''
            signup=False
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(response, username=username, password=password)

                if user is not None:
                    auth_login(response, user)
                    return redirect("/")
            else:
                signup = True
                for er in form.errors.as_data().values():
                    err = str(er[0])
                    err = err[2:-2]
                    if err == 'This field is required.':
                        err = 'All fields are required'
                    break

            return render(response, 'registration/login.html', {'err': err, 'form':form, 'signup': signup})
