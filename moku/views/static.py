from django.utils.translation import gettext_lazy

from moku.views.base import View


class ChangelogView(View):
    """Displays the static changelog page."""

    template_name = "moku/changelog.jinja"
    page_title = gettext_lazy("changelog")


class PrivacyView(View):
    """Displays the static privacy policy page."""

    template_name = "moku/privacy.jinja"
    page_title = gettext_lazy("privacy policy")


class TermsView(View):
    """Displays the static terms of use page."""

    template_name = "moku/terms.jinja"
    page_title = gettext_lazy("terms of use")
