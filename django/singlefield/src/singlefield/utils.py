def show_breadcrumbs(breadcrumbs):
    outlist = []
    for link, title in breadcrumbs:
        outlist.append(f'<a href="{link}">{title}</a>')
    trail = ' → '.join(outlist)
    return f'<nav class="breadcrumbs">{trail}</nav>'


class BreadcrumbMixin:
    _root_breadcrumb = ('/', 'Home')

    def get_breadcrumbs(self):
        self.breadcrumbs = [self._root_breadcrumb]
        return self.breadcrumbs

    def show_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        return show_breadcrumbs(breadcrumbs)
