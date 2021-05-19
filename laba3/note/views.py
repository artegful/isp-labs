from django.shortcuts import render
from .models import Note

def notes_list(request):
    notes = Note.objects.order_by('create_time')
    return render(request, 'note/notes_list.html', {'notes': notes})