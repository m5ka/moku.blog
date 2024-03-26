import pytest

from moku.models.user import User


@pytest.mark.django_db
def test_user(user: User):
    """Test that a user is created successfully with all required data."""
    assert isinstance(user.pk, int)
    assert user.pk > 0
    assert user.id == user.pk
    assert str(user) == "jean"
    assert user.get_absolute_url() == "/user/jean"
