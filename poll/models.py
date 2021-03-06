from django.db import models
from django.db.models import Count


class Users(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email_address = models.CharField(max_length=50)
    is_admin = models.SmallIntegerField(null=False, default=0)
    is_active = models.SmallIntegerField(null=False, default=1)

    def __unicode__(self):
        return self.email_address
    

class Questions(models.Model):
    QUESTION_TYPE = ( ('multi-choice','multiple choice'), ('essay','free-form essay'), )
    poll_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=250)
    question_type = models.CharField(max_length=25, choices=QUESTION_TYPE)
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def get_poll_results(self, poll_id):
        return Votes.objects.filter(answer_value__question__id = poll_id).values('answer_value') \
        .annotate(vote_count=Count('answer_value'))

    def __unicode__(self):
        return self.question_text

    class Meta:
        permissions=(
            ("can_send_poll_emails","Can send poll emails"
            ),
        )


class Answers(models.Model):
    question = models.ForeignKey(Questions)
    answer_text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.answer_text


class Votes(models.Model):
    answer_value = models.ForeignKey(Answers)
    voter = models.ForeignKey(Users)
    answer_timestamp = models.DateTimeField()

    def __unicode__(self):
        return str(self.answer_value)


class Users_Questions_Hash(models.Model):
    voter = models.ForeignKey(Users)
    question = models.ForeignKey(Questions)
    hash_value = models.CharField(max_length=255)
    is_valid = models.SmallIntegerField(null=False, default=1)
    
    def __unicode__(self):
        return self.voter
