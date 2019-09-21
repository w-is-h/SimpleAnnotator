import json

def fill_db(project):
    from .models import DocumentSet, Document
    data = json.load(open(project.add_data_from.path))

    for key in data.keys():
        # Try to get exisiting ds
        dss = DocumentSet.objects.filter(project=project, name=str(key))
        if len(dss) > 0:
            ds = dss[0]
            ds.done = False
        else:
            ds = DocumentSet()
            ds.name = str(key)
            ds.project = project
            ds.save()

        for s_doc in data[key]:
            try:
                doc = Document()
                doc.name = s_doc.get('doc_table', "NO_NAME")
                doc.text = s_doc['content']
                doc.start_ind = int(s_doc['annotations'][0]['start'])
                doc.end_ind = int(s_doc['annotations'][0]['end'])
                doc.string_orig = s_doc['annotations'][0]['string_orig']
                doc.cui = s_doc['annotations'][0]['concept']
                doc.document_id = s_doc['id']
                doc.document_set = ds
                doc.save()
            except Exception as e:
                print("*"*100)
                print(str(e))


def get_doc(project, sid=None):
    from .models import DocumentSet, Document

    if sid is None:
        dss = DocumentSet.objects.filter(project=project, done=False).order_by('name')
        if len(dss) > 0:
            ds = dss[0]
            documents = Document.objects.filter(done=False, document_set=ds).order_by('document_id')
            if len(documents) > 0:
                document = documents[0]
                return document
    else:
        ds = DocumentSet.objects.get(id=sid)
        documents = Document.objects.filter(done=False, document_set=ds).order_by('document_id')
        if len(documents) > 0:
            document = documents[0]
            return document
        else:
            ds = DocumentSet.objects.get(id=sid)
            document = Document.objects.filter(document_set=ds).order_by('document_id')[0]
            return document

    return None
