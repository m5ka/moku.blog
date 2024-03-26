import re

import pytest

from moku.constants import Verbs
from moku.models.post import Post
from moku.models.user import User


@pytest.fixture
def post(user: User) -> Post:
    """Generate a test post."""
    return Post.objects.create(
        emoji="🌭", food="sausage surprise", verb=Verbs.COOKED, created_by=user
    )


@pytest.fixture(scope="session")
def re_uuid() -> re.Pattern:
    """Regex pattern to match a UUID."""
    return re.compile(r"[2-9A-HJ-NP-Za-km-z]{22}$")


@pytest.fixture
def user() -> User:
    """Generate a test user."""
    return User.objects.create_user(
        username="jean",
        email="jean.slater@example.com",
        password="sausage_surprise123!",
    )
