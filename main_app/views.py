from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from django.db.models import Count
from .form import FlagForm, JoinTeamForm, CreateTeamForm, UserCreation
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import *
# Create your views here.

def get_contest():
    contest = Contest.objects.all()[0]
    start_time = contest.start_time.replace(tzinfo=None)
    end_time = contest.end_time.replace(tzinfo=None)
    now = datetime.now()
    if start_time <= now <= end_time:
        contest.contest_status = 1
    elif now > end_time:
        contest.contest_status = 2
    else:
        contest.contest_status = 0
    contest.save()
    return contest

@login_required(login_url='welcome')
def questions(request):
    contest = get_contest()
    if not request.user.is_superuser:
        if not(request.user.user_status == 2 and contest.contest_status >= 1):
            raise Http404('Not found')
    questions = Question.objects.values('pk', 'title', 'score', 'cat', 'created').annotate(solved_count=Count('teams')).order_by('created')
    list_of_pk = request.user.team.solved_questions.values_list('pk', flat=True)

    for question in questions:
        if question['pk'] in list_of_pk:
            question['solved'] = True
        else:
            question['solved'] = False
    delta_time = timedelta(hours=3, minutes=30)
    context = {
        'questions': questions,
        'user': request.user,
        'endTime': contest.end_time + delta_time
    }
    return render(request, 'main_app/dashboard.html', context)


@login_required(login_url='welcome')
def question(request, pk):
    contest = get_contest()
    if not request.user.is_superuser:
        if not (request.user.user_status == 2 and contest.contest_status >= 1):
            raise Http404('Not found')
    if contest.contest_status == 2:
        finished = True
    else:
        finished = False
    is_flag_registered = False
    question = Question.objects.get(pk=pk)
    questions = Question.objects.all().order_by('created')
    form = FlagForm()

    if question in request.user.team.solved_questions.all():
        is_flag_registered = True

    if request.method == 'POST' and finished == False:
        if is_flag_registered:
            messages.error(request, 'The flag has already been registered')
        else:
            form = FlagForm(request.POST)
            if form.is_valid():
                flag = form.cleaned_data.get('flag')
                if flag == question.flag:
                    if question.teams.count() != 0 and (question.score - (question.main_score * 0.05)) >= (question.main_score/2):
                        question.score = int(question.score - (question.main_score * 0.05))
                        question.save()
                    request.user.team.solved_questions.add(question)
                    is_flag_registered = True
                else:
                    messages.error(request, 'Wrong answer!!!')
    delta_time = timedelta(hours=3, minutes=30)
    context = {
        'question': question,
        'form': form,
        'flag': is_flag_registered,
        'questions': questions,
        'user': request.user,
        'finished': finished,
        'endTime': contest.end_time + delta_time
    }
    return render(request, 'main_app/question-detail.html', context)




@login_required(login_url='welcome')
def join_team(request):
    contest = get_contest()
    if contest.contest_status >= 1:
        raise Http404('Not Found')
    if request.method == 'POST':
        if not request.user.user_status >= 1:
            raise Http404('you should verify your account')
        join_form = JoinTeamForm(request.POST)
        if join_form.is_valid():
            uid = join_form.cleaned_data.get('token')
            try:
                team = Team.objects.get(join_team_uuid=uid)
                if team.customuser_set.count() == 2:
                    messages.error(request, 'Sorry. This team is full')
                else:
                    if request.user.team and request.user.team.customuser_set.all().count() == 1:
                        if not request.user.team == team:
                            request.user.team.delete()
                    request.user.team = team
                    messages.success(request, 'You have successfully joined')
                    request.user.user_status = 2
                    request.user.save()
            except Team.DoesNotExist:
                msg = 'There is no team with this token'
                messages.error(request, msg)
        create_form = CreateTeamForm()
        if request.user.team:
            hash = request.user.team.join_team_uuid
            team_name = request.user.team.name
        else:
            hash = ''
            team_name = ''
        delta_time = timedelta(hours=3, minutes=30)
        context = {
            'create_form': create_form,
            'join_form': join_form,
            'verify': True,
            'user': request.user,
            'hash': hash,
            'team_name': team_name,
            'startTime': contest.start_time + delta_time
        }
        return render(request, 'main_app/createTeam.html', context)
    else:
        raise Http404('Not Found')


@login_required(login_url='welcome')
def create_team(request):
    contest = get_contest()
    if contest.contest_status >= 1:
        raise Http404('Not Found')
    delta_time = timedelta(hours=3, minutes=30)
    if request.user.user_status >= 1:
        hash = ''
        team_name = ''
        create_form = CreateTeamForm()
        if request.method == 'POST':
            if not request.user.team:
                create_form = CreateTeamForm(request.POST)
                if create_form.is_valid():
                    name = create_form.cleaned_data.get('name')
                    team = Team.objects.create(name=name)
                    request.user.team = team
                    request.user.user_status = 2
                    request.user.save()
                    hash = team.join_team_uuid
                    team_name = team.name
                    messages.success(request, 'Team create successfully')
            else:
                messages.error(request, 'You have already joined a team')

        if request.user.team:
            team_name = request.user.team.name
            hash = request.user.team.join_team_uuid
        join_form = JoinTeamForm()
        context = {
            'create_form': create_form,
            'join_form': join_form,
            'verify': True,
            'user': request.user,
            'hash': hash,
            'team_name': team_name,
            'startTime': contest.start_time + delta_time
        }
        return render(request, 'main_app/createTeam.html', context)
    else:
        context = {
            'verify': False,
            'user': request.user,
            'startTime': contest.start_time + delta_time
        }
        return render(request, 'main_app/createTeam.html', context)


def registeruser(request):
    contest = get_contest()
    if contest.contest_status >= 1:
        raise Http404('Not Found')
    form = UserCreation()
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'your account has been created successfully')
            messages.success(request, 'Please Login and verify your account')
            return redirect('login')
        # else:
            # messages.error(request, 'Error in registraion')

    context = {
        'form': form,
    }

    return render(request, 'main_app/signup.html', context)


@login_required(login_url='welcome')
def table(request):
    contest = get_contest()
    if not (request.user.user_status == 2 and contest.contest_status >= 1):
        raise Http404('Not found')
    questions = Question.objects.all()
    teams = sorted(Team.objects.all(), key=lambda t: t.total_score, reverse=True)
    # teams = .order_by('total_score')
    delta_time = timedelta(hours=3, minutes=30)
    context = {
        'questions': questions,
        'teams': teams,
        'user': request.user,
        'endTime': contest.end_time + delta_time
    }
    return render(request, 'main_app/scoreBoard.html', context)


def loginuser(request):
    contest = get_contest()
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            get_user_model().objects.get(username=username)
        except:
            messages.error(request, "username dose not  exist")
            return render(request, 'main_app/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if contest.contest_status >= 1:
                return redirect('questions')
            else:
                return redirect('create-team')
        else:
            messages.error(request, "username Or password is incorrect")
    return render(request, 'main_app/login.html')


@login_required(login_url='welcome')
def logoutuser(request):
    logout(request)
    return redirect('welcome')


def first_page(request):
    return render(request, 'main_app/firstPG.html')

def redirect_view(request):
    return redirect('welcome')
