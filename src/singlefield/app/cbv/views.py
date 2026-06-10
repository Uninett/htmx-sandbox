import logging

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.forms import ModelForm

from singlefield.app.models import Book
from singlefield.app.forms import BookForm, SingleFieldFormMixin
from singlefield.utils import BreadcrumbMixin


LOG = logging.getLogger(__name__)


def get_forms(data=None, obj=None):
    data = {} if data is None else data
    forms = {}
    for Form in SingleFieldFormMixin.__subclasses__():
        kwargs = {}
        #if isinstance(Form, ModelForm):
        kwargs['instance'] = obj
        if Form.fieldname in data:
            kwargs['data'] = data
        form = Form(**kwargs)
        forms[form.fieldname] = form
    return forms


class ConvenienceMixin(BreadcrumbMixin):
    def get_context_data(self, **kwargs):
        subtype = self.subtype if self.subtype else ''
        page_title = f': {subtype}' if subtype else ''
        misc = self.get_misc_fields()
        LOG.info("Getting context for %s", self.__class__.__name__)
        return super().get_context_data(
            subtype=subtype,
            page_title=page_title,
            misc=misc,
            **kwargs,
        )

    def get_misc_fields(self):
        """Get fields that are not stored on a model"""
        misc = []
        for fieldname, form in get_forms().items():
            if form.json_backed:
                misc.append(fieldname)
        return misc

    def get_success_url(self):
        if hasattr(self, 'success_url'):
            return reverse(self.success_url)
        return ''

    # Way too easy to get lost without something like the below...

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse(self.success_url), self.subtype)
        return self.add_final_breadcrumb(breadcrumb)

    def add_final_breadcrumb(self, breadcrumb):
        if self.subtype in breadcrumb[0] and not breadcrumb in self.breadcrumbs:
            self.breadcrumbs.append(breadcrumb)
        return self.breadcrumbs


class ClassicMixin:
    subtype: str = 'multifield'
    success_url = 'book-list'
    edit_url = 'book-edit'
    links = {
        'book_create': 'book-create',
        "book_delete": "book-delete",
        "book_edit": edit_url,
        "book_new": "book-new",
    }


class SingleFieldMixin:
    subtype: str = 'singlefield'
    success_url = 'book-list2'
    links = {
        'book_create': 'book-create2',
        "book_delete": "book-delete2",
        "book_edit": 'book-edit2',
        'book_get_field': 'book-edit-field2',
        "book_new": "book-new2",
    }


class HTMxGetSingleFieldMixin:
    subtype: str = 'singlefield-htmx-get'
    success_url = 'book-list3'
    links = {
        'book_create': 'book-create3',
        "book_delete": "book-delete3",
        "book_edit": 'book-edit3',
        'book_get_field': 'book-edit-field3',
        "book_new": "book-new3",
    }


class HTMxBoostSingleFieldMixin:
    subtype: str = 'singlefield-htmx-boost'
    success_url = 'book-list4'
    links = {
        'book_create': 'book-create4',
        "book_delete": "book-delete4",
        "book_edit": 'book-edit4',
        'book_get_field': 'book-edit-field4',
        "book_new": "book-new4",
    }


# list views, detail views skipped


class ListBookView(ClassicMixin, ConvenienceMixin, ListView):
    model = Book
    ordering = ["title"]


class SingleFieldListBookView(SingleFieldMixin, ListBookView):
    template_name = 'singlefield_app/book_list2.html'


class HTMxGetSingleFieldListBookView(HTMxGetSingleFieldMixin, SingleFieldListBookView):
    template_name = 'singlefield_app/book_list3.html'


class HTMxBoostSingleFieldListBookView(HTMxBoostSingleFieldMixin, SingleFieldListBookView):
    template_name = 'singlefield_app/book_list4.html'

# create views


class CreateBookView(ClassicMixin, ConvenienceMixin, CreateView):
    model = Book
    form_class = BookForm

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


class SingleFieldCreateBookView(SingleFieldMixin, ConvenienceMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'singlefield_app/book_form2.html'

    def get_forms(self):
        return get_forms(data=self.request.POST)

    def get_context_data(self, **kwargs):
        forms = self.get_forms()
        return super().get_context_data(forms=forms, **kwargs)

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new2'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


class HTMxGetSingleFieldCreateBookView(HTMxGetSingleFieldMixin, SingleFieldCreateBookView):

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new3'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


class HTMxBoostSingleFieldCreateBookView(HTMxBoostSingleFieldMixin, SingleFieldCreateBookView):

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (reverse('book-new4'), 'Add new')
        return self.add_final_breadcrumb(breadcrumb)


# delete views


class DeleteBookView(ClassicMixin, ConvenienceMixin, DeleteView):
    model = Book

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


class SingleFieldDeleteBookView(SingleFieldMixin, DeleteBookView):
    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete2', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


class HTMxGetSingleFieldDeleteBookView(HTMxGetSingleFieldMixin, SingleFieldDeleteBookView):
    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete3', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


class HTMxBoostSingleFieldDeleteBookView(HTMxBoostSingleFieldMixin, SingleFieldDeleteBookView):
    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse('book-delete4', kwargs={'pk': self.kwargs['pk']}),
            'Delete',
        )
        return self.add_final_breadcrumb(breadcrumb)


# update view (multifield only)


class UpdateBookView(ClassicMixin, ConvenienceMixin, UpdateView):
    model = Book
    form_class = BookForm

    def get_breadcrumbs(self):
        super().get_breadcrumbs()
        breadcrumb = (
            reverse(self.edit_url, kwargs={'pk': self.kwargs['pk']}),
            'Edit',
        )
        return self.add_final_breadcrumb(breadcrumb)


# Update field views


class SingleFieldUpdateBookView(SingleFieldMixin, ConvenienceMixin, UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'singlefield_app/book_edit.html'

    def get_forms(self):
        instance = self.get_object()
        return get_forms(data=self.request.POST, obj=instance)

    def get_context_data(self, **kwargs):
        forms = self.get_forms()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        valid = False
        for form in forms.values():
            if form.is_bound and form.is_valid():
                valid = True
        if valid:
            return self.form_valid(forms)
        return self.form_invalid(forms)

    def form_valid(self, forms):
        for fieldname, form in forms.items():
            if not (form.is_bound and form.is_valid()):
                continue
            form.save()
        return HttpResponseRedirect(self.get_success_url())


class HTMxGetSingleFieldUpdateBookView(HTMxGetSingleFieldMixin, SingleFieldUpdateBookView):
    template_name = 'singlefield_app/book_edit.html'

    def get_fragment(self):
        "Redirect to start of book"
        object = self.get_object()
        return f"book-{ object.id }"

#     def get_fragment(self):
#         "Redirect to field"
#         object = self.get_object()
#         fieldname = self.kwargs['fieldname']
#         return f"field-{ object.id }-{ fieldname }"

    def get_success_url(self):
        url = reverse(self.success_url, fragment=self.get_fragment())
        LOG.info("Going to %s", url)
        return url


class HTMxBoostSingleFieldUpdateBookView(HTMxBoostSingleFieldMixin, SingleFieldUpdateBookView):
    template_name = 'singlefield_app/book_edit.html'


# the magic extra views for rendering the field template


class SingleFieldBookFieldView(SingleFieldMixin, ConvenienceMixin, DetailView):
    model = Book
    template_name = 'singlefield_app/book_field_form.html'

    def get_breadcrumbs(self):
        # Only needed and used by "singlefield"
        # Multifield doesn't use this view
        # The two htmx views do not use this template
        super().get_breadcrumbs()
        breadcrumb = (
            reverse(
                'book-edit-field2',
                kwargs={
                    'pk': self.kwargs['pk'],
                    'fieldname' : self.kwargs['fieldname']},
            ),
            'Edit field',
        )
        return self.add_final_breadcrumb(breadcrumb)

    def get_forms(self):
        instance = self.get_object()
        return get_forms(data=request.POST, obj=instance)

    def get_context_data(self, **kwargs):
        forms = get_forms(obj=self.object)
        fieldname = self.kwargs["fieldname"]
        form = forms[fieldname]
        context = super().get_context_data(fieldname=fieldname, form=form, **kwargs)
        LOG.info("Getting context for %s", self.__class__.__name__)
        return context


class HTMxGetSingleFieldBookFieldView(HTMxGetSingleFieldMixin, SingleFieldBookFieldView):
    template_name = 'singlefield_app/_book_field_form.html'


class HTMxBoostSingleFieldBookFieldView(HTMxBoostSingleFieldMixin, SingleFieldBookFieldView):
    template_name = 'singlefield_app/_book_field_form.html'
