
from django.shortcuts import render
from django.http import HttpResponse
from poll.models import Questions

# Create your views here.

# fix issue with this query for recent_question_list
def index(request):
    recent_question_list = Questions.objects.order_by('-end_date')
    context = { 'recent_question_list': recent_question_list }
    return render(request, 'poll/index.html', context) 

def detail(request, poll_id):
    return HttpResponse("detail view for poll %s" % poll_id)

def results(request, poll_id):
    return HttpResponse("results view for poll %s" % poll_id)

def vote(request, poll_id):
    return HttpResponse("Vote view for poll %s" % poll_id)
