from django.contrib import admin
from .models import *
import pandas
from io import StringIO
from django.http import HttpResponse, HttpResponseRedirect
import icd10

# Register your models here.
admin.site.register(Concept)
admin.site.register(DocumentSet)
admin.site.register(MetaTaskValue)
admin.site.register(MetaTask)
admin.site.register(MetaAnnotation)

def download(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied

    arr = []
    tasks = MetaTask.objects.all()
    head = ['doc_id', 'string_orig', 'cui', 'icd10', 'done', 'db_id', 'icd10-ch', 'comment']
    for task in tasks:
        head.append(task.name)

    arr.append(head)
    dss = DocumentSet.objects.filter(project=queryset[0])
    for ds in dss:
        docs = Document.objects.filter(document_set=ds)
        for doc in docs:
            try:
                comment = Comment.objects.get(document=doc).text
            except:
                comment = ""
            row = [""] * len(head)
            row[0] = doc.document_id
            row[1] = doc.string_orig
            row[2] = doc.cui
            row[3] = ds.name
            row[4] = doc.done
            row[5] = doc.id
            row[6] = icd10.find(ds.name.upper()).chapter
            row[7] = comment
            anns = MetaAnnotation.objects.filter(document=doc)
            for ann in anns:
                row[head.index(ann.meta_task.name)] = ann.meta_task_value.name
            arr.append(row)

    sio = StringIO()
    df = pandas.DataFrame(arr[1:], columns=arr[0])
    df.to_csv(sio)
    sio.seek(0)

    response = HttpResponse(sio, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
    return response

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    actions = [download]
admin.site.register(Project, ProjectAdmin)


def remove_all_documents(modeladmin, request, queryset):
    Document.objects.all().delete()

class DocumentAdmin(admin.ModelAdmin):
    model = Document
    actions = [remove_all_documents]
