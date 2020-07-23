from django.shortcuts import render, redirect
from django import forms
from . import util
import markdown2
import random

class NewSearchForm(forms.Form):
    entry_search = forms.CharField(label="Search Encyclopedia")

class NewCreateForm(forms.Form):
    title = forms.CharField(label="Page Title")
    markdown_content = forms.CharField(label = "Markdown Content", widget=forms.Textarea)

class NewEditForm(forms.Form):
    markdown_content = forms.CharField(label = "Markdown Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": NewSearchForm()
    })

def view_entry(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/entry.html", {
        "entry": None,
        "title": title.capitalize(),
        "search_form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "title": title.capitalize(),
            "search_form": NewSearchForm()
        })
   
# Search for an existing entry in the encyclopedia
def entry_search(request):
    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewSearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the search word from the 'cleaned' version of form data
            search_keyword = form.cleaned_data["entry_search"]

            # See if search word matches any of the entry titles exactly
            all_entries = util.list_entries()
            
            # Check for exact matches
            if search_keyword.upper() in (entry.upper() for entry in all_entries):
                # Keyword matches exactly, redirect to that page
                return redirect('/wiki/' + search_keyword)
    
                
            # Check for partial matches
            entry_subset = []
            for entry in all_entries:
                if search_keyword.upper() in entry.upper():
                    entry_subset.append(entry)
            
            if len(entry_subset) > 0: # We have some partial matches
                return render(request, "encyclopedia/search_results.html", {
                    "entries": entry_subset,
                    "search_form": NewSearchForm()
                })
                        

            # No matches
            return render(request, "encyclopedia/search_results.html", {
                    "entries": None,
                    "search_form": NewSearchForm()
                })

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/index.html", {
                "search_form": form
            })

    return render(request, "encyclopedia/index.html", {
        "search_form": NewSearchForm()
    })

# Take user to random encyclopedia entry
def random_page(request):
    # Find all current encyclopedia entries
    all_entries = util.list_entries()
    # Pull random entry title
    random_entry_title = random.choice(all_entries)
    # Display entry
    #return view_entry(request, random_entry_title)
    return redirect('/wiki/' + random_entry_title)

# Create a new encyclopedia entry
def create_new_page(request):
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewCreateForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title and markdown content
            title = form.cleaned_data["title"].capitalize()
            markdown_content = form.cleaned_data["markdown_content"]

            #TODO: fix text area appearance, its way too big





            # Entry does not yet exist
            if util.get_entry(title) is None:
                # Save entry and bring user to the new entry's page
                util.save_entry(title, markdown_content)
                return redirect("/wiki/" + title)

            # If entry already exists, present user with error message
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "An encyclopedia entry already exists under this title",
                    "search_form": NewSearchForm()
                })
        
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create.html", {
                "create_form": form,
                "search_form": NewSearchForm()
            })
        

    else:
        return render(request, "encyclopedia/create.html", {
            "create_form": NewCreateForm(),
            "search_form": NewSearchForm()
        })

# Lets used edit entry's markdown content
def edit_page(request, title):
    markdown_content = util.get_entry(title)

    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEditForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the markdown content
            markdown_content = form.cleaned_data["markdown_content"]

            #TODO: fix text area appearance, its way too big



            # Save entry and bring user to the entry's page
            util.save_entry(title, markdown_content)
            return redirect("/wiki/" + title)
        
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit.html", {
            "edit_form": form,
            "search_form": NewSearchForm(),
            "title": title
        })
        

    else:
        return render(request, "encyclopedia/edit.html", {
            "edit_form": NewEditForm({'markdown_content': markdown_content}),
            "search_form": NewSearchForm(),
            "title": title
        })