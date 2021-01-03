from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


# Create your models here.
class AcademicYear(models.Model):
    academic_year_id = models.PositiveIntegerField(primary_key=True)
    start_of_academic_year = models.DateField()
    end_of_academic_year = models.DateField()
    is_active = models.BooleanField(default=False)

    objects = models.Manager()

    def clean(self):
        if self.end_of_academic_year <= self.start_of_academic_year:
            raise ValidationError({
                'end_of_academic_year': f"End of an academic year({self.end_of_academic_year}) "
                                        f"cannot come before its start({self.start_of_academic_year})"
            })

        if self.start_of_academic_year.year != self.academic_year_id:
            raise ValidationError({
                'start_of_academic_year': f"Start of the academic year {self.start_of_academic_year.year} and"
                                          f"academic year {self.academic_year_id} not matching each other"
            })

        if self.end_of_academic_year.year != self.academic_year_id and \
                settings.ACADEMIC_YEAR_START_TIME == 'January':
            raise ValidationError({
                'end_of_academic_year': f"Start of the academic year {self.end_of_academic_year.year} and"
                                        f"academic year {self.academic_year_id} not matching each other"
            })

        if self.end_of_academic_year.year != self.academic_year_id + 1 and \
                settings.ACADEMIC_YEAR_START_TIME != 'January':
            raise ValidationError({
                'end_of_academic_year': f"Start of the academic year {self.end_of_academic_year.year} and"
                                        f"academic year {self.academic_year_id} not matching each other"
            })

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(AcademicYear, self).save(force_insert=force_insert,
                                       force_update=force_update,
                                       using=using,
                                       update_fields=update_fields)

    @staticmethod
    def get_active_year():
        return AcademicYear.objects.filter(is_active=True).first()
