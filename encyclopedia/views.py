from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import markdown
from . import util
from django import forms

import random


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def show_article(request, title):
    article = util.get_entry(title)
    if article == None:
        article = no_article(title)

    return render(
        request,
        "encyclopedia/article.html",
        {"article": markdown(article), "title": title},
    )


def no_article(title):
    return f'Article "{title}" not found. Try again'


def search(request):
    query = request.GET["q"]
    article = util.get_entry(query)
    if not article == None:
        return HttpResponseRedirect(
            reverse("encyclopedia:article", kwargs={"title": query})
        )

    result_list = []
    entries_list = util.list_entries()
    for i in entries_list:
        if i.lower().find(query.lower()) >= 0:
            result_list.append(i)

    if len(result_list) == 0:
        result_list = False

    return render(
        request,
        "encyclopedia/search.html",
        {
            "results": result_list,
        },
    )


def random_page(request):
    entries_list = util.list_entries()
    rand_entry_index = random.randint(0, len(entries_list) - 1)
    return HttpResponseRedirect(
        reverse(
            "encyclopedia:article", kwargs={"title": entries_list[rand_entry_index]}
        )
    )


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "10"}))


def create(request):

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = request.POST["title"]
            content = request.POST["content"]
    
            if title in [x.lower() for x in util.list_entries()]:
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry with such name already exists, try again."
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(
                    reverse(
                        "encyclopedia:article",
                        kwargs={"title": title},
                    )
                )
                
    return render(
        request,
        "encyclopedia/create.html",
        {
            "form": NewEntryForm,
        },
    )
    
def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = request.POST["title"]
            content = request.POST["content"]

            util.save_entry(title, content)
            return HttpResponseRedirect(
                reverse(
                    "encyclopedia:article",
                    kwargs={"title": title},
                )
            )
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": NewEntryForm(initial={
                'title': title,
                'content': util.get_entry(title),
            }),
            "title": title,
        })
