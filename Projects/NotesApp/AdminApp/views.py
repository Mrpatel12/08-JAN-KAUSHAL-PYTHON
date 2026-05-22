from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from UserApp.models import CustomUser, Note
from .forms import AdminUserForm

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='login')(view_func)

@superuser_required
def admin_dashboard(request):
    total_users = CustomUser.objects.filter(is_superuser=False).count()
    total_notes = Note.objects.count()
    verified_users = CustomUser.objects.filter(is_verified=True, is_superuser=False).count()
    recent_users = CustomUser.objects.filter(is_superuser=False).order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_notes': total_notes,
        'verified_users': verified_users,
        'recent_users': recent_users,
    }
    return render(request, 'AdminApp/dashboard.html', context)

@superuser_required
def user_list(request):
    query = request.GET.get('q')
    users = CustomUser.objects.filter(is_superuser=False).order_by('-date_joined')
    if query:
        from django.db.models import Q
        users = users.filter(
            Q(fullname__icontains=query) | 
            Q(email__icontains=query) | 
            Q(city__icontains=query) |
            Q(mobile__icontains=query)
        )
    return render(request, 'AdminApp/user_list.html', {'users': users})

@superuser_required
def add_user(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            messages.success(request, f'User {user.fullname} added successfully.')
            return redirect('admin_user_list')
    else:
        form = AdminUserForm()
    return render(request, 'AdminApp/user_form.html', {'form': form, 'title': 'Add User'})

@superuser_required
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.fullname} updated successfully.')
            return redirect('admin_user_list')
    else:
        form = AdminUserForm(instance=user)
    return render(request, 'AdminApp/user_form.html', {'form': form, 'title': 'Edit User'})

@superuser_required
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        name = user.fullname
        user.delete()
        messages.success(request, f'User {name} deleted successfully.')
        return redirect('admin_user_list')
    return render(request, 'AdminApp/user_confirm_delete.html', {'user': user})

@superuser_required
def toggle_user_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    status = "unblocked" if user.is_active else "blocked"
    messages.success(request, f'User {user.fullname} has been {status}.')
    return redirect('admin_user_list')

@superuser_required
def admin_note_list(request):
    query = request.GET.get('q')
    notes = Note.objects.all().order_by('-updated_at')
    if query:
        from django.db.models import Q
        notes = notes.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(user__fullname__icontains=query) |
            Q(user__email__icontains=query)
        )
    return render(request, 'AdminApp/note_list.html', {'notes': notes})

@superuser_required
def admin_delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        title = note.title
        note.delete()
        messages.success(request, f'Note "{title}" deleted successfully.')
        return redirect('admin_note_list')
    return render(request, 'AdminApp/note_confirm_delete.html', {'note': note})
