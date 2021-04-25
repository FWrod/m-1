from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth import logout, authenticate, login as auth_login
from core.models import Card, User, Deck
from core.forms import createUser
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.filters import CardFilter, DeckFilter

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

def card_ranking(request):
    card_filter = CardFilter(request.GET, queryset=Card.objects.all().order_by('-favorites'))

    paginator = Paginator(card_filter.qs, 20)
    page_number = request.GET.get('page')
    card_obj = paginator.get_page(page_number)

    context = {
        'card_obj': card_obj,
        'card_filter': card_filter,
    }

    return render(request, 'card_ranking.html', context)

def deck_ranking(request):
    deck_filter = DeckFilter(request.GET, queryset=Deck.objects.all().order_by('-favorites'))

    paginator = Paginator(deck_filter.qs, 20)
    page_number = request.GET.get('page')
    deck_obj = paginator.get_page(page_number)

    context = {
        'deck_obj': deck_obj,
        'deck_filter': deck_filter,
    }

    return render(request, 'deck_ranking.html', context)

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
        favorited_deck = Deck.objects.all().filter(favorites=other_user)
        context['favorited_deck'] = favorited_deck
    
    if Deck.objects.all().filter(user=other_user).exists():
        user_deck = Deck.objects.all().filter(user=other_user)
        context['user_deck'] = user_deck

    return render(request, 'profile.html', context)

def card(request, title):
    card = Card.objects.get(title=title)
    deck = Deck.objects.all().filter(cards=card).order_by('-favorites')[:5]
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
        'deck':deck,
        'recomend_list':sorted(recomend_list,key=lambda k:k['match'], reverse=True)[:5],
    }

    '''
    if Deck.objects.all().filter(user=request.user).exists():
        deck = Deck.objects.all().filter(user=request.user)
        context['deck'] = deck
    '''    

    return render(request, 'card.html', context)

def deck(request, title):
    deck = Deck.objects.get(title=title)
    other_user = User.objects.get(email=deck.user)

    if request.method == 'POST':
        if 'favorite' in request.POST:
            if Deck.objects.filter(favorites=request.user).exists():
                deck.favorites.remove(request.user)
            else:
                deck.favorites.add(request.user)

    context = {
        'deck':deck,
        'other_user':other_user,
    }

    return render(request, 'deck.html', context)

def error404(request, exception=None):
    return render(request, 'error404.html')

def error500(request, exception=None): 
    return render(request, 'error500.html')