from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage

from .tasks import send_email_task
from .models import MessageBoard
from .forms import MessageCreateForm


class MessageBoardView(LoginRequiredMixin, FormView):
    template_name = "messageboard/index.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("messageboard:messageboard")
    _context_defaults = {
        "title": "Messages ...",
        "description": "Liste des membres du club avec option de filtrage.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messageboard"] = get_object_or_404(MessageBoard, id=1)
        context["are_subscribe"] = "Vous êtes inscrit!"
        context["subscribe"] = "S'inscrire"
        context["unsubscribe"] = "Se désinscrire"
        context["subscriber"] = "Abonné"
        context["informations"] = (
            "Inscrivez-vous pour recevoir les informations et les résultats du club."
        )
        context["not_informations"] = (
            "Vous recevrez des informations et des résultats du club."
        )
        context.update(self._context_defaults)
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

    def get_context_data(self, **kwargs):
        return {
            "newsletter_title": "Newsletter...",
            "newsletter_description": "Description des résultats et des projets du club",
            "greeting_hello": "Bonjour",
            "newsletter_welcome_message": "Bienvenue dans notre bulletin mensuel!",
            "club_updates_notice": "Soyez attentif aux informations fournies par le club.",
            "website_link_text": "Accès au site",
            "news_title_escrime": "Actu Escrime Mandelieu",
            "message_appreciation": "Merci, vous êtes géniaux! 😎",
            "gratitude_message": "Merci pour vos propositions, vos accompagnements, vos commentaires et votre soutien! 🥰",
            "club_support_title": "Soutenez le club ⚔️",
            "support_message": "✨ Rejoignez-nous sur les réseaux sociaux, partagez vos idées💡 et/ou images📸 avec nous. ✨",
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def test_func(self):
        return self.request.user.is_staff
