from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from poll.models import Questions, Answers


# Create your views here.


def index(request):
    recent_question_list = Questions.objects.all().order_by('-end_date')
    context = { 'recent_question_list': recent_question_list }
    return render(request, 'poll/index.html', context) 

def detail(request, poll_id):
    poll = get_object_or_404(Questions, pk=poll_id)
    return render(request, 'poll/detail.html', {'poll': poll } )

def results(request, poll_id):
    poll = get_object_or_404(Questions, pk=poll_id)
    return render(request, 'poll/results.html', {'poll': poll} )

def vote(request, poll_id):
    p = get_object_or_404(Questions, pk=poll_id)
    try:
        selected_choice = p.answers_set.get(pk=request.POST['answer'])
    except (KeyError, Answers.DoesNotExist):
        # redisplay the voting form
        return render(request, 'poll/detail.html', {
            'poll': p,
            'error_message': 'Please select a choice',
        })
    # here is where to save the vote results to the Votes table
    else:
        pass


    
    return HttpResponseRedirect(reverse('poll:results', args=(p.id,) ) )
