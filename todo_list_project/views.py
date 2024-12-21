from django.http import JsonResponse, HttpResponseBadRequest
from .models import Note
from django.shortcuts import render, redirect, get_object_or_404


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
        try:
            note_id = request.POST["note_id"]
            note_title = request.POST["title"]
            note_content = request.POST["content"]

            if not note_id or not note_title or not note_content:
                return HttpResponseBadRequest("Missing required fields.")

            note = get_object_or_404(Note, id=note_id)

            note.title = note_title.strip()
            note.content = note_content.strip()
            note.save()

            return redirect("main_page.html")
        except Exception as e:
            return render(
                request,
                "error.html",
                {"message": f"An error occurred while updating the note: {str(e)}"},
            )

    return redirect("main_page.html")


def create_note(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            content = request.POST.get("content")

            if not title or not content:
                return HttpResponseBadRequest("Both title and content are required.")

            Note.objects.create(title=title.strip(), content=content.strip())
            return redirect("main_page.html")
        except Exception as e:
            return render(
                request,
                "error.html",
                {"message": f"An error occurred while creating the note: {str(e)}"},
            )
    return redirect("create_note.html")
