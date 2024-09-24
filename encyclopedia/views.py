from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util

import markdown2

from random import choice

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea(), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    form = NewPageForm()
    return render(request, "encyclopedia/new_page.html",{
       "form": form, "title": "Create a New Page" 
    })

def create_newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "error": "Error: Page Already Exists"
                })
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": util.convert(content)
            })    
    return new_page(request)

def edit(request, title):
    return render(request, "encyclopedia/edit_page.html", {
        "content": util.get_entry(title), "title": title
    })

def update_page(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": util.convert(content)
            })

def entry(request, title):
    if title == "*search*":
        query = request.GET['q']
        entries = []
        for entry in util.list_entries():
            if query == entry:
                return render(request, "encyclopedia/entry.html", {
                    "title": query, "content": util.convert(util.get_entry(query)) 
                })
            elif query in entry:
                entries.append(entry)
        return render(request, "encyclopedia/search_substrings.html", {
            "entries": entries, "length": len(entries) 
        })
    if title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
        "title": title, "content": util.convert(util.get_entry(title))   
    })
    return render(request, "encyclopedia/error.html", {
        "error": "Error: Page not Found (404)" 
    })


def random(request):
    random_entry = choice(util.list_entries())
    return entry(request, random_entry)


