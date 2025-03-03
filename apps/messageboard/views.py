from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
import threading
from .tasks import send_email_task
from .models import MessageBoard
from .forms import MessageCreateForm


class MessageBoardView(LoginRequiredMixin, FormView):
    template_name = "messageboard/index.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("messageboard:messageboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messageboard"] = get_object_or_404(MessageBoard, id=1)
        return context

    def form_valid(self, form):
        messageboard = get_object_or_404(MessageBoard, id=1)
        if self.request.user in messageboard.subscribers.all():
            message = form.save(commit=False)
            message.author = self.request.user
            message.messageboard = messageboard
            message.save()
            # Utilisation de la classe EmailService
            # EmailService.send_email(message)
        else:
            messages.warning(self.request, "You need to be Subscribed!")
            return redirect(self.success_url)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messageboard = get_object_or_404(MessageBoard, id=1)
        if request.user not in messageboard.subscribers.all():
            messageboard.subscribers.add(request.user)
        else:
            messageboard.subscribers.remove(request.user)
        return redirect("messageboard:messageboard")


class EmailService:
    @staticmethod
    def send_email(message):
        messageboard = message.messageboard
        subscribers = messageboard.subscribers.all()

        for subscriber in subscribers:
            subject = f"New Message from {message.author.profile.name}"
            body = f"{message.author.profile.name}: {message.body}\n\nRegards from\nMy Message Board"

            # Utilisation de Celery
            send_email_task.delay(subject, body, subscriber.email)

            # Envoi alternatif avec threading (au cas où Celery n'est pas configuré)
            # threading.Thread(target=EmailService.send_email_thread, args=(subject, body, subscriber)).start()

    @staticmethod
    def send_email_thread(subject, body, subscriber):
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.send()


class NewsletterView(UserPassesTestMixin, View):
    template_name = "messageboard/newsletter.html"

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
