# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import sklearn
import pandas as pd
from pages.models import Item, ToDoList
from django.shortcuts import render, redirect
from .forms import RegisterForm


def homePageView(request):
    return render(request, 'home.html', {
        'mynumbers': [1, 2, 3, 4, 5, 6],
        'firstName': 'Sally',
        'lastName': 'Poon',
    })


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')


def sallyPageView(request):
    return render(request, 'sally.html')


def homePost(request):
    # Use request object to extract choice.

    choice = -999
    gmat = -999

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']

        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice = int(currentChoice)
        gmat = float(gmatStr)
    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice': choice, 'gmat': gmat}, ))


def results(request, choice, gmat):
    print("*** Inside reults()")
    # load saved model
    with open('./model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf.append({'gmat': gmat,
                                            'work_experience': workExperience},
                                           ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat': gmat,
                                            'prediction': singlePrediction})


def todos(request):
    print("*** Inside todos()")
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    return render(request, 'todos.html',
                  {'ToDoItemDetail': itemErrandDetail})


def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('message',
                                                kwargs={'msg': "Your are registered.", 'title': "Success!"}, ))

    # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})


def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title })


def secretArea(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('message',
               kwargs={'msg': "Please login to access this page.",
                       'title': "Login required."}, ))
    return render(request, 'secret.html', {'useremail': request.user.email })

