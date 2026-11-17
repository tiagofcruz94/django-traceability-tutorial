from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarcassForm
from .models import DeboningLot


def lot_list(request):
    lots = DeboningLot.objects.all()
    return render(request, "traceability/lot_list.html", {"lots": lots})


def lot_detail(request, pk):
    lot = get_object_or_404(DeboningLot, pk=pk)
    return render(request, "traceability/lot_detail.html", {"lot": lot})


def carcass_create(request):
    """Show the new-carcass form and save it on a valid POST."""
    if request.method == "POST":
        form = CarcassForm(request.POST)
        if form.is_valid():
            carcass = form.save()
            messages.success(request, f"Carcaça {carcass.slaughter_number} adicionada.")
            # Redirect after POST so refreshing the page doesn't submit the form twice.
            return redirect("traceability:lot_list")
    else:
        form = CarcassForm()

    # Reached on GET (empty form) and on an invalid POST (form with the user's data and errors).
    return render(request, "traceability/carcass_form.html", {"form": form})
