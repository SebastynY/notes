from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.views import generic
from django.urls import reverse_lazy
from core.forms import NotesForm
from core.models import Note


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('main')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


def index(request: WSGIRequest):
    if request.user.is_authenticated:
        count_notes = Note.objects.filter(author=request.user).count()
        context = {
            'count_notes': count_notes,
        }
    else:
        context = {
            'count_notes': 0,
        }
    return render(request, 'core/index.html', context=context)


@login_required
def get_notes(request: WSGIRequest):
    context = {
        'notes': Note.objects.filter(author__id=request.user.id),
    }
    return render(request, 'core/notes_list.html', context=context)


@login_required
def add_notes(request: WSGIRequest):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author_id = request.user.id
            form.save()
            return redirect('notes_list')
    else:
        form = NotesForm()

    context = {
        'form': form,
    }
    return render(request, 'core/add_notes.html', context=context)


@login_required
def delete_notes(request: WSGIRequest, note_id: int):
    get_object_or_404(Note, pk=note_id).delete()
    return redirect('notes_list')


@login_required
def edit_notes(request: WSGIRequest, note_id: int):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NotesForm(instance=note)

    context = {
        'form': form,
    }
    return render(request, 'core/add_notes.html', context=context)
