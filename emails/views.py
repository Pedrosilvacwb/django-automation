from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import EmailForm
from .models import Subscriber
from .tasks import send_email_task


# Create your views here.
def send_email(request: HttpRequest):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email_form = form.save()

            mail_subject = request.POST.get("subject")
            message = request.POST.get("body")

            email_list = email_form.email_list

            subscribers = Subscriber.objects.filter(email_list=email_list)

            to_email = [email.email_address for email in subscribers]

            attachment = None
            if email_form.attachment:
                attachment = email_form.attachment.path

            send_email_task.delay(
                mail_subject=mail_subject,
                message=message,
                to_email=to_email,
                attachment=attachment,
            )

            messages.success(request, "Email sent successfullt!")
            return redirect("send_email")
        return
    else:
        form = EmailForm()
        context = {"form": form}
        return render(request, "email/send-email.html", context)
