from django.shortcuts import redirect, render

from .util import *
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry(request, title):
    # Versuche, den Eintrag abzurufen
    entry_content = get_entry(title)

    # Überprüfe, ob der Eintrag existiert
    if entry_content is not None:
        # Konvertiere Markdown in HTML
        entry_content_html = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {"title": title, "content": entry_content_html})
    else:
        # Eintrag nicht gefunden, zeige Fehlerseite
        return render(request, "encyclopedia/entry_not_found.html", {"title": title})
    
def search(request):
    query = request.GET.get('q', '').upper()  # Konvertiere die Suchanfrage in Großbuchstaben
    entries = list_entries()

    matching_entries = [entry for entry in entries if query in entry.upper()]

    if matching_entries:
        # Wenn ein übereinstimmender Eintrag gefunden wurde, direkt zu diesem Eintrag umleiten.
        if len(matching_entries) == 1 and matching_entries[0].upper() == query:
            return redirect('entry', title=query)
        else:
            return render(request, 'encyclopedia/search_results.html', {'entries': matching_entries, 'query': query})
    else:
        # Wenn keine Übereinstimmung gefunden wurde, zur allgemeinen Suchergebnisseite umleiten.
        return render(request, 'encyclopedia/search_results.html', {'entries': entries, 'query': query})

def create_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Überprüfe, ob der Eintrag bereits existiert
        if get_entry(title) is not None:
            return render(request, 'encyclopedia/create_page.html', {'error': 'Eintrag existiert bereits', 'title': title, 'content': content})

        # Bearbeite den Content-String
        modified_content = f"# {title}\n\n{content}"

        # Speichere den neuen Eintrag
        save_entry(title, modified_content)

        # Umleitung zur neuen Seite
        return redirect('entry', title=title)
    else:
        return render(request, 'encyclopedia/create_page.html')

def edit(request, title):
    # Versuche, den Eintrag abzurufen
    entry_content = get_entry(title)

    # Überprüfe, ob der Eintrag existiert
    if entry_content is not None:
        if request.method == "POST":
            # Benutzer hat das Bearbeitungsformular gesendet
            new_content = request.POST.get('content')

            # Speichere die Bearbeitungen
            save_entry(title, new_content)

            # Umleitung zur Eintragsseite nach dem Speichern
            return redirect('entry', title=title)
        else:
            # Benutzer hat die Bearbeitungsseite aufgerufen, zeige das Formular an
            return render(request, 'encyclopedia/edit_page.html', {'title': title, 'content': entry_content})
    else:
        # Eintrag nicht gefunden, zeige Fehlerseite
        return render(request, 'encyclopedia/entry_not_found.html', {'title': title})

def random_page(request):
    entries = list_entries()

    if entries:
        random_entry = random.choice(entries)
        return redirect('entry', title=random_entry)
    else:
        return render(request, 'encyclopedia/entry_not_found.html', {'title': 'Random Page'})

def delete_entry(request, title):
    # Versuche, den Eintrag abzurufen
    entry_content = get_entry(title)

    # Überprüfe, ob der Eintrag existiert
    if entry_content is not None:
        # Lösche den Eintrag
        delete_entry_file(title)
        # Umleitung zur Indexseite nach dem Löschen
        return redirect('index')
    else:
        # Eintrag nicht gefunden, zeige Fehlerseite
        return render(request, "encyclopedia/entry_not_found.html", {"title": title})
