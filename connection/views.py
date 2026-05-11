from django.shortcuts import render, redirect
from .forms import ClientForm


def create_client(request):

    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            client_app = form.save()
            print("client_success")  # change to your url name


    else:
        form = ClientForm()

    return render(request, "client_form.html", {"form": form})