from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Note
from .forms import NoteForm


def note_list(request):
    """Display all notes with pinned notes first"""
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})


def note_create(request):
    """Create a new note"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, 'Note created successfully!')
            return redirect('note_list')
    else:
        form = NoteForm()
    
    return render(request, 'notes/note_form.html', {
        'form': form,
        'title': 'Create New Note',
        'button_text': 'Create Note'
    })


def note_edit(request, pk):
    """Edit an existing note"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'notes/note_form.html', {
        'form': form,
        'note': note,
        'title': 'Edit Note',
        'button_text': 'Update Note'
    })


def note_delete(request, pk):
    """Delete a note"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('note_list')
    
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


@require_http_methods(["POST"])
def note_toggle_pin(request, pk):
    """Toggle pin status of a note"""
    note = get_object_or_404(Note, pk=pk)
    note.is_pinned = not note.is_pinned
    note.save()
    
    status = 'pinned' if note.is_pinned else 'unpinned'
    messages.success(request, f'Note {status} successfully!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_pinned': note.is_pinned,
            'message': f'Note {status} successfully!'
        })
    
    return redirect('note_list')


def note_detail(request, pk):
    """Display a single note"""
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})
