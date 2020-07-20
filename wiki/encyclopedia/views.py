from django.shortcuts import render
from django import forms
from . import util
import markdown2
import random

class NewTaskForm(forms.Form):
    entry_search = forms.CharField(label="Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTaskForm()
    })

def view_entry(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/entry.html", {
        "entry": None,
        "title": title.capitalize(),
        "form": NewTaskForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "title": title.capitalize(),
            "form": NewTaskForm()
        })
   
# Search for an existing entry in the encyclopedia
def entry_search(request):
    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the search word from the 'cleaned' version of form data
            search_keyword = form.cleaned_data["entry_search"]

            # See if search word matches any of the entry titles exactly
            all_entries = util.list_entries()
            
            # Check for exact matches
            if search_keyword.upper() in (entry.upper() for entry in all_entries):
                # Keyword matches exactly, render that page
                return view_entry(request, search_keyword)
                

            # Check for partial matches
            entry_subset = []
            for entry in all_entries:
                if search_keyword.upper() in entry.upper():
                    entry_subset.append(entry)
            
            if len(entry_subset) > 0: # We have some partial matches
                return render(request, "encyclopedia/search_results.html", {
                    "entries": entry_subset,
                    "form": NewTaskForm()
                })
                        

            # No matches
            return render(request, "encyclopedia/search_results.html", {
                    "entries": None,
                    "form": NewTaskForm()
                })

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/index.html", {
                "form": form
            })

    return render(request, "encyclopedia/index.html", {
        "form": NewTaskForm()
    })

# Take user to random encyclopedia entry
def random_page(request):
    # Find all current encyclopedia entries
    print("funtion called")
    all_entries = util.list_entries()
    print(all_entries)
    print("%%%%%%%%%%%%")
    # Pull random entry title
    random_entry_title = random.choice(all_entries)
    # Display entry
    return view_entry(request, random_entry_title)