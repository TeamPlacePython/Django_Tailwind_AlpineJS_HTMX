from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.views.generic.edit import FormView
import logging

from apps.constant import CONSTANT_SAVE, CONSTANT_CANCEL
from .models import Post, Tag, Comment, Reply
from .forms import (
    ReplyCreateForm,
    PostCreateForm,
    PostEditForm,
    CommentCreateForm,
)

logger = logging.getLogger(__name__)


# 🏠 Page d'accueil avec pagination
class PostIndexView(ListView):
    model = Post
    template_name = "posts/post_index.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag")
        if tag_slug:
            return Post.objects.filter(tags__slug=tag_slug)
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = (
            get_object_or_404(Tag, slug=self.kwargs.get("tag"))
            if "tag" in self.kwargs
            else None
        )
        context["post_index_title"] = "Le blog des adhérents ..."
        return context


# 📌 Création d'un post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("posts:post_index")
    _context_defaults = {
        "post_create_title": "Nouveau post ...",
        "post_create_description": "",
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user

        if not self.request.FILES.get("image"):
            messages.error(self.request, "Vous devez ajouter une image !")
            return self.form_invalid(
                form
            )  # Afficher le formulaire avec l'erreur

        post.image = self.request.FILES["image"]
        post.save()
        form.save_m2m()

        messages.success(self.request, "Post créé avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "button_save_label": CONSTANT_SAVE,
                "button_cancel_label": CONSTANT_CANCEL,
                **self._context_defaults,
            }
        )
        return context


# ✏️ Modification d'un post
class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "posts/post_edit.html"
    success_url = reverse_lazy("posts:home")

    def form_valid(self, form):
        post = form.save(commit=False)
        if "image" in self.request.FILES:
            post.image = self.request.FILES["image"]
        post.save()
        messages.success(self.request, "Post mis à jour avec succès !")
        return super().form_valid(form)


# 📄 Détail d'un post avec commentaires
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_page.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """
        Retrieves the post and makes sure it exists, otherwise returns a 404 error.
        """
        post = super().get_object(queryset)
        if not post or post.id is None:
            raise Http404("Post introuvable")
        return post

    def get_context_data(self, **kwargs):
        """
        Adds comments and forms to the page context.
        """
        context = super().get_context_data(**kwargs)
        post = self.object  # Récupération de l'objet de la vue

        context["commentform"] = CommentCreateForm()
        context["replyform"] = ReplyCreateForm()
        context["comments"] = post.comments.all()

        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Handles HTML response and HTMX rendering.
        """
        request = self.request
        post = self.get_object()

        if request.htmx:
            # Gestion du tri des commentaires si demandé
            if "top" in request.GET:
                comments = (
                    post.comments.annotate(num_likes=Count("likes"))
                    .filter(num_likes__gt=0)
                    .order_by("-num_likes")
                )
            else:
                comments = post.comments.all()

            # Mise à jour du contexte pour HTMX
            context.update({"comments": comments})
            return render(
                request,
                "snippets/loop_postpage_comments.html",
                context=context,
                **response_kwargs,
            )

        return super().render_to_response(context, **response_kwargs)


# 🗑️ Suppression d'un post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("posts:home")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post supprimé avec succès !")
        return super().delete(request, *args, **kwargs)


# 📝 Création d'un commentaire
class CommentCreateView(LoginRequiredMixin, FormView):
    form_class = CommentCreateForm
    template_name = "snippets/add_comment.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["id"])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.parent_post = post
        comment.save()
        messages.success(self.request, "Commentaire ajouté avec succès !")
        return redirect("posts:post-page", id=post.id)


# 🗨️ Création d'une réponse
class ReplyCreateView(LoginRequiredMixin, FormView):
    form_class = ReplyCreateForm
    template_name = "snippets/add_reply.html"

    def form_valid(self, form):
        comment = get_object_or_404(Comment, id=self.kwargs["id"])
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.parent_comment = comment
        reply.save()
        messages.success(self.request, "Réponse ajoutée avec succès !")
        return redirect("posts:post-page", id=comment.parent_post.id)


# ❌ Suppression d'un commentaire
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "posts/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "posts:post-page", kwargs={"id": self.object.parent_post.id}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Commentaire supprimé !")
        return super().delete(request, *args, **kwargs)


# ❌ Suppression d'une réponse
class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = "posts/reply_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "posts:post-page",
            kwargs={"id": self.object.parent_comment.parent_post.id},
        )

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Réponse supprimée !")
        return super().delete(request, *args, **kwargs)


# ❤️ Gestion des likes
class LikeToggleView(LoginRequiredMixin, View):
    model = None  # Doit être défini dans les sous-classes

    def post(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        user_exists = obj.likes.filter(id=request.user.id).exists()

        if obj.author != request.user:
            if user_exists:
                obj.likes.remove(request.user)
            else:
                obj.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER", "posts:home"))


class LikePostView(LikeToggleView):
    model = Post


class LikeCommentView(LikeToggleView):
    model = Comment


class LikeReplyView(LikeToggleView):
    model = Reply
