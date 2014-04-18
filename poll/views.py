from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.core.mail import send_mail
from django.utils import timezone
from django.forms import ModelForm
from django.contrib import messages
import hashlib
import random
#from random import randint
from poll.models import Questions, Answers, Votes, Users, Users_Questions_Hash


def index(request):
    recent_question_list = Questions.objects.all().order_by('-end_date')
    context = { 'recent_question_list': recent_question_list }
    return render(request, 'poll/index.html', context) 

# here is where you would check the querystring token ?token=blahblah. use the hash code
# of the token to validate. you should not put the token in the database. safer this way.
# have a separate page (poll/) where you have to log in. The authentication processs shoudl
# be the same as when you log into the admin. from that page you can log in and see the list 
# of the poll topics. next to each one is a button to send out the emails. use the 
# send_mass_email option. look at the django documentation.
# the entire site will be SSL (certificate). for internal testing use a self-signed cert.
# the details page is where the URL in the email will send people. There should be code here 
# (see top sentence of comment) to validate the token and tell who is the person who clicked 
# the link. from that you also know the question. then. after they vote, i can register the results
# in the table and display the results.

# look up the answer_id across from vote when it redirects to the results page. right now it is 
# including the p.id as an argument. look into adding an optionl argument, which will be the 
# selected choice.

#In [19]: v = Votes(answer_value=Answers.objects.get(id=1),voter=Users.objects.get(id=2),answer_timestamp=timezone.now() )

def detail(request, poll_id):
    poll = get_object_or_404(Questions, pk=poll_id)
    return render(request, 'poll/detail.html', {'poll': poll } )

def results(request, poll_id):
    poll = get_object_or_404(Questions, pk=poll_id)
    allvotes2 = poll.get_poll_results(poll_id)
    allvotes = get_list_or_404(Votes.objects.filter(answer_value_id__question_id__id=poll_id ) )
    return render(request, 'poll/results.html', {'allvotes': allvotes, 'allvotes2': allvotes2, 'poll': poll} )

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
        v = Votes(answer_value=selected_choice,voter=Users.objects.get(id=3),answer_timestamp=timezone.now() )
        v.save()
        messages.add_message(request, messages.INFO, selected_choice)
    
    return HttpResponseRedirect(reverse('poll:results', args=(p.id,) ) )


def sendemail(request, poll_id):
    users = Users.objects.filter(is_active=1) #put explicit email address call
    question = get_object_or_404(Questions, pk=poll_id)
    for user in users:        
        salt = str(random.randint(1,1000))
        token = u'%s:%s:%s' % (user.email_address, question.question_text, salt)
        hashed_token = hashlib.sha1(token).hexdigest()
        Users_Questions_Hash.objects.create(voter=user, question=question, hash_value=hashed_token, is_valid=1)
    return HttpResponseRedirect(reverse('poll:index' ) )



#ValueError at /poll/1/sendemail/
#Cannot assign "2L": "Users_Questions_Hash.voter" must be a "Users" instance.
