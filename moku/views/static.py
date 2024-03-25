from django.views.generic import TemplateView


class ChangelogView(TemplateView):
    template_name = "moku/changelog.jinja"


class PrivacyView(TemplateView):
    template_name = "moku/privacy.jinja"


class TermsView(TemplateView):
    template_name = "moku/terms.jinja"
