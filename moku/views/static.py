from moku.views.base import View


class ChangelogView(View):
    template_name = "moku/changelog.jinja"


class PrivacyView(View):
    template_name = "moku/privacy.jinja"


class TermsView(View):
    template_name = "moku/terms.jinja"
