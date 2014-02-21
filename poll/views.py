from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from poll.models import Questions

# Create your views here.

# fix issue with this query for recent_question_list
def index(request):
    recent_question_list = Questions.objects.all().order_by('-end_date')
    context = { 'recent_question_list': recent_question_list }
    return render(request, 'poll/index.html', context) 

def detail(request, poll_id):
    poll = get_object_or_404(Questions, pk=poll_id)
    return render(request, 'poll/detail.html', {'poll': poll } )

def results(request, poll_id):
    return HttpResponse("results view for poll %s" % poll_id)

def vote(request, poll_id):
    return HttpResponse("Vote view for poll %s" % poll_id)
