import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress
from .forms import ProfileForm, EmailForm


# Fixtures
@pytest.fixture
def user(db):
    """Create a test user.

    Returns:
        User: A test user with username 'testuser' and email 'test@example.com'
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def authenticated_client(client, user):
    """Create an authenticated client.

    Args:
        client: Django test client
        user: Test user fixture

    Returns:
        Client: An authenticated Django test client
    """
    client.force_login(user)
    return client


# ProfileView tests
@pytest.mark.django_db
class TestProfileView:
    """Test suite for ProfileView.

    Tests both authenticated and unauthenticated access to profile views,
    as well as viewing other users' profiles.
    """

    def test_profile_view_with_username(self, client, user):
        """Test accessing a profile page using a username."""
        url = reverse("users:profile", kwargs={"username": user.username})
        response = client.get(url)
        assert response.status_code == 200
        assert "profile" in response.context

    def test_profile_view_without_username_unauthenticated(self, client):
        """Test accessing own profile while not logged in."""
        url = reverse("users:profile")
        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_profile_view_without_username_authenticated(
        self, authenticated_client, user
    ):
        """Test accessing own profile while logged in."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.context["profile"] == user.profile


# ProfileEditView tests
@pytest.mark.django_db
class TestProfileEditView:
    """Test suite for ProfileEditView.

    Tests profile editing functionality including form submission
    and authentication requirements.
    """

    def test_profile_edit_view_unauthenticated(self, client):
        """Test that unauthenticated users cannot access edit page."""
        url = reverse("users:profile-edit")
        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_profile_edit_view_get(self, authenticated_client):
        """Test displaying the profile edit form."""
        url = reverse("users:profile-edit")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_profile_edit_view_post_valid(self, authenticated_client):
        """Test submitting valid profile edit data."""
        url = reverse("users:profile-edit")
        data = {"bio": "New bio text", "location": "New location"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse("users:profile")


# ProfileEmailChangeView tests
@pytest.mark.django_db
class TestProfileEmailChangeView:
    """Test suite for ProfileEmailChangeView.

    Tests email change functionality including form submission
    and duplicate email validation.
    """

    def test_email_change_view_htmx(self, authenticated_client):
        """Test getting the email change form via HTMX."""
        url = reverse("users:profile-email-change")
        response = authenticated_client.get(url, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert "form" in response.context

    def test_email_change_view_post_valid(self, authenticated_client):
        """Test successful email change."""
        url = reverse("users:profile-email-change")
        data = {"email": "newemail@example.com"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert len(mail.outbox) == 1  # Check that an email has been sent

    def test_email_change_view_post_duplicate_email(
        self, authenticated_client, db
    ):
        """Test email change with an already existing email."""
        User.objects.create_user(
            "otheruser", "existing@example.com", "pass123"
        )
        url = reverse("users:profile-email-change")
        data = {"email": "existing@example.com"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert "already in use" in str(messages[0])


# ProfileDeleteView tests
@pytest.mark.django_db
class TestProfileDeleteView:
    """Test suite for ProfileDeleteView.

    Tests account deletion functionality including confirmation
    and actual deletion process.
    """

    def test_profile_delete_view_get(self, authenticated_client):
        """Test displaying the account deletion confirmation page."""
        url = reverse("users:profile-delete")
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_profile_delete_view_post(self, authenticated_client, user):
        """Test successful account deletion."""
        url = reverse("users:profile-delete")
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert response.url == reverse("home:home-index")
        assert not User.objects.filter(id=user.id).exists()
        messages = list(get_messages(response.wsgi_request))
        assert "Account deleted" in str(messages[0])


# UserSignals tests
@pytest.mark.django_db
class TestUserSignals:
    """Test suite for User model signals.

    Tests automatic actions triggered by User model events.
    """

    def test_profile_creation_on_user_create(self, db):
        """Test automatic profile creation when user is created."""
        user = User.objects.create_user(
            username="testsignals",
            email="testsignals@example.com",
            password="testpass123",
        )
        assert hasattr(user, "profile")
        assert user.profile is not None

    def test_username_lowercase_on_save(self, db):
        """Test username conversion to lowercase on save."""
        user = User.objects.create_user(
            username="TestUPPER",
            email="test@example.com",
            password="testpass123",
        )
        assert user.username == "testupper"

    def test_email_address_creation_on_user_create(self, db):
        """Test automatic email address creation for new users."""
        user = User.objects.create_user(
            username="testmail",
            email="testmail@example.com",
            password="testpass123",
        )
        email_address = EmailAddress.objects.get(user=user)
        assert email_address.email == user.email
        assert email_address.primary
        assert not email_address.verified

    def test_email_address_update_on_user_email_change(self, db):
        """Test email address update when user email changes."""
        user = User.objects.create_user(
            username="testmail",
            email="old@example.com",
            password="testpass123",
        )

        # Check that the initial email is properly configured
        initial_email = EmailAddress.objects.get(user=user)
        assert initial_email.email == "old@example.com"

        # Change the user's email
        user.email = "new@example.com"
        user.save()

        # Check that the email has been updated and marked as unverified
        updated_email = EmailAddress.objects.get(user=user)
        assert updated_email.email == "new@example.com"
        assert not updated_email.verified


# ProfileUsernameChangeView tests
@pytest.mark.django_db
class TestProfileUsernameChangeView:
    """Test suite for ProfileUsernameChangeView.

    Tests username change functionality including HTMX requests
    and duplicate username validation.
    """

    def test_username_change_view_htmx(self, authenticated_client):
        """Test getting the username change form via HTMX."""
        url = reverse("users:profile-username-change")
        response = authenticated_client.get(url, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert "form" in response.context

    def test_username_change_view_post_valid(self, authenticated_client):
        """Test successful username change."""
        url = reverse("users:profile-username-change")
        data = {"username": "newusername"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse("users:profile-settings")
        messages = list(get_messages(response.wsgi_request))
        assert "Username successfully updated" in str(messages[0])

    def test_username_change_view_post_duplicate(
        self, authenticated_client, db
    ):
        """Test username change with an already existing username."""
        User.objects.create_user("existinguser", "test@test.com", "pass123")
        url = reverse("users:profile-username-change")
        data = {"username": "existinguser"}
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert "already in use" in str(messages[0])


# ProfileSettingsView tests
@pytest.mark.django_db
class TestProfileSettingsView:
    """Test suite for ProfileSettingsView.

    Tests access to profile settings page for both authenticated
    and unauthenticated users.
    """

    def test_settings_view_unauthenticated(self, client):
        """Test that unauthenticated users cannot access settings."""
        url = reverse("users:profile-settings")
        response = client.get(url)
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_settings_view_authenticated(self, authenticated_client):
        """Test that authenticated users can access settings."""
        url = reverse("users:profile-settings")
        response = authenticated_client.get(url)
        assert response.status_code == 200


# ProfileEmailVerifyView tests
@pytest.mark.django_db
class TestProfileEmailVerifyView:
    """Test suite for ProfileEmailVerifyView.

    Tests email verification functionality including email sending.
    """

    def test_email_verify_view(self, authenticated_client):
        """Test requesting a new verification email."""
        url = reverse("users:profile-emailverify")
        response = authenticated_client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("users:profile-settings")
        assert len(mail.outbox) == 1


# Forms tests
@pytest.mark.django_db
class TestForms:
    """Test suite for all user-related forms.

    Tests form validation for Profile, Email, and Username forms.
    """

    def test_profile_form_valid(self):
        """Test ProfileForm with valid data."""
        form_data = {"displayname": "Test User", "info": "Test bio"}
        form = ProfileForm(data=form_data)
        assert form.is_valid()

    def test_profile_form_invalid_displayname(self):
        """Test ProfileForm with invalid display name."""
        form_data = {"displayname": "A", "info": "Test bio"}  # Trop court
        form = ProfileForm(data=form_data)
        assert not form.is_valid()
        assert "displayname" in form.errors

    def test_email_form_valid(self):
        """Test EmailForm with valid email."""
        form_data = {"email": "valid@email.com"}
        form = EmailForm(data=form_data)
        assert form.is_valid()

    def test_email_form_invalid(self):
        """Test EmailForm with invalid email."""
        form_data = {"email": "invalid-email"}
        form = EmailForm(data=form_data)
        assert not form.is_valid()


# Profile Model tests
@pytest.mark.django_db
class TestProfileModel:
    """Test suite for Profile model.

    Tests Profile model methods, properties, and validation.
    """

    def test_profile_str(self, user):
        """Test string representation of Profile."""
        assert str(user.profile) == user.username

    def test_profile_name_with_displayname(self, user):
        """Test name property when display name is set."""
        user.profile.displayname = "Display Name"
        user.profile.save()
        assert user.profile.name == "Display Name"

    def test_profile_name_without_displayname(self, user):
        """Test name property when display name is not set."""
        assert user.profile.name == user.username

    def test_profile_avatar_with_image(self, user):
        """Test avatar property with custom image."""
        # Note: Ce test nécessiterait un fichier image de test
        pass

    def test_profile_avatar_without_image(self, user):
        """Test avatar property with default image."""
        assert "avatar.svg" in user.profile.avatar

    def test_profile_clean_invalid_displayname(self, user):
        """Test validation of invalid display name."""
        user.profile.displayname = "A"
        with pytest.raises(ValidationError):
            user.profile.clean()


# Admin tests
@pytest.mark.django_db
class TestAdmin:
    """Test suite for Django admin interface.

    Tests admin interface functionality for Profile model.
    """

    def test_profile_admin_list_display(self, admin_client, user):
        """Test admin list view for profiles."""
        url = reverse("admin:users_profile_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_profile_admin_search(self, admin_client, user):
        """Test admin search functionality for profiles."""
        url = reverse("admin:users_profile_changelist") + f"?q={user.username}"
        response = admin_client.get(url)
        assert response.status_code == 200
