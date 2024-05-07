from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from .models import WhoPays

def index(request):
    context = {
        "who_pays": get_object_or_404(WhoPays, pk=1)
    }
    return render(request, "pay_mexican_guys/pay_mexican_guys.html", context)

@permission_required("pay_mexican_guys.change_whopays")
def rotate(request):
    users = list(User.objects.all().order_by("pk"))
    who_pays = get_object_or_404(WhoPays, pk=1)
    current_user = who_pays.user

    idx = users.index(current_user)
    next_user = users[(idx+1)%len(users)]

    who_pays.user = next_user
    who_pays.save()

    return redirect(index)
