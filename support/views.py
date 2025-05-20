from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SupportTicket
from .forms import SupportTicketForm


@login_required
def support_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "support/support_list.html", {"tickets": tickets})


@login_required
def support_new(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('support_list')
    else:
        form = SupportTicketForm()

    return render(request, 'support/support_new.html', {"form": form})


@login_required
def support_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk, user=request.user)
    return render(request, 'support/support_detail.html', {'ticket': ticket})
