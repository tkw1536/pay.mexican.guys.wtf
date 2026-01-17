import random

from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import WhoPays


MESSGAES = [
    "Good news, {user}! Tonight’s dinner is generously sponsored by <b>{payer}</b> 🎉",
    "Relax, {user}. Wallets stay closed - <b>{payer}</b> has this one.",
    "{user}, you may order dessert. <b>{payer}</b> already accepted their fate.",
    "Today’s menu is à la carte, courtesy of <b>{payer}</b>.",
    "Hear ye, hear ye! By ancient office law, <b>{payer}</b> shall fund this feast.",
    "History will remember this dinner... mostly because <b>{payer}</b> paid for it.",
    "The council has decided: <b>{payer}</b> will take one for the team.",
    "A moment of silence for <b>{payer}</b>’s bank account.",
    "Billing request successfully assigned to <b>{payer}</b> ✅",
    "Transaction pending… awaiting <b>{payer}</b>’s approval.",
    "{user}, you are in read-only mode. <b>{payer}</b> has write access to the bill.",
]

OWN_MESSAGES = [
    "Oops, {user}, looks like you’re paying tonight 😬",
    "{user}, your wallet called… it’s time to say goodbye.",
    "The council has decided: {user} takes one for the team.",
    "{user}, may your coffee be strong and your credit limit higher.",
    "Brace yourself, {user}. The bill is coming.",
    "{user}, may your generosity be rewarded... eventually.",
]


def index(request):
    who_pays = get_object_or_404(WhoPays, pk=1)
    payer_name = who_pays.user.first_name or who_pays.user.username
    message = f"It's <b>{payer_name}</b>'s turn"
    if request.user:
        user_name = request.user.first_name or request.user.username
        message = random.choice(MESSGAES).format(user=user_name, payer=payer_name)
    if request.user == who_pays.user:
        message = random.choice(OWN_MESSAGES).format(user=user_name)

    context = {
        "message": message,
        "who_pays": who_pays,
    }
    return render(request, "pay_mexican_guys/pay_mexican_guys.html", context)


@permission_required("pay_mexican_guys.change_whopays")
def rotate(request):
    users = list(User.objects.all().order_by("pk"))
    who_pays = get_object_or_404(WhoPays, pk=1)
    current_user = who_pays.user

    idx = users.index(current_user)
    next_user = users[(idx + 1) % len(users)]

    who_pays.user = next_user
    who_pays.last_change = datetime.now()
    who_pays.save()

    return redirect(index)
