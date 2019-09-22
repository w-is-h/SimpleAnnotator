from django.shortcuts import render
from .models import *
from .utils import get_doc
import icd10
from medcat.cdb import CDB
cdb = CDB()
#cdb.load_dict("/home/ubuntu/data/umls/models/trained/cdb-umls-lr-1-cs-9-np-0.5-2m-n.dat")


def index(requet):
    # list projects
    pass

# Create your views here.
def annotate(request, from_save=False):
    data = request.GET
    sid = None
    if 'sid' in data:
        sid = data['sid']
    context = {}

    if from_save and sid:
        if DocumentSet.objects.get(id=sid).done:
            sid = None

    # Tasks
    context['tasks'] = MetaTask.objects.all().order_by('name')
    project = None
    document = None

    if 'pid' in data:
        pid = data['pid']
        project = Project.objects.get(id=pid)
        document = None
        context['document_sets'] = DocumentSet.objects.filter(project=project).order_by('name')
        context['pid'] = pid
    else:
        # Get first project for this user
        pid = Project.objects.filter(members=request.user)[0].id
        project = Project.objects.get(id=pid)
        document = None
        context['document_sets'] = DocumentSet.objects.filter(project=project).order_by('name')
        context['pid'] = pid


    if 'did' in data:
        did = int(data['did'])
        document = Document.objects.get(id=did)
        if document.done:
            anns = MetaAnnotation.objects.filter(document=document)
            context['tasks'][0].real_val = False
            for task in context['tasks']:
                ann = MetaAnnotation.objects.filter(document=document, meta_task=task)
                if ann:
                    ann = ann[0]
                    task.cid = ann.meta_task_value.id
    elif project is not None:
        if sid is not None:
            # Get all ds
            document = get_doc(project, sid=sid)
        else:
            # Get all ds
            document = get_doc(project)

    if document is not None:
        context['documents'] = Document.objects.filter(document_set=document.document_set).order_by('document_id')
        context['active_doc'] = document
    else:
        if sid is not None:
            ds = DocumentSet.objects.get(id=sid)
            document = Document.objects.filter(document_set=ds).order_by('document_id')

            context['documents'] = Document.objects.filter(document_set=document.document_set).order_by('document_id')
            context['active_doc'] = document
        else:
            ds = DocumentSet.objects.filter(project=project).order_by('name')[0]
            document = Document.objects.filter(document_set=ds).order_by('document_id')[0]

            context['documents'] = Document.objects.filter(document_set=document.document_set).order_by('document_id')
            context['active_doc'] = document

    text = context['active_doc'].text

    if context['active_doc'].string_orig.lower() in text.lower():
        start = text.lower().index(context['active_doc'].string_orig.lower())
        end = start + len(context['active_doc'].string_orig)
    else:
        start = 0
        end = 0

    s_start = max(0, start-1000)
    s_end = min(len(text), end + 1000)
    print(s_start)

    text = text[s_start:start] + "<span class='ann'>" + text[start:end] + "</span>" + text[end:s_end]
    text = text.replace("\n", "<br />")
    context['text'] = text

    # Info from MedCAT and some dict
    context['pretty_name'] = None
    if context['active_doc'].cui.upper() in cdb.cui2pretty_name:
        context['pretty_name'] = cdb.cui2pretty_name[context['active_doc'].cui.upper()]

    try:
        context['icd'] = icd10.find(context['active_doc'].document_set.name.upper()).description
    except:
        context['icd'] = "None"

    return render(request, 'annotate.html', context)

def save(request):
    print(request.POST)
    data = request.POST
    try:
        did = data['did']
        doc = Document.objects.get(id=did)

        # Remove if annotation already exists
        MetaAnnotation.objects.filter(document=doc).delete()

        for key in data.keys():
            if str(key).isnumeric():
                task = MetaTask.objects.get(id=int(key))
                value = MetaTaskValue.objects.get(id=int(data[key]))

                ma = MetaAnnotation()
                ma.document = doc
                ma.meta_task = task
                ma.meta_task_value = value
                ma.save()
        doc.done = True
        doc.save()

        # Save done if needed
        ds = doc.document_set
        docs = Document.objects.filter(done=False, document_set=ds)
        if len(docs) == 0:
            ds.done = True
            ds.save()
    except Exception as e:
        print(e)
    return annotate(request, from_save=True)
