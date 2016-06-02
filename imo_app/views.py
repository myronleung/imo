from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, NewEntryForm, VoteForm, CommentForm
from .models import UserProfile, Question, Choice, Comment, Voted

from django.utils import timezone
# Create your views here.
def index(request):
    q_list = Question.objects.all()
    query = request.GET.get("q")
    if query:
        q_list = q_list.filter(
            Q(question_text__icontains=query)|
            Q(description__icontains=query)|
            Q(choice1__icontains=query)|
            Q(choice2__icontains=query)|
            Q(choice3__icontains=query)
            ).distinct()

    paginator = Paginator(q_list, 12) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        q = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        q = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        q = paginator.page(paginator.num_pages)
    current_user = request.user
    context = {'q_all': q, 'current_user': current_user}
    return render(request, 'imo_app/index.html', context)

@login_required
def detail(request, question_id):
    current_user = request.user
    u = UserProfile.objects.get(user=current_user)
    q = Question.objects.get(id = question_id)
    c = Comment.objects.filter(question=q)
    v = Voted.objects.filter(voter=u, question = q)
    print ('------')
    print (v)
    print ('------')
    if v:
        return HttpResponseRedirect(reverse('imo_app:results', args=[q.id]))
    else:
        return render(request, 'imo_app/detail.html', {'question':q, 'comments':c,})

def view_registration(request):
    template = loader.get_template('imo_app/view_registration.html')
    # Display formform = LoginForm()
    form = RegistrationForm()
    return render(request, 'imo_app/view_registration.html', {'form': form})

def submit_registration(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            u = User.objects.create_user(username = username, password = password, email = email, first_name=first_name, last_name=last_name)
            u.save()
            p = UserProfile(user = u)
            p.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('imo_app:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'imo_app/view_registration.html', {'form': form})

def view_login(request):
    template = loader.get_template('imo_app/view_login.html')
    form = LoginForm()
    return render(request, 'imo_app/view_login.html', {'form': form})

def submit_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    # redirect to a new URL:
                    return HttpResponseRedirect(reverse('imo_app:index'))
                else:
                    # Return a 'disabled account' error message
                    # redirect to a new URL:
                    return HttpResponseRedirect(reverse('imo_app:index'))
            else:
                # Return an 'invalid login' error message.
                # redirect to a new URL:
                error_message = 'Login Failed'
                context = {'form':form, 'error_message':error_message}
                return render(request, 'imo_app/view_login.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'imo_app/view_login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('imo_app:index'))

def view_newentry(request):
    template = loader.get_template('imo_app/view_newentry.html')
    # Display formg
    form = NewEntryForm()
    return render(request, 'imo_app/view_newentry.html', {'form': form})

def submit_newentry(request, id=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewEntryForm(request.POST or None, request.FILES or None)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            current_user = request.user
            question_text = form.cleaned_data['question_text']
            author =  UserProfile.objects.get(id=current_user.id)
            description = form.cleaned_data['description']
            pub_date = timezone.now()
            choice1 = form.cleaned_data['choice1']
            choice2 = form.cleaned_data['choice2']
            choice3 = form.cleaned_data['choice3']
            image1 = instance.image1
            image2 = instance.image2
            image3 = instance.image3
            q = Question(question_text = question_text, author = author, description = description, pub_date = pub_date)
            q.save()
            c1 = Choice(question = q, choice_text = choice1, image = image1)
            c1.save()
            c2 = Choice(question = q, choice_text = choice2, image = image2)
            c2.save()
            c3 = Choice(question = q, choice_text = choice3, image = image3)
            c3.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('imo_app:detail', args=[q.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewEntryForm()

    return render(request, 'imo_app/view_newentry.html', {'form': form})

def submit_vote(request, question_id):
    current_user = request.user
    question = get_object_or_404(Question, pk=question_id)
    u =  UserProfile.objects.get(id=current_user.id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print ('----')
        print ('voted')
        print ('----')
        v = Voted(voter=u, question=question)
        v.save()
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'imo_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        question.total_votes += 1
        question.save()
        selected_choice.percentage = round((selected_choice.votes / question.total_votes) * 100.0,2)
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('imo_app:results', args=(question.id,)))
def about(request):
    return render(request, 'imo_app/about.html')
def faq(request):
    return render(request, 'imo_app/faq.html')

def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    comments = request.POST.get('comment_text')
    #Print the comments taken from the HTML
    print ("----------------")
    print (comments)
    print ("----------------")
    #If they're trying to post it, set up all the input information
    if request.POST:
        current_user = request.user
        author =  UserProfile.objects.get(id=current_user.id)
        comment_text = comments
        pub_date = timezone.now()
        #Pass the information to Comment model and save it
        comment = Comment(question = question, author = author, comment_text = comment_text, pub_date = pub_date)
        comment.save()
        #If it worked, add comment and display results
        return HttpResponseRedirect(reverse('imo_app:results', args=[question.id]))

    else:
        #If they aren't trying to post, just display results
        return render(request, 'imo_app/results.html')


def results(request, question_id):
    q = Question.objects.get(id = question_id)
    c = Comment.objects.filter(question=q)
    author = q.author.user.username
    if (author == request.user.username):
        check_author = '1'
    else:
        check_author = ''
    choices = Choice.objects.filter(question = q)
    context = {'question':q, 'choices': choices, 'comments': c, 'check_author': check_author}
    return render(request, 'imo_app/results.html', context)

def change_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if (request.POST.get('edit')):
        template = loader.get_template('imo_app/view_newentry.html')
        form = NewEntryForm(request.POST or None, instance=question)
        # Display formg
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'question': question.id,
            "title": "Detail",
            "form": form,
        }
        return render(request, "view_newentry.html", context)
    elif (request.POST.get('delete')):
        Question.objects.filter(id=question_id).delete()
        return HttpResponseRedirect(reverse('imo_app:index'))
