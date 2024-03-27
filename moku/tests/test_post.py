import re

import pytest

from moku.models.post import Post


@pytest.mark.django_db
def test_post(post: Post, re_uuid: re.Pattern):
    """Test that a post is created successfully with all required data."""
    assert isinstance(post.pk, int)
    assert post.pk > 0
    assert post.pk == post.id
    assert re_uuid.match(post.uuid) is not None
    assert post.html == '<a href="/user/jean">@jean</a> cooked sausage surprise'
    assert post.plain_text == "@jean cooked sausage surprise"
