from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, FileResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.core.paginator import InvalidPage
from django.views.decorators.cache import cache_page
from django.views.generic.edit import FormView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
    TemplateView,
)
import logging

from apps.constant import CONSTANT_SAVE, CONSTANT_CANCEL, CONSTANT_CONFIRM
from .models import Post, Tag, Comment, Reply, Image
from .forms import (
    ReplyCreateForm,
    AddPostForm,
    PostEditForm,
    CommentCreateForm,
)

logger = logging.getLogger(__name__)


# 🏠 Page d'accueil avec pagination
class PostHomeView(ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_tag_slug(self):
        return self.kwargs.get("tag")

    def get_queryset(self):
        tag_slug = self.get_tag_slug()
        queryset = (
            Post.objects.select_related("author")
            .prefetch_related("tags")
            .annotate(like_count=Count("likes"))
        )
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.get_tag_slug()
        context.update(
            {
                "tag": (
                    get_object_or_404(Tag, slug=tag_slug) if tag_slug else None
                ),
                "page": self.request.GET.get("page", 1),
            }
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(
                self.request, "posts/snippets/loop_home_posts.html", context
            )
        return super().render_to_response(context, **response_kwargs)

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, allow_empty_first_page=True
        )
        page_number = self.request.GET.get("page") or 1
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage:
            logger.warning(
                f"[Pagination out-of-bounds] page={page_number} | max={paginator.num_pages}"
            )
            page = paginator.page(1)
            return (paginator, page, page.object_list, page.has_other_pages())


# @method_decorator(cache_page(60 * 15), name="dispatch")  # 15 minutes
class LastPostFragmentView(TemplateView):
    template_name = "posts/components/last_post_fragment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = (
            Post.objects.select_related("author")
            .prefetch_related("tags")
            .annotate(like_count=Count("likes"))
            .only("id", "title", "image", "created", "author__username")[:3]
        )
        return context


# 📌 Création d'un post
class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = AddPostForm
    template_name = "posts/add_post.html"
    success_url = reverse_lazy("posts:post_home")
    _context_defaults = {
        "add_post_title": "Nouveau post ...",
        "add_post_description": "",
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user

        # ✅ Vérification de l'image
        uploaded_image = form.cleaned_data.get("image")
        if not uploaded_image:
            messages.error(self.request, "Vous devez ajouter une image !")
            return self.form_invalid(form)

        post.image = uploaded_image
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
    success_url = reverse_lazy("posts:post_home")
    _context_defaults = {
        "post_edit_title": "Edit post ...",
        "post_edit_description": "",
    }

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            messages.error(
                request, "Vous n'avez pas la permission de modifier ce post."
            )
            return redirect("posts:post_detail", pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        if "image" in self.request.FILES:
            post.image = self.request.FILES["image"]
        post.save()
        messages.success(self.request, "Post mis à jour avec succès !")
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


# 📄 Détail d'un post avec commentaires
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    _context_defaults = {
        "post_detail_title": "",
        "post_detail_description": "",
    }

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
        post = self.object
        context.update(
            {
                "commentform": CommentCreateForm(),
                "replyform": ReplyCreateForm(),
                "comments": post.comments.all(),
                **self._context_defaults,
            }
        )

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
                "posts/snippets/loop_postpage_comments.html",
                context=context,
                **response_kwargs,
            )

        return super().render_to_response(context, **response_kwargs)


# 🗑️ Suppression d'un post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("posts:post_home")
    _context_defaults = {
        "post_delete_title": "Suppression irréversible ...",
        "post_delete_description": "",
    }

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post supprimé avec succès !")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "button_confirm_label": CONSTANT_CONFIRM,
                "button_cancel_label": CONSTANT_CANCEL,
                "sentence": "Voulez-vous vraiment supprimer ce post ?",
                **self._context_defaults,
            }
        )
        return context


# 📝 Création d'un commentaire
class CommentCreateView(LoginRequiredMixin, FormView):
    form_class = CommentCreateForm
    template_name = "posts/snippets/comment_create.html"

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
    template_name = "posts/snippets/reply_create.html"

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


class ImageWallView(ListView):
    model = Image
    template_name = "posts/image_wall.html"
    context_object_name = "images"
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.order_by("-uploaded_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_obj"] = context["page_obj"]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(
                self.request,
                "posts/partials/_image_list.html",
                context,
                **response_kwargs,
            )
        return super().render_to_response(context, **response_kwargs)

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, allow_empty_first_page=True
        )
        page_number = self.request.GET.get("page") or 1
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            logger.warning(
                f"[Pagination out-of-bounds] page={page_number} | max={paginator.num_pages}"
            )
            page = paginator.page(1)

        return paginator, page, page.object_list, page.has_other_pages()


class ImageDownloadView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "You must be logged in to download images."
            )

        image = get_object_or_404(Image, pk=pk)
        return FileResponse(
            image.image.open(),
            as_attachment=True,
            filename=image.image.name.split("/")[-1],
        )


class LastImageFragmentView(ListView):
    model = Image
    template_name = "posts/components/last_image_fragment.html"
    context_object_name = "last_images"
    paginate_by = None

    def get_queryset(self):
        return Image.objects.order_by("-uploaded_at")[:3]
