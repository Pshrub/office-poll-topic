from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import hashlib
import random
from poll.models import Questions, Answers, Votes, Users, Users_Questions_Hash

@permission_required('poll.can_send_poll_emails', login_url='/login')
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

# in this method, use something like this: request.GET['token']
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
        # below is the flash message.
        messages.add_message(request, messages.INFO, selected_choice)
    
    return HttpResponseRedirect(reverse('poll:results', args=(p.id,) ) )

# think about creating a template for the email and returning the template here. 
# This would have the proper separation of business logic from the display logic.
# instead of having the email specified below as text
def sendEmail(request, poll_id): 
    users = Users.objects.filter(is_active=1) 
    question = get_object_or_404(Questions, pk=poll_id)
    for user in users:        
        salt = str(random.randint(1,10000))
        token = u'%s:%s:%s' % (user.email_address, question.question_text, salt)
        hashed_token = hashlib.sha1(token).hexdigest()
        Users_Questions_Hash.objects.create(voter=user, question=question, hash_value=hashed_token, is_valid=1)
    
    # use the send_mass_mail function, which queues up all the emails and only connects one time to send out the emails.
    # https://docs.djangoproject.com/en/1.7/topics/email/#django.core.mail.send_mail
    # in the templates directory, add two files: email.html and email.txt.
    # then look at this post: http://stackoverflow.com/questions/2809547/creating-email-templates-with-django
    # or this: http://stackoverflow.com/questions/19970348/django-html-e-mail-template-doesnt-load-css-in-the-e-mail

        subject = 'Vote in this new poll!'
        body = ('Vote in the latest poll. Here is the question'
            'question.question_text'
            'URL/hashed_token')
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,  
            [user.email_address] )
    return HttpResponseRedirect(reverse('poll:index' ) )

# when i am in the context of the request, looking into request.get_host() to dynamically get the name and port,


# http://127.0.0.1:8000/vote?token=W#$RTW#$RWSE$RAW#%$WS#$ER - this is an example of the URL




