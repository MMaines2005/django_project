from django.shortcuts import render, redirect
from .models import User, Book, UserManager
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"html/index.html")

# Registration with validations
def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/landing')

# landing page with all the information about likes and books for user
def landing(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
           "books" : Book.objects.all(),
           "user" : User.objects.get(id=request.session['user_id']),
        }
    return render(request, "html/landing.html", context)

# Make a book

def book_create(request):
    
    errors = Book.objects.book_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/landing')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            uploaded_by = user
        )
        # bonus: the book creator automatically favorites the book
        user.liked_books.add(book)

        return redirect(f'/landing/{book.id}')

def oneview(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "html/one_book.html", context)

#login with validations
def login(request):
    if request.method == 'GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['greeting'] = user.first_name
    return redirect('/landing')

def update(request, book_id):
    book = Book.objects.get(id=book_id)
    book.description = request.POST['description']
    book.save()

    return redirect(f"/landing/{book_id}")

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return redirect('/landing')

def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)

    return redirect(f'/landing/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)

    return redirect(f'/landing/{book_id}')
#logout 
def logout(request):
    request.session.flush()
    return redirect('/')