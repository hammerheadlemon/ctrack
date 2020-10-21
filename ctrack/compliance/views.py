from django.shortcuts import render

from ctrack.caf.models import CAF


def overview(request):
    cafs = CAF.objects.all()
    context = {"cafs": cafs}
    return render(request, "compliance/overview.html", context)

