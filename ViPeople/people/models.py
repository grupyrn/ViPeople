from django.db import models

class People(models.Model):
    name = models.CharField('Nome', max_length=50)
    phone = models.CharField('Telefone', max_length=50)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __unicode__(self):
        return u"#%s - %s" % (self.pk, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('people_view', [self.pk])

    @models.permalink
    def get_update_url(self):
        return ('people_update', [self.pk])

    @models.permalink
    def get_delete_url(self):
        return ('people_delete', [self.pk])