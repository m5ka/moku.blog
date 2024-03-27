from django.shortcuts import render


def forbidden(request, exception):
    return render(request, "moku/error/403.jinja")


def not_found(request, exception):
    return render(request, "moku/error/404.jinja")


def server_error(request):
    return render(request, "moku/error/500.html")
