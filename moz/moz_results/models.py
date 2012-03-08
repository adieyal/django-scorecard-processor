from django.db import models
from scorecard_processor.models import Entity
import plugins, reports

# Create your models here.
def attachment_storage(instance, filename):
    return 'entity_attachments/%s/%s' % (instance.entity.pk, filename)

class Attachment(models.Model):
    #Possibly store metadata about the files/attachment?
    entity = models.ForeignKey(Entity)
    file = models.FileField(upload_to=attachment_storage, help_text="Upload a new file")

    def __unicode__(self):
        return u'%s on %s' % (self.file, self.entity)

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    @property
    def extension(self):
        return self.filename.split('.')[-1]

