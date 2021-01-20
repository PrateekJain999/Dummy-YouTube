from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Products
from math import ceil
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def index(request):
    if request.method == "POST":
        Username = request.POST.get('username')
        Password = request.POST.get('password')

        user = auth.authenticate(username=Username, password=Password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is Not Valid")
    else:
        return render(request, 'Music/index.html')


def signup(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        Email = request.POST.get('email')
        UserName = request.POST.get('username')
        Password1 = request.POST.get('password1')
        Checkbox = request.POST.get('checkbox')
        Password2 = request.POST.get('password2')

        if Checkbox:
            if Password1 == Password2:
                if User.objects.filter(username=UserName).exists():
                    messages.info(request, 'Username already taken')
                    print("error")
                    return redirect("signup")
                elif User.objects.filter(email=Email).exists():
                    messages.info(request, "Email Already Taken")
                    print("error")
                    return redirect("signup")
                else:
                    user = User.objects.create_user(username=UserName, password=Password1, email=Email,
                                                    first_name=firstName, last_name=lastName)
                    user.save()
                    return render(request, 'Music/index.html')
            else:
                messages.info(request, "Password Must be Same")
                return redirect("signup")
    return render(request, "Music/signup.html")


def home(request):
    product = Products.objects.all()
    slide = (len(product) // 8) + ceil((len(product)) - (len(product) // 8))
    paramas = {'no_of_song': slide, 'range': range(slide), 'product': product}
    return render(request, 'Music/first.html', paramas)


def search(request):
    if request.GET.get('search'):
        Se = request.GET.get('search')

    # img = Products.objects.filter(product_name=Se).values('image')
    img = Products.objects.all().get(product_name__exact=Se)
    a = ml(Se)
    product1 = []
    for i in range(6):
        product1.append(a[i])

    print(product1)
    para = {'product': Se, 'movie': product1, 'img': img}
    return render(request, 'Music/search.html', para)


def ml(se):
    df = pd.read_csv("C:/Users/jain2/Documents/working/movie_recommender/movie_dataset.csv")

    features = ['keywords', 'cast', 'genres', 'director']

    def combine_features(row):
        return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']

    for feature in features:
        df[feature] = df[feature].fillna('')

    df["combined_features"] = df.apply(combine_features, axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)

    def get_title_from_index(index):
        return df[df.index == index]["title"].values[0]

    def get_index_from_title(title):
        return df[df.title == title]["index"].values[0]

    movie_user_likes = se
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))

    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

    i = 0
    c = []
    for element in sorted_similar_movies:

        c.append(get_title_from_index(element[0]))
        i = i + 1
        if i > 5:
            break
    return c


def about(request):
    return render(request, 'Music/about.html')


def contact(request):
    return render(request, 'Music/contact.html')


def library(request):
    df = pd.read_csv("C:/Users/jain2/Documents/working/movie_recommender/movie_dataset.csv")

    df = df[['original_title', 'director', 'popularity', 'vote_average']]

    a = []
    b = []
    c = []
    d = []
    for i in range(100):
        a.append(df.at[i, 'original_title'])
        b.append(df.at[i, 'director'])
        c.append(df.at[i, 'popularity'])
        d.append(df.at[i, 'vote_average'])

    para = {'a': a, 'b': b, 'c': c, 'd': d, 'no': range(100), "df": df}

    return render(request, 'Music/Library.html', para)


def logout(request):
    print("call")
    auth.logout(request)
    return redirect('/')