from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *
from django.http import HttpResponse
from datetime import datetime, timedelta
import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#@login_required(login_url='login')
def home(request):

    return render(request,'polls/home.html')



def OtpPage(request):
    error_message =None
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']
        #print(f"USERNAME {username}")
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until =datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(MyUser, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    return redirect('home')
                else:
                    error_message = "Invalid confirmation codes"
            else:
                error_message = "Confirmation codes  have expired"
        else:
            error_message = "something went wrong"



    return render(request,'polls/OtpPage.html', {'error_message':error_message})

@login_required(login_url='login')
def AllElectionCategories(request):
    categories = ElectionCategories.objects.all()

    context = {
        "categories":categories,
    }

    return render(request,'polls/ElectionCategories.html',context)

@login_required()
def polls_list(request,id):
    #all_polls = 0
    all_polls=0
    params=0
    search_term =0
    
    categoryId = ElectionCategories.objects.get(id=id)
    categoryIdName = categoryId.Category

    # Storing speech in a variable to use later
    request.session['categoryIdName'] = categoryIdName

    if not (request.user.is_superuser) and categoryIdName == "CR":
        login_user_course = request.user.Course.CourseName
        login_user_year = request.user.Year.Name

    
        print(f"LOGIN {login_user_course}")
        print(f"LOGIN {login_user_year}")

        all_polls = Poll.objects.filter(
                    Category__id__icontains = categoryId.id,
                    Course__CourseName__icontains = login_user_course,
                    Year__Name__icontains = login_user_year

                    )

        search_term = ''
        if 'name' in request.GET:
            all_polls = all_polls.order_by('text')

        if 'date' in request.GET:
            all_polls = all_polls.order_by('pub_date')

        if 'vote' in request.GET:
            all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

        if 'search' in request.GET:
            search_term = request.GET['search']
            all_polls = all_polls.filter(text__icontains=search_term)

        paginator = Paginator(all_polls, 100)  # Show 6 contacts per page
        page = request.GET.get('page')
        polls = paginator.get_page(page)

        get_dict_copy = request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
        print(params)



    elif not (request.user.is_superuser) and categoryIdName == "WABUNGE":
        login_user_college = request.user.College.CollegeName
        login_user_location = request.user.Location.LocationName

    
        print(f"LOGIN WABUNGE {login_user_college}")
        print(f"LOGIN WABUNGE {login_user_location}")

        all_polls = Poll.objects.filter(
                    Category__id__icontains = categoryId.id,
                    College__CollegeName__icontains = login_user_college,
                    Location__LocationName__icontains = login_user_location,
                    is_off_cumpus=True

                    )

        search_term = ''
        if 'name' in request.GET:
            all_polls = all_polls.order_by('text')

        if 'date' in request.GET:
            all_polls = all_polls.order_by('pub_date')

        if 'vote' in request.GET:
            all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

        if 'search' in request.GET:
            search_term = request.GET['search']
            all_polls = all_polls.filter(text__icontains=search_term)

        paginator = Paginator(all_polls, 100)  # Show 6 contacts per page
        page = request.GET.get('page')
        polls = paginator.get_page(page)

        get_dict_copy = request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
        print(params)

    

    else:

        all_polls = Poll.objects.filter(
                    Category__id__icontains = categoryId.id
                    )

        search_term = ''
        if 'name' in request.GET:
            all_polls = all_polls.order_by('text')

        if 'date' in request.GET:
            all_polls = all_polls.order_by('pub_date')

        if 'vote' in request.GET:
            all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

        if 'search' in request.GET:
            search_term = request.GET['search']
            all_polls = all_polls.filter(text__icontains=search_term)

        paginator = Paginator(all_polls, 100)  # Show 6 contacts per page
        page = request.GET.get('page')
        polls = paginator.get_page(page)

        get_dict_copy = request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
        print(params)

    context = {
        'all_polls': all_polls,
        #'all_polls': all_polls,
        'params': params,
        'search_term': search_term,
        'categoryIdName':categoryIdName,

    }
    return render(request, 'polls/polls_list.html', context)


@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)  # Show 7 contacts per page

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'polls/polls_list.html', context)


@login_required()
def polls_add(request):
    categoryIdName = request.session.get('categoryIdName', '')
    print(f"Category {categoryIdName}")

    if request.user.has_perm('polls.add_poll'):
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            if form.is_valid:
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                new_choice1 = Choice(
                    poll=poll, choice_text=form.cleaned_data['choice1']).save()
                new_choice2 = Choice(
                    poll=poll, choice_text=form.cleaned_data['choice2']).save()

                messages.success(
                    request, "Poll & Choices added successfully", extra_tags='alert alert-success alert-dismissible fade show')

                return redirect('add')
        else:
            form = PollAddForm()
        context = {
            'form': form,
            'categoryIdName':categoryIdName,
        }
        return render(request, 'polls/add_poll.html', context)
    else: 
        return HttpResponse("Sorry but you don't have permission to do that!")


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("AllElectionCategories")

    else:
        form = EditPollForm(instance=poll)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    poll.delete()
    messages.success(request, "Poll Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("AllElectionCategories")


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('edit', poll.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()
    messages.success(
        request, "Choice Deleted successfully", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('edit', poll.id)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll_detail.html', context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("AllElectionCategories")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("detail", poll_id)
    return render(request, 'polls/poll_result.html', {'poll': poll})


@login_required
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        return render(request, 'polls/poll_result.html', {'poll': poll})
