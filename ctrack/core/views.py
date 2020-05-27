from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home_page(request):
    if request.user.is_stakeholder():
        return render(request, "pages/stakeholder_home.html")
    else:
        return render(request, "pages/home.html")
