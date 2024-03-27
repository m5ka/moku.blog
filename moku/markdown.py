from django.apps import apps
from django.conf import settings
from mistune import HTMLRenderer, Markdown
from mistune.plugins.formatting import strikethrough, subscript, superscript
from mistune.plugins.url import url

USERNAME_PATTERN = (
    r"@[a-z0-9-_.]{"
    + str(settings.USERNAME_MIN_LENGTH)
    + r","
    + str(settings.USERNAME_MAX_LENGTH)
    + r"}"
)


def _parse_username_link(inline, m, state):
    User = apps.get_model("moku", "User")

    text = m.group(0)
    pos = m.end()
    if state.in_link:
        inline.process_text(text, state)
        return pos

    try:
        user = User.objects.get(username=text[1:])
    except User.DoesNotExist:
        inline.process_text(text, state)
        return pos

    state.append_token(
        {
            "type": "link",
            "children": [{"type": "text", "raw": f"@{user.username}"}],
            "attrs": {"url": user.get_absolute_url()},
        }
    )
    return pos


def _username(md):
    md.inline.register("username", USERNAME_PATTERN, _parse_username_link)


full_markdown = Markdown(
    renderer=HTMLRenderer(),
    plugins=[strikethrough, subscript, superscript, url, _username],
)

basic_markdown = Markdown(
    renderer=HTMLRenderer(), plugins=[strikethrough, subscript, superscript, url]
)
