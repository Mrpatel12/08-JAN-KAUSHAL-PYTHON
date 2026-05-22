from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Studinfo
from .forms import PostForm, studform
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PostForm()

    return render(request, 'home.html', {
        'form': form,
        'posts': posts
    })
def update(request,id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        post = get_object_or_404(Post, id=id)
        form = PostForm(instance=post)
    return render(request, 'edit.html', {'form': form})
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('home')

def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_Valid():
            form.save()
            return redirect('login')
    else:    
        form = UserCreationForm()

    return render(request,'register.html',{'form':form})
                   
def showdata(request):
    data = Studinfo.objects.all()
    return render(request, 'showdata.html', {'data': data})   

def adddata(request):
    if request.method == 'POST':
        form = studform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showdata')   
    else:
        form = studform()

    return render(request, 'update.html', {'form': form})
            