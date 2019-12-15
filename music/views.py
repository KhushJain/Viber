from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from .models import Album

def index(request):
    all_album = Album.objects.all()
    return render(request, "music/index.html",{"all_album" :all_album})

def detail(request,album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, "music/detail.html", {"album":album})


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return render(request, self.template_name,{'form':form})



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('music:index')
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')
