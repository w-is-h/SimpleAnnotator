from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import fill_db


STATUS_CHOICES = [
        (0, 'Not Validated'),
        (1, 'Validated'),
        ]

BOOL_CHOICES = [
        (0, 'False'),
        (1, 'True')
        ]


class Concept(models.Model):
    pretty_name = models.CharField(max_length=300)
    cui = models.CharField(max_length=100, unique=True)
    desc = models.TextField(default="", blank=True)
    tui = models.CharField(max_length=20)
    semantic_type = models.CharField(max_length=200, blank=True, null=True)
    vocab = models.CharField(max_length=100)
    synonyms = models.TextField(default='', blank=True)


    def __str__(self):
        return str(self.pretty_name)



class Document(models.Model):
    name = models.CharField(max_length=150)
    create_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default="", blank=True)
    start_ind = models.IntegerField()
    end_ind = models.IntegerField()
    string_orig = models.TextField(default="", blank=True)
    cui = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    document_id = models.CharField(max_length=1000)
    document_set = models.ForeignKey('DocumentSet', on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='doc2set')


    def __str__(self):
        return str(self.name)


class DocumentSet(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='project_doc_set')
    done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(default="", blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    add_data_from = models.FileField()

    def __str__(self):
        return str(self.name)


class MetaTaskValue(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)


class MetaTask(models.Model):
    name = models.CharField(max_length=150)
    values = models.ManyToManyField(MetaTaskValue, related_name='values')
    description = models.TextField(default="", blank=True)


class MetaAnnotation(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    meta_task = models.ForeignKey('MetaTask', on_delete=models.CASCADE)
    meta_task_value = models.ForeignKey('MetaTaskValue', on_delete=models.CASCADE)


# Extract text from the uploaded dataset
@receiver(post_save, sender=Project)
def save_dataset(sender, instance, **kwargs):
    fill_db(instance)
