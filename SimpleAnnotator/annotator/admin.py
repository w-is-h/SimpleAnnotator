from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Concept)
admin.site.register(Document)
admin.site.register(DocumentSet)
admin.site.register(Project)
admin.site.register(MetaTaskValue)
admin.site.register(MetaTask)
admin.site.register(MetaAnnotation)
