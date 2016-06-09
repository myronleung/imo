from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.db.models import Q, F
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, NewEntryForm, VoteForm, CommentForm, ProfileForm
from .models import UserProfile, Question, Choice, Comment, Voted, Friendship

from django.utils import timezone
# Create your views here.
def index(request):
    q_list = Question.objects.all()
    if request.GET.get("q"):
        query = request.GET.get("q")
        q_list = search_bars(q_list, query)
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

    return render(request, 'imo_app/index.html', {'q_all': q})

@login_required
def detail(request, question_id):
    current_user = request.user
    u = UserProfile.objects.get(user=current_user.id)
    q = Question.objects.get(id = question_id)
    c = Comment.objects.filter(question=q)
    v = Voted.objects.filter(voter=u, question = q)
    author = q.author.user.username
    if author == current_user.username:
        return HttpResponseRedirect(reverse('imo_app:results', args=[q.id]))
    print ('------')
    print (v)
    print ('------')
    if v:
        return HttpResponseRedirect(reverse('imo_app:results', args=[q.id]))
    else:
        return render(request, 'imo_app/detail.html', {'question':q, 'comments':c})

def view_registration(request):
    user = request.user
    if user is not None:
        if user.is_active:
            return HttpResponseRedirect(reverse('imo_app:index'))
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
            name = first_name + ' ' + last_name

            u = User.objects.create_user(username = username, password = password, email = email, first_name=first_name, last_name=last_name)
            u.save()
            p = UserProfile(user = u)
            p.name = name
            p.save()
            user = authenticate(username=username, password=password)
            login(request, user)
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
    user = request.user
    if user.is_authenticated():
        template = loader.get_template('imo_app/view_newentry.html')
        # Display formg
        form = NewEntryForm()
        return render(request, 'imo_app/view_newentry.html', {'form': form})
    else:
        raise Http404
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
            author_name = author.user.first_name + author.user.last_name
            description = form.cleaned_data['description']
            pub_date = timezone.now()
            choice1 = form.cleaned_data['choice1']
            choice2 = form.cleaned_data['choice2']
            choice3 = form.cleaned_data['choice3']
            image1 = instance.image1
            image2 = instance.image2
            image3 = instance.image3
            q = Question(question_text = question_text, author = author, author_name = author_name, description = description, pub_date = pub_date, choice1 = choice1, choice2 = choice2, choice3 = choice3, image1 = image1, image2 = image2, image3 = image3)
            q.save()
            c1 = Choice(question = q, choice_text = choice1, image = image1)
            c1.save()
            c2 = Choice(question = q, choice_text = choice2, image = image2)
            c2.save()
            c3 = Choice(question = q, choice_text = choice3, image = image3)
            c3.save()
            author_name = q.author.user.username
            if (author_name == current_user.username):
                q.total_votes += 1
                return HttpResponseRedirect(reverse('imo_app:results', args=[q.id]))
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('imo_app:detail', args=[q.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewEntryForm()

    return render(request, 'imo_app/view_newentry.html', {'form': form})

@login_required
def submit_vote(request, question_id):
    current_user = request.user
    question = get_object_or_404(Question, pk=question_id)
    u =  UserProfile.objects.get(id=current_user.id)
    v = Voted.objects.filter(question=question, voter=current_user.id)
    if v:
        return HttpResponseRedirect(reverse('imo_app:results', args=[question.id]))
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
        choices = Choice.objects.all().filter(question=question)
        choice1 = choices[0].votes
        choice2 = choices[1].votes
        choice3 = choices[2].votes
        question.total_votes = choice1 + choice2 + choice3
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

@login_required
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

@login_required
def results(request, question_id):
    q = Question.objects.get(id = question_id)
    c = Comment.objects.filter(question=q)
    author = q.author.user.username
    if (author == request.user.username):
        check_author = '1'
    else:
        check_author = ''
    choices = Choice.objects.filter(question = q)
    for i in choices:
        i.percentage = round((i.votes / q.total_votes) * 100, 2)
    context = {'question':q, 'choices': choices, 'comments': c, 'check_author': check_author}
    return render(request, 'imo_app/results.html', context)

@login_required
def edit(request, id=None):
    if (request.POST.get('delete')):
        Question.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('imo_app:index'))
    #since we don't have choice saved in question, set instance.values for form
    #if user clicked delete, delete post
    #else, create new form
    instance = Question.objects.get(id=id)
    old_choices = Choice.objects.all().filter(question=instance)
    author = instance.author
    current_user = request.user
    if author.user.username == current_user.username:
        if (request.POST.get('edit')):
            instance.choice1 = old_choices[0]
            instance.image1 = old_choices[0].image
            instance.choice2 = old_choices[1]
            instance.image2 = old_choices[1].image
            instance.choice3 = old_choices[2]
            instance.image3 = old_choices[2].image
            form = NewEntryForm(instance=instance)
        elif request.method == 'POST':
            form = NewEntryForm(request.POST or None, request.FILES or None, instance=instance)
            if form.is_valid():
                # process the data in form.cleaned_data as required
                instance = form.save(commit=False)
                instance.save()
                #collect all the old images
                image1 = old_choices[0].image
                image2 = old_choices[1].image
                image3 = old_choices[2].image
                #gather the new choices as the choises
                choice1 = instance.choice1
                choice2 = instance.choice2
                choice3 = instance.choice3
                #gather all the images from form
                new_image1 = instance.image1
                new_image2 = instance.image2
                new_image3 = instance.image3

                #update images
                #if the instance is the old image, just use old image
                #first image
                if new_image1 == '':
                    image1 = image1
                else:
                    image1 = new_image1
                #if the clear box is checked, this will remove image
                if request.POST.get('image1-clear'):
                    image1 = ''
                #second image
                if new_image2 == '':
                    image2 = image2
                else:
                    image2 = new_image2
                if request.POST.get('image2-clear'):
                    image2 = ''
                #third image
                if new_image3 == '':
                    image3 = image3
                else:
                    image3 = new_image3
                if request.POST.get('image3-clear'):
                    image3 = ''

                #update votes
                #if any change in the choice
#                if choice1 != old_choices[0] or image1 != old_choices[0].image or request.POST.get('image1-clear'):
#                    #remove the votes for that choice from total votes
#                    instance.total_votes = instance.total_votes - old_choices[0].votes
#                    #set total votes to 0
#                    votes1 = 0
#                #else leave it the same
#                else:
#                    votes1 = old_choices[0].votes
#
#                #choice2
#                if choice2 != old_choices[1] or image2 != old_choices[1].image or request.POST.get('image2-clear'):
#                    #remove the votes for that choice from total votes
#                    instance.total_votes = instance.total_votes - old_choices[1].votes
#                    #set total votes to 0
#                    votes2 = 0
#                #else leave it the same
#                else:
#                    votes2 = old_choices[1].votes
#
#                #choice3
#                if choice3 != old_choices[2] or image3 != '' and image3 != old_choices[2].image or request.POST.get('image3-clear'):
#                    #remove the votes for that choice from total votes
#                    instance.total_votes = instance.total_votes - old_choices[2].votes
#                    #set total votes to 0
#                    votes3 = 0
#                #else leave it the same
#                else:
#                    votes3 = old_choices[2].votes
                #delete the old choices so we can add the new ones
                Choice.objects.filter(question=instance).delete()
                #add the new choices
                c1 = Choice(question = instance, choice_text = choice1, image = image1) # votes = votes1)
                c2 = Choice(question = instance, choice_text = choice2, image = image2) # votes = votes2)
                c3 = Choice(question = instance, choice_text = choice3, image = image3) # votes = votes3)
                c1.save()
                c2.save()
                c3.save()
                return HttpResponseRedirect(reverse('imo_app:results', args=[instance.id]))
        context = {
            "instance": instance,
            "form": form,
        }
        return render(request, "imo_app/change_entry.html", context)
    elif author != current_user:
        raise Http404

@login_required
def your_posts(request):
    current_user = request.user
    author = UserProfile.objects.get(id=current_user.id)
    q_list = Question.objects.filter(author=author)
    if request.GET.get("q"):
        query = request.GET.get("q")
        q_list = search_bars(q_list, query)
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
    context = {'q_all': q, 'current_user': current_user}
    return render(request, 'imo_app/your_posts.html', context)

@login_required
def profile(request):
    #Calls
    current_user=request.user
    author = UserProfile.objects.get(id=current_user.id)
    friends_list = Friendship.objects.filter(requester=current_user.id, status='Friends')[:10]
    q_list = Question.objects.filter(author=author)
    total_friends = author.total_friends
    #if trying to edit
    if (request.POST.get('edit')):
        form = ProfileForm(instance=author)
        return render(request, 'imo_app/profile_form.html', {'form': form})
    elif request.method == 'POST':
        form = ProfileForm(request.POST or None, request.FILES or None, instance=author)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            current_user=request.user
            instance.save()
            author = UserProfile.objects.get(id=current_user.id)
            q_list = Question.objects.filter(author=author)
            if request.GET.get("q"):
                query = request.GET.get("q")
                q_list = search_bars(q_list, query)
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
            #paginator for friends
            paginator = Paginator(friends_list, 20) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                f = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                f = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                f = paginator.page(paginator.num_pages)
            context = {
                'friends': total_friends,
                'f_all': f,
                'q_all': q,
                'current_user': current_user,
                'first_name': author.user.first_name,
                'last_name': author.user.last_name,
                'gender': author.gender,
                'birthday': author.birthday,
                'about': author.about,
                'email': author.user.email,
                'motto': author.motto,
                'picture': author.picture,
            }
            return render(request, 'imo_app/profile.html', context)
        context = {
            "instance": instance,
            "form": form,
        }
        return render(request, 'imo_app/profile_form.html', context)
    #check if they have a query
    if request.GET.get("q"):
        query = request.GET.get("q")
        q_list = search_bars(q_list, query)
    paginator = Paginator(q_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        q = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        q = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        q = paginator.page(paginator.num_pages)

    requests = ''
    if Friendship.objects.filter(friend=current_user.id, status='requested'):
        requests = Friendship.objects.filter(friend=current_user.id, status='requested')[:5]
    context = {
        'requests': requests,
        'friends': total_friends,
        'f_all': friends_list,
        'q_all': q,
        'current_user': current_user,
        'first_name': author.user.first_name,
        'last_name': author.user.last_name,
        'gender': author.gender,
        'birthday': author.birthday,
        'about': author.about,
        'email': author.user.email,
        'motto': author.motto,
        'picture': author.picture,
    }
    return render(request, 'imo_app/profile.html', context)

@login_required
def view_profile(request, id):
    current_user = request.user
    profile = UserProfile.objects.get(id=id)
    q_list = Question.objects.filter(author=profile)
    friends_list = Friendship.objects.filter(requester=id, status='Friends')[:10]
    #set status to empty in case they aren't friends
    status = ''
    # check if they're friends
    if Friendship.objects.filter(requester=current_user.id, friend=id):
        friend_check = Friendship.objects.get(requester=current_user.id, friend=id)
        status = friend_check.status
    total_friends = profile.total_friends
    #check if it's their own profile and if so return a value of 1
    same_user = False
    if current_user.id == profile.id:
        same_user = True
    #paginator for questions
    paginator = Paginator(q_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        q = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        q = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        q = paginator.page(paginator.num_pages)
    context = {
        'same_user':same_user,
        'status': status,
        'friends': total_friends,
        'f_all': friends_list,
        'q_all': q,
        'first_name': profile.user.first_name,
        'last_name': profile.user.last_name,
        'gender': profile.gender,
        'birthday': profile.birthday,
        'about': profile.about,
        'email': profile.user.email,
        'motto': profile.motto,
        'picture': profile.picture,
        'id': id
    }
    return render(request, 'imo_app/view_profile.html', context)

@login_required
def search(request):
    q_list = Question.objects.all()
    prof_list = UserProfile.objects.all()
    query = request.GET.get("a")
    if query == "":
        return HttpResponseRedirect(reverse('imo_app:index'))
    prof_list = UserProfile.objects.filter(
        Q(name__icontains=query)|
        Q(motto__icontains=query)
        )
    q_list = search_bars(q_list, query)
    #paginator for questions
    paginator = Paginator(q_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        q = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        q = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        q = paginator.page(paginator.num_pages)
    #paginator for profiles
    paginator = Paginator(prof_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        p = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        p = paginator.page(paginator.num_pages)
    context = {
        'q_all': q,
        'p_all': p,
        'query': query
    }
    return render(request, 'imo_app/search.html', context)


def search_bars(q_list, query):
    if query:
        choices = 'do not have this string'
        choice = Choice.objects.filter(choice_text = query)
        if choice:
            choices = Choice.objects.get(id = choice)
        q_list = q_list.filter(
            Q(author_name__icontains=query)|
            Q(question_text__icontains=query)|
            Q(description__icontains=query)|
            Q(choice1__icontains=choices)|
            Q(choice2__icontains=choices)|
            Q(choice3__icontains=choices)
            ).distinct()
        return q_list

#def paginator(q_list, num):
#    paginator = Paginator(q_list, num) # Show 25 contacts per page
#    page = request.GET.get('page')
#    try:
#        q = paginator.page(page)
#    except PageNotAnInteger:
#        # If page is not an integer, deliver first page.
#        q = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range (e.g. 9999), deliver last page of results.
#        q = paginator.page(paginator.num_pages)
#    return q

@login_required
def all_friends(request, user_id):
    friends_list = Friendship.objects.filter(requester=user_id, status='Friends')
    if request.GET.get("f"):
        query = request.GET.get("f")
        query_people = UserProfile.objects.filter(
            Q(name__icontains=query)
            ).values('id')
        friends_list = Friendship.objects.filter(requester=user_id, friend__in=query_people)
    context = {
        'f_all': friends_list
    }
    return render(request, 'imo_app/friends.html', context)

@login_required
def friends_polls(request):
    current_user = request.user
    # .values makes it so that it creates a dictionary
    friends = Friendship.objects.filter(requester=current_user.id).values('friend_id')
    # author in checks whether or not the dictionary has that value, and if so counts that as one
    q_list = Question.objects.filter(author__in=friends)
    if request.GET.get("q"):
        query = request.GET.get("q")
        q_list = search_bars(q_list, query)
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
    requests = ''
    if Friendship.objects.filter(friend=current_user.id, status='requested'):
        requests = Friendship.objects.filter(friend=current_user.id, status='requested')[:5]
    context = {
        'requests': requests,
        'q_all': q
        }
    return render(request, 'imo_app/friends_polls.html', context)

@login_required
def request_friend(request, friend_id):
    current_user = request.user
    requester = UserProfile.objects.get(id=current_user.id)
    profile = UserProfile.objects.get(id=friend_id)
    if Friendship.objects.filter(requester=current_user.id, friend=friend_id):
        pass
    elif Friendship.objects.filter(requester=friend_id, friend=current_user.id, status='requested'):
        friend = Friendship(requester=requester, friend=profile, status='Friends')
        friend.save()
        accept_friend(request, friend_id)
    else:
        friend = Friendship(requester=requester, friend=profile, status='requested')
        friend.save()

    return HttpResponseRedirect(reverse('imo_app:view_profile', args=[profile.id]))

@login_required
def accept_friend(request, friend_id):
    current_user = request.user
    friend1 = Friendship.objects.get(requester=current_user.id, friend=friend_id)
    friend2 = Friendship.objects.get(requester=friend_id, friend=current_user.id)
    friend1.status = 'Friends'
    friend2.status = 'Friends'
    friend1.save()
    friend2.save()

    #update total_friends
    person1 = UserProfile.objects.get(id=current_user.id)
    person2 = UserProfile.objects.get(id=friend_id)
    person1.total_friends = person1.total_friends + 1
    person2.total_friends = person2.total_friends + 1
    person1.save()
    person2.save()

    return

@login_required
def accept_friend_profile(request, friend_id):
    current_user = request.user
    requester = UserProfile.objects.get(id=current_user.id)
    profile = UserProfile.objects.get(id=friend_id)
    current_user = request.user
    friend = Friendship(requester=requester, friend=profile, status='Friends')
    friend.save()
    friend1 = Friendship.objects.get(requester=current_user.id, friend=friend_id)
    friend2 = Friendship.objects.get(requester=friend_id, friend=current_user.id)
    friend1.status = 'Friends'
    friend2.status = 'Friends'
    friend1.save()
    friend2.save()

    #update total_friends
    person1 = UserProfile.objects.get(id=current_user.id)
    person2 = UserProfile.objects.get(id=friend_id)
    person1.total_friends = person1.total_friends + 1
    person2.total_friends = person2.total_friends + 1
    person1.save()
    person2.save()

    return HttpResponseRedirect(reverse('imo_app:profile'))

@login_required
def decline_friend_profile(request, friend_id):
    current_user = request.user
    friend = Friendship.objects.filter(requester=friend_id, friend=current_user.id)
    friend.delete()

    return HttpResponseRedirect(reverse('imo_app:profile'))

@login_required
def accept_friend_friends_feed(request, friend_id):
    current_user = request.user
    requester = UserProfile.objects.get(id=current_user.id)
    profile = UserProfile.objects.get(id=friend_id)
    current_user = request.user
    friend = Friendship(requester=requester, friend=profile, status='Friends')
    friend.save()
    friend1 = Friendship.objects.get(requester=current_user.id, friend=friend_id)
    friend2 = Friendship.objects.get(requester=friend_id, friend=current_user.id)
    friend1.status = 'Friends'
    friend2.status = 'Friends'
    friend1.save()
    friend2.save()

    #update total_friends
    person1 = UserProfile.objects.get(id=current_user.id)
    person2 = UserProfile.objects.get(id=friend_id)
    person1.total_friends = person1.total_friends + 1
    person2.total_friends = person2.total_friends + 1
    person1.save()
    person2.save()

    return HttpResponseRedirect(reverse('imo_app:friends_feed'))

@login_required
def decline_friend_friends_feed(request, friend_id):
    current_user = request.user
    friend = Friendship.objects.filter(requester=friend_id, friend=current_user.id)
    friend.delete()

    return HttpResponseRedirect(reverse('imo_app:friends_feed'))

@login_required
def remove_friend(request, friend_id):
    current_user=request.user
    friend1 = Friendship.objects.get(requester=current_user.id, friend=friend_id)
    friend2 = Friendship.objects.get(requester=friend_id, friend=current_user.id)
    friend1.delete()
    friend2.delete()

    #remove total_friends
    person1 = UserProfile.objects.get(id=current_user.id)
    person2 = UserProfile.objects.get(id=friend_id)
    person1.total_friends = person1.total_friends - 1
    person2.total_friends = person2.total_friends - 1
    person1.save()
    person2.save()

    return HttpResponseRedirect(reverse('imo_app:index'))
