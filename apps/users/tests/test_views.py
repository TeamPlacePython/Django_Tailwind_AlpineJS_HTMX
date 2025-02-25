import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from pytest_django.asserts import assertTemplateUsed
from django.contrib.messages import get_messages


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def authenticated_client(client, user):
    client.login(username="testuser", password="testpass123")
    return client


@pytest.mark.django_db
class TestProfileView:
    def test_profile_view_without_username(self, authenticated_client):
        url = reverse("users:profile")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "users/profile.html")

    def test_profile_view_with_username(self, client, user):
        url = reverse("users:profile", kwargs={"username": user.username})
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "users/profile.html")

    def test_profile_view_with_invalid_username(self, client):
        url = reverse("users:profile", kwargs={"username": "nonexistent"})
        response = client.get(url)
        assert response.status_code == 404

    def test_profile_view_unauthenticated(self, client):
        url = reverse("users:profile")
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestProfileEditView:
    def test_profile_edit_view_get(self, authenticated_client):
        url = reverse("users:profile-edit")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "users/profile_edit.html")

    def test_profile_edit_view_post_valid(self, authenticated_client):
        url = reverse("users:profile-edit")
        data = {
            "bio": "New bio text",
            # Ajoutez d'autres champs de formulaire nécessaires ici
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse("users:profile")

    def test_profile_edit_view_unauthenticated(self, client):
        url = reverse("users:profile-edit")
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url


@pytest.mark.django_db
class TestProfileEmailChangeView:
    def test_email_change_view_get_htmx(self, authenticated_client):
        url = reverse("users:profile-emailchange")
        response = authenticated_client.get(url, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assertTemplateUsed(response, "partials/email_form.html")

    def test_email_change_view_post_valid(self, authenticated_client):
        url = reverse("users:profile-emailchange")
        data = {"email": "newemail@example.com"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert len(mail.outbox) == 1  # Vérifie qu'un email a été envoyé

    def test_email_change_view_post_existing_email(
        self, authenticated_client, db
    ):
        User.objects.create_user(
            username="other", email="existing@example.com", password="pass123"
        )
        url = reverse("users:profile-emailchange")
        data = {"email": "existing@example.com"}
        response = authenticated_client.post(url, data)
        messages = list(get_messages(response.wsgi_request))
        assert "is already in use" in str(messages[0])


@pytest.mark.django_db
class TestProfileUsernameChangeView:
    def test_username_change_view_get_htmx(self, authenticated_client):
        url = reverse("users:profile-usernamechange")
        response = authenticated_client.get(url, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assertTemplateUsed(response, "partials/username_form.html")

    def test_username_change_view_post_valid(self, authenticated_client):
        url = reverse("users:profile-usernamechange")
        data = {"username": "newusername"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert "Username updated successfully" in str(messages[0])


@pytest.mark.django_db
class TestProfileDeleteView:
    def test_profile_delete_view_get(self, authenticated_client):
        url = reverse("users:profile-delete")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "users/profile_delete.html")

    def test_profile_delete_view_post(self, authenticated_client, user):
        url = reverse("users:profile-delete")
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert response.url == reverse("home:home-index")
        assert not User.objects.filter(id=user.id).exists()
        messages = list(get_messages(response.wsgi_request))
        assert "Account deleted" in str(messages[0])


@pytest.mark.django_db
class TestProfileEmailVerifyView:
    def test_email_verify_view(self, authenticated_client):
        url = reverse("users:profile-emailverify")
        response = authenticated_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("users:profile-settings")
        assert len(mail.outbox) == 1  # Vérifie qu'un email a été envoyé
