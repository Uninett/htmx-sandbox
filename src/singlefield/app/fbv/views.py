import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from singlefield.app.models import Book
from singlefield.app.forms import BookForm, SingleFieldFormMixin
from singlefield.utils import show_breadcrumbs


LOG = logging.getLogger(__name__)


def get_forms(data=None, obj=None):
    data = {} if data is None else data
    forms = {}
    for Form in SingleFieldFormMixin.__subclasses__():
        kwargs = {}
        kwargs['instance'] = obj
        if Form.fieldname in data:
            kwargs['data'] = data
        form = Form(**kwargs)
        forms[form.fieldname] = form
    return forms


def get_misc_fields():
    """Get fields that are not stored on a model"""
    misc = []
    for fieldname, form in get_forms().items():
        if form.json_backed:
            misc.append(fieldname)
    return misc


def get_context_data(view_name, subtype, **kwargs):
    subtypename = subtype.subtype
    page_title = f': {subtypename}' if subtypename else ''
    misc = get_misc_fields()
    LOG.info("Getting context for %s", view_name)
    return dict(
        subtype=subtypename,
        page_title=page_title,
        misc=misc,
        view=subtype,
        **kwargs,
    )


# Way too easy to get lost without something like the below...


class Breadcrumb:
    _root_breadcrumb = ('/', 'Home')

    def get_breadcrumbs(self):
        self.breadcrumbs = getattr(self, 'breadcrumbs', [self._root_breadcrumb])
        return self.breadcrumbs

    def add_subtype_breadcrumb(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumb = (reverse(self.success_url), self.subtype)
        breadcrumbs = self.add_final_breadcrumb(breadcrumb)
        return breadcrumbs

    def add_final_breadcrumb(self, breadcrumb):
        self.breadcrumbs = self.get_breadcrumbs()
        if self.subtype in breadcrumb[0] and breadcrumb not in self.breadcrumbs:
            self.breadcrumbs.append(breadcrumb)
        return self.breadcrumbs

    def show_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        return show_breadcrumbs(breadcrumbs)


def get_breadcrumbs(subtype, link_name, link_text, kwargs=None):
    if kwargs is None:
        kwargs = {}
    subtype.get_breadcrumbs()
    subtype.add_subtype_breadcrumb()
    breadcrumb = (reverse(subtype.links[link_name], kwargs=kwargs), link_text)
    subtype.add_final_breadcrumb(breadcrumb)
    return subtype


class Classic(Breadcrumb):
    subtype: str = 'multifield'
    success_url = 'fbv-book-list'
    edit_url = 'fbv-book-edit'
    links = {
        'book_create': 'fbv-book-create',
        'book_delete': 'fbv-book-delete',
        'book_edit': edit_url,
        'book_new': 'fbv-book-new',
    }


class SingleField(Breadcrumb):
    subtype: str = 'singlefield'
    success_url = 'fbv-book-list2'
    links = {
        'book_create': 'fbv-book-create2',
        'book_delete': 'fbv-book-delete2',
        'book_edit': 'fbv-book-edit2',
        'book_get_field': 'fbv-book-edit-field2',
        'book_new': 'fbv-book-new2',
    }


class HTMxGetSingleField(Breadcrumb):
    subtype: str = 'singlefield-htmx-get'
    success_url = 'fbv-book-list3'
    links = {
        'book_create': 'fbv-book-create3',
        'book_delete': 'fbv-book-delete3',
        'book_edit': 'fbv-book-edit3',
        'book_get_field': 'fbv-book-edit-field3',
        'book_new': 'fbv-book-new3',
    }


class HTMxBoostSingleField(Breadcrumb):
    subtype: str = 'singlefield-htmx-boost'
    success_url = 'fbv-book-list4'
    links = {
        'book_create': 'fbv-book-create4',
        'book_delete': 'fbv-book-delete4',
        'book_edit': 'fbv-book-edit4',
        'book_get_field': 'fbv-book-edit-field4',
        'book_new': 'fbv-book-new4',
    }


# list views, detail views skipped


def _common_list_view(name, Subtype, template_name, request):
    subtype = Subtype()
    books = Book.objects.order_by('title')

    subtype.get_breadcrumbs()
    subtype.add_subtype_breadcrumb()

    kwargs = {
        'object_list': books,
        'books': books,
    }

    context = get_context_data(name, subtype, **kwargs)
    return render(request, template_name, context=context)


@require_GET
def list_view(request):
    return _common_list_view('list_view', Classic, 'singlefield_app/book_list.html', request)


@require_GET
def list_view2(request):
    return _common_list_view('list_view2', SingleField, 'singlefield_app/book_list2.html', request)


@require_GET
def list_view3(request):
    return _common_list_view('list_view3', HTMxGetSingleField, 'singlefield_app/book_list3.html', request)


@require_GET
def list_view4(request):
    return _common_list_view('list_view4', HTMxBoostSingleField, 'singlefield_app/book_list4.html', request)


# create views


def _get_create_breadcrumbs(subtype):
    return get_breadcrumbs(subtype, 'book_new', 'Add new')


@require_http_methods(['GET', 'POST'])
def create_view(request):
    subtype = Classic()
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(subtype.success_url)

    subtype = _get_create_breadcrumbs(subtype)

    kwargs = {
        'form': form,
    }
    context = get_context_data('create_view', subtype, **kwargs)
    return render(request, 'singlefield_fbv/book_form.html', context=context)


def _common_create_view(view_name, Subtype, request):
    subtype = Subtype()
    forms = get_forms()  # One form per field

    if request.method == 'POST':
        form = BookForm(request.POST)  # Save all fields at once!
        if form.is_valid():
            valid = True
            obj = form.save()
            forms = get_forms(request.POST, obj)
            for form in forms.values():
                if form.json_backed:
                    if form.is_valid():
                        form.save()
                    else:
                        valid = False
            if valid:
                return redirect(subtype.success_url)

    subtype = _get_create_breadcrumbs(subtype)

    kwargs = {
        'forms': forms,
    }
    context = get_context_data(view_name, subtype, **kwargs)
    template_name = 'singlefield_app/book_form2.html'
    return render(request, template_name, context=context)


@require_http_methods(['GET', 'POST'])
def create_view2(request):
    return _common_create_view('create_view2', SingleField, request)


@require_http_methods(['GET', 'POST'])
def create_view3(request):
    return _common_create_view('create_view3', HTMxGetSingleField, request)


@require_http_methods(['GET', 'POST'])
def create_view4(request):
    return _common_create_view('create_view4', HTMxBoostSingleField, request)


# delete views


def _common_delete_view(view_name: str, Subtype, request, pk: int):
    subtype = Subtype()
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect(subtype.success_url)

    subtype = get_breadcrumbs(subtype, 'book_delete', 'Delete', {'pk': pk})

    kwargs = {
        'object': book,
        'book': book,
    }
    context = get_context_data(view_name, subtype, **kwargs)
    return render(request, 'singlefield_app/book_confirm_delete.html', context=context)


@require_http_methods(['GET', 'POST'])
def delete_view(request, pk: int):
    return _common_delete_view('delete_view', Classic, request, pk)


@require_http_methods(['GET', 'POST'])
def delete_view2(request, pk: int):
    return _common_delete_view('delete_view2', SingleField, request, pk)


@require_http_methods(['GET', 'POST'])
def delete_view3(request, pk: int):
    return _common_delete_view('delete_view3', HTMxGetSingleField, request, pk)


@require_http_methods(['GET', 'POST'])
def delete_view4(request, pk: int):
    return _common_delete_view('delete_view4', HTMxBoostSingleField, request, pk)


# update view (multifield only)


@require_http_methods(['GET', 'POST'])
def update_view(request, pk: int):
    subtype = Classic()
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect(subtype.success_url)

    subtype = get_breadcrumbs(subtype, 'book_edit', 'Update', {'pk': pk})

    kwargs = {'form': form}
    context = get_context_data('update_view', subtype, **kwargs)
    return render(request, 'singlefield_fbv/book_form.html', context=context)


# update field views


@require_http_methods(['GET', 'POST'])
def update_view2(request, pk: int, fieldname: str):
    subtype = SingleField()
    book = get_object_or_404(Book, pk=pk)
    forms = get_forms(obj=book)

    if request.method == 'POST':
        forms = get_forms(data=request.POST, obj=book)
        form = forms[fieldname]
        if form.is_bound and form.is_valid():
            form.save()
            return redirect(subtype.success_url)

    subtype = get_breadcrumbs(
        subtype,
        'book_edit',
        'Update',
        {'pk': pk, 'fieldname': fieldname},
    )

    kwargs = {'forms': forms}
    context = get_context_data('update_view2', subtype, **kwargs)
    return render(request, 'singlefield_app/book_form2.html', context=context)


@require_http_methods(['GET', 'POST'])
def update_view3(request, pk: int, fieldname: str):
    subtype = HTMxGetSingleField()
    book = get_object_or_404(Book, pk=pk)
    forms = get_forms(obj=book)

    if request.method == 'POST':
        forms = get_forms(data=request.POST, obj=book)
        form = forms[fieldname]
        if form.is_bound and form.is_valid():
            form.save()

            fragment = f'book-{ book.id }'
            # fragment = '"field-{ book.id }-{ fieldname }'

            success_url = reverse(subtype.success_url, fragment)
            return redirect(success_url)

    kwargs = {'forms': forms}
    context = get_context_data('update_view3', subtype, **kwargs)
    return render(request, 'singlefield_fbv/book_form3.html', context=context)


@require_http_methods(['GET', 'POST'])
def update_view4(request, pk: int, fieldname: str):
    subtype = HTMxBoostSingleField()
    book = get_object_or_404(Book, pk=pk)
    forms = get_forms(obj=book)

    if request.method == 'POST':
        forms = get_forms(data=request.POST, obj=book)
        form = forms[fieldname]
        if form.is_bound and form.is_valid():
            form.save()

            success_url = reverse(subtype.success_url)
            return redirect(success_url)

    kwargs = {'forms': forms}
    context = get_context_data('update_view4', subtype, **kwargs)
    return render(request, 'singlefield_fbv/book_form4.html', context=context)


# the magic extra views for rendering the field template


def _get_common_field_view(view_name, subtype, template_name, request, pk: int, fieldname: str):
    book = get_object_or_404(Book, pk=pk)
    forms = get_forms(obj=book)

    kwargs = {
        'book': book,
        'object': book,
        'fieldname': fieldname,
        'form': forms[fieldname],
    }
    context = get_context_data('get_field_view2', subtype, **kwargs)
    return render(request, template_name, context=context)


@require_GET
def get_field_view2(request, pk: int, fieldname: str):
    subtype = SingleField()
    template_name = 'singlefield_app/book_field_form.html'

    # separate page so needs breadcrumbs
    subtype.get_breadcrumbs()
    subtype.add_subtype_breadcrumb()
    breadcrumb = (
        reverse('fbv-book-edit-field', kwargs={'pk': pk, 'fieldname': fieldname}),
        'Edit field',
    )
    subtype.add_final_breadcrumb(breadcrumb)

    return _get_common_field_view('get_field_view2', subtype, template_name, request, pk, fieldname)


@require_GET
def get_field_view3(request, pk: int, fieldname: str):
    subtype = HTMxGetSingleField()
    template_name = 'singlefield_app/_book_field_form.html'
    return _get_common_field_view('get_field_view3', subtype, template_name, request, pk, fieldname)


@require_GET
def get_field_view4(request, pk: int, fieldname: str):
    subtype = HTMxBoostSingleField()
    template_name = 'singlefield_app/_book_field_form.html'
    return _get_common_field_view('get_field_view4', subtype, template_name, request, pk, fieldname)
