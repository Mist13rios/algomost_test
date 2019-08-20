from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from main.forms import PollForm


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PollView(View):
    form_class = PollForm
    initial = {'key': 'value'}
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.validate_unique(exclude='id'):
                form.save()
                return redirect('showcase')
            else:
                return JsonResponse({'message': form.errors})
        else:
            return JsonResponse({'message': form.errors})


@method_decorator(csrf_exempt, name='dispatch')
class AuthUser(View):
    @staticmethod
    def get(request,  *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('index')
        else:
            template_name = 'login.html'
            form = AuthenticationForm(request)
            return render(request, template_name, {'form': form})

    @staticmethod
    def post(request,  *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return JsonResponse({'message': 'Wrong username/password'})


@method_decorator(login_required, name='dispatch')
class ShowcaseView(View):
    template_name = "showcase/showcase.html"


@method_decorator(login_required, name='dispatch')
class CartView(View):
    template_name = "cart.html"
