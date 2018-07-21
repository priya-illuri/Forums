from django import forms
from django.views import View
from django.shortcuts import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

def index(request):
    return redirect("login")

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("login")

class SignupForm(forms.Form):

    first_name=forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','place-holder':'firstname'})
    )

    last_name=forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','place-holder':'lastname'})
    )

    username=forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','place-holder':'username'})
    )

    password=forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control','place-holder':'password'})
    )


class LoginForm(forms.Form):

    username=forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','place-holder':'username'})
    )

    password=forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control','place-holder':'password'})
    )



class SignupController(View):
    def get(self,request):
        form=SignupForm
        template_name='signup.html'
        return render(request,template_name,{'form':form})

    def post(self,request):
        form=SignupForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(**form.cleaned_data)
            user.save()

            user=authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request,user)
                return redirect("questions_html")
            else:
                template_name = 'templates/signup.html'
                return render(request, template_name, {'form': form})

        else:
            template_name='templates/signup.html'
            return render(request, template_name, {'form': form})



class LoginController(View):
    def get(self,request):
        form=LoginForm
        template_name='login.html'
        return render(request,template_name,{'form':form})

    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():


            user=authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request,user)
                return redirect("questions_html")
            else:
                return redirect("signup")
                # template_name = 'templates/signup.html'
                # return render(request, template_name, {'form': form})

        else:
            return redirect("signup")
            # template_name='templates/signup.html'
            # return render(request, template_name, {'form': form})
