from django.http import JsonResponse
from .models import Note
from django.shortcuts import render, redirect


def get_all_notes(request):
    notes = Note.objects.all()

    if not notes.exists():
        return JsonResponse({"message": "No notes found."}, status=404)

    data = [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for note in notes
    ]
    return JsonResponse(data, safe=False)


def main_page(request):
    notes = Note.objects.all()

    if not notes.exists():
        return JsonResponse({"message": "No notes found."}, status=404)

    return render(request, "main_page.html", {"notes": notes})


def update_note(request):
    if request.method == "POST":
        note_id = request.POST["note_id"]
        note_title = request.POST["title"]
        note_content = request.POST["content"]

        note = Note.objects.get(id=note_id)
        note.title = note_title
        note.content = note_content
        note.save()

        return redirect("main_page")

    return redirect("main_page")
