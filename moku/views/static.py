from moku.views.base import View


class ChangelogView(View):
    """Displays the static changelog page."""

    template_name = "moku/changelog.jinja"


class PrivacyView(View):
    """Displays the static privacy policy page."""

    template_name = "moku/privacy.jinja"


class TermsView(View):
    """Displays the static terms of use page."""

    template_name = "moku/terms.jinja"
