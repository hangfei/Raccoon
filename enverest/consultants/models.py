from django.db import models
from django.db.models import Q
from django.utils import timezone
import operator

class ExpertManager(models.Manager):
    def search(self, search_terms):
        terms = [term.strip() for term in search_terms.split()]
        q_objects = []

        for term in terms:
            q_objects.append(Q(description_text__icontains=term))
        qs = self.get_queryset()
        return qs.filter(reduce(operator.or_, q_objects))

class Client(models.Model):
    first_name_text = models.CharField("First Name", max_length=30)
    last_name_text = models.CharField("Last Name", max_length=30)
    password = models.CharField("Password", max_length=30, default = '12345')
    def __str__(self):
        return self.first_name_text + " " + self.last_name_text

class Expert(models.Model):
    APPLYING = 'A'
    JUNIOR = 'J'
    SENIOR = 'S'

    EXPERT_STATUS_CHOICES = (
       (APPLYING, 'Expert is applying'),
       (JUNIOR, 'Expert'),
       (SENIOR, 'Senior Expert'),
    )

    first_name_text = models.CharField("First Name", max_length=30)
    last_name_text = models.CharField("Last Name", max_length=30)
    password = models.CharField("Password", max_length=30, default = '12345')
    description_text = models.CharField("Description", max_length=500)
    status = models.CharField(max_length=1,
                              choices=EXPERT_STATUS_CHOICES,
                              default=APPLYING)
    def __str__(self):
        return self.first_name_text + " " + self.last_name_text

class Project(models.Model):
    PROJECT_CREATED = 'PC'
    PROJECT_SUBMITTED = 'PS'
    EXPERT_ASSIGNED = 'EA'
    IN_PROGRESS = 'IP'
    PROJECT_FINISHED = 'PF'
    PAYMENT_RECEIVED = 'PR'

    PROJECT_STATUS_CHOICES = (
       (PROJECT_CREATED, 'Project is created'),
       (PROJECT_SUBMITTED, 'Project is submitted'),
       (EXPERT_ASSIGNED, 'An expert is assigned'),
       (IN_PROGRESS,'An expert is working on it'),
       (PROJECT_FINISHED,'Project is finished'),
       (PAYMENT_RECEIVED,'Payment is received and the project is closed'),
    )

    CLIENT = 'CLT'
    EXPERT = 'EPT'
    ADMINISTRATOR = 'ADM'

    ASSIGN_TO_CHOICES = (
       (CLIENT, 'Waiting for client'),
       (EXPERT, 'Waiting for expert'),
       (ADMINISTRATOR, 'Waiting for system administrator'),
    )

    client = models.ForeignKey(Client)
    expert = models.ForeignKey(Expert)
    title_text = models.CharField(max_length=200)
    info_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date end')
    state = models.CharField(max_length=2,
                             choices=PROJECT_STATUS_CHOICES,
                             default=PROJECT_CREATED)
    assgin_to = models.CharField(max_length=3,
                                 choices=ASSIGN_TO_CHOICES,
                                 default=CLIENT)

    def __str__(self):
        return self.title_text
# Create your models here.

