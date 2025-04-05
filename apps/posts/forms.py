from django import forms
from django.forms import ModelForm
from .models import Post, Comment, Reply


class PostCreateForm(ModelForm):
    """Formulaire de création de Post avec upload d'image"""

    class Meta:
        model = Post
        fields = ["title", "image", "body", "tags"]
        labels = {
            "title": "Titre",
            "body": "Caption",
            "tags": "Category",
            "image": "Image",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Titre du post",
                    "class": "font1 text-1xl mb-4 w-full",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ajoutez une légende ...",
                    "class": "font1 text-1xl mb-4 w-full",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "mb-4"}),
            "image": forms.ClearableFileInput(attrs={"class": "hidden"}),
        }

    image = forms.ImageField(required=False)


class PostEditForm(ModelForm):
    """Formulaire d'édition d'un Post avec modification d'image"""

    class Meta:
        model = Post
        fields = ["body", "tags", "image"]
        labels = {"body": "", "tags": "Category"}
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 3, "class": "font1 text-4xl"}
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "mb-4"}),
    )


class CommentCreateForm(ModelForm):
    """Formulaire de création de Commentaire"""

    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Add comment ...",
                    "class": "w-full border p-2",
                }
            )
        }


class ReplyCreateForm(ModelForm):
    """Formulaire de création de Réponse à un Commentaire"""

    class Meta:
        model = Reply
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Add reply ...",
                    "class": "w-full border p-2 text-sm",
                }
            )
        }
