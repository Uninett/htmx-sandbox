from django.views.generic import TemplateView

from ..utils import BreadcrumbMixin


class HomePageView(BreadcrumbMixin, TemplateView):
    template_name = "homepage.html"

    breadcrumbs = [('/', 'Home')]
