from django.views.generic import TemplateView

from singlefield.utils import BreadcrumbMixin


class HomePageView(BreadcrumbMixin, TemplateView):
    template_name = 'singlefield_app/homepage.html'

    breadcrumbs = [('/', 'Home')]
