from django.shortcuts import render
from django import forms
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/entry.html", {
        "entry": None,
        "title": title.capitalize()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "title": title.capitalize()
        })
   