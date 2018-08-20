from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    num_books_dawkins = Book.objects.filter(author__last_name__icontains='dawkins').count()

    num_visits = request.session.get("num_visits", 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_dawkins': num_books_dawkins,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 5

    # def get_context_data(self):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context["some_data"] = "This is just some data"
    #     return context

    def get_queryset(self):
        return Book.objects.filter(title__icontains='')


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowd_user.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)

