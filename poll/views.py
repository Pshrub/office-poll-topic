from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
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

# the entire site will be SSL (certificate). for internal testing use a self-signed cert.
# the details page is where the URL in the email will send people. There should be code here 
# (see top sentence of comment) to validate the token and tell who is the person who clicked 
# the link. from that you also know the question. then. after they vote, i can register the results
# in the table and display the results.

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


def sendEmail(request, poll_id): 
    users = Users.objects.filter(is_active=1) 
    question = get_object_or_404(Questions, pk=poll_id)
    urlbase = request.get_host()
    for user in users:        
        salt = str(random.randint(1,10000))
        token = u'%s:%s:%s' % (user.email_address, question.question_text, salt)
        hashed_token = hashlib.sha1(token).hexdigest()
        token_link = str(urlbase) + '/vote?token=' + str(hashed_token)
        Users_Questions_Hash.objects.create(voter=user, question=question, hash_value=hashed_token, is_valid=1)
    
        subject, from_email, to = 'Vote in the latest poll!', settings.DEFAULT_FROM_EMAIL, [user.email_address]
        c = Context({'firstname': user.first_name,
            'questiontext': question.question_text,
            'tokenlink': token_link})    
        text_content = render_to_string('mail/email.txt', c)
        html_content = render_to_string('mail/email.html', c)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
    messages.add_message(request, messages.INFO, 'Emails sent successfully')

    return HttpResponseRedirect(reverse('poll:index' ) )

# http://127.0.0.1:8000/vote?token=W#$RTW#$RWSE$RAW#%$WS#$ER - this is an example of the URL




