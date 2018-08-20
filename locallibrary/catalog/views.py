from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    num_books_dawkins = Book.objects.filter(author__last_name__icontains='dawkins').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_dawkins': num_books_dawkins,
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
