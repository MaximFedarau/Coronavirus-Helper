from django.db import models

# Create your models here.

class Update(models.Model):
    update_title = models.CharField('Update name',max_length=150)
    update_text = models.TextField('Update text')
    publication_date = models.DateTimeField('Data of update')

    def __str__(self):
        return self.update_title
