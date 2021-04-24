from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login as auth_login
from core.models import Card, User, Deck
from core.forms import createUser
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def home(request):
    context = {
        'card': Card.objects.all()
    }

    return render(request, 'home.html' , context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            user = request.user
            return redirect('/' + user.username + '/')
    else:
        form = AuthenticationForm()
    return render(request,'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = createUser(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/guide/')
    else:
        form = createUser()
    return render(request, 'register.html', {'form':form})

def profile(request, username):
    other_user = User.objects.get(username=username)
    if request.method == 'POST':
        user = User.objects.get(email=request.user) 
        if 'logout' in request.POST: 
            if user == other_user:
                logout(request)
                return redirect("/")

    context = {
        'other_user':other_user,
    }

    if User.objects.all().filter(email=request.user).exists():
        user = User.objects.get(email=request.user)
        context['user'] = user

    if Card.objects.all().filter(favorites=other_user).exists():
        card = Card.objects.all().filter(favorites=other_user)
        context['card'] = card

    if Deck.objects.all().filter(favorites=other_user).exists():
        deck = Card.objects.all().filter(favorites=other_user)
        context['favorited_deck'] = deck
    
    if Deck.objects.all().filter(user=other_user).exists():
        deck = Card.objects.all().filter(user=other_user)
        context['user_deck'] = deck

    return render(request, 'profile.html', context)

def card(request, title):
    card = Card.objects.get(title=title)
    recomend_list = []

    for i in Card.objects.all().exclude(id=card.id):
        matrix = CountVectorizer().fit_transform([card.content,i.content])
        match = cosine_similarity(matrix)[1][0]

        recomend_obj = dict(
            recomend = i,
            match = match,
        )
        
        recomend_list.append(recomend_obj)

    if request.method == 'POST':
        if 'favorite' in request.POST:
            if Card.objects.filter(favorites=request.user).exists():
                card.favorites.remove(request.user)
            else:
                user = User.objects.get(email=request.user) 
                card.favorites.add(request.user)

        elif 'deck' in request.POST:
            if Deck.objects.get(id=request.POST['deck'], cards=card).exists():
                deck = Deck.objects.get(id=request.POST['deck'])
                deck.cards.remove(card)
            else:
                deck = Deck.objects.get(id=request.POST['deck']) 
                deck.cards.add(card)
                
    context = {
        'card':card,
        'recomend_list':sorted(recomend_list,key=lambda k:k['match'], reverse=True)[:5],
    }

    if User.objects.all().filter(username=request.user).exists():
        if Deck.objects.all().filter(user=request.user).exists():
            deck = Deck.objects.all().filter(user=request.user)
            context['deck'] = deck

    return render(request, 'card.html', context)

def deck(request):
    return render(request, 'deck.html')

def error404(request, exception=None):
    return render(request, 'error404.html')

def error500(request, exception=None): 
    return render(request, 'error500.html')