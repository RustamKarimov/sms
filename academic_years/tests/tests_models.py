from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings

from academic_years.models import AcademicYear


# Create your tests here.
class AcademicYearModelTest(TestCase):
    def test_clean_method_with_end_date_coming_before_start_date(self):
        start = datetime(2020, 12, 1)
        end = datetime(2020, 11, 1)
        year = 2020

        academic_year = AcademicYear(
            academic_year_id=year, start_of_academic_year=start, end_of_academic_year=end
        )
        self.assertRaises(ValidationError, academic_year.clean)

    def test_save_method_with_wrong_data_calls_clean(self):
        start = datetime(2020, 12, 1)
        end = datetime(2020, 11, 1)
        year = 2020

        academic_year = AcademicYear(
            academic_year_id=year, start_of_academic_year=start, end_of_academic_year=end
        )
        self.assertRaises(ValidationError, academic_year.save)

    def test_different_start_of_year_and_year_raise_exception(self):
        start = datetime(2021, 11, 1)
        end = datetime(2021, 12, 1)
        year = 2020

        academic_year = AcademicYear(
            academic_year_id=year, start_of_academic_year=start, end_of_academic_year=end
        )
        self.assertRaises(ValidationError, academic_year.clean)

    def test_different_end_of_year_and_year_raise_exception(self):
        start = datetime(2021, 11, 1)
        end = datetime(2021, 12, 1)
        year = 2020

        academic_year = AcademicYear(
            academic_year_id=year, start_of_academic_year=start, end_of_academic_year=end
        )
        self.assertRaises(ValidationError, academic_year.clean)

    def test_different_end_of_year_and_year_raise_exception_for_september_start(self):
        settings.ACADEMIC_YEAR_START_TIME = 'September'
        start = datetime(2020, 1, 1)
        end = datetime(2020, 12, 1)
        year = 2020

        academic_year = AcademicYear(
            academic_year_id=year, start_of_academic_year=start, end_of_academic_year=end
        )
        self.assertRaises(ValidationError, academic_year.clean)

    def test_clean_method_passes(self):
        start = datetime(2020, 11, 1)
        end = datetime(2020, 12, 1)
        year = 2020

        academic_year = AcademicYear.objects.create(
            academic_year_id=year, start_of_academic_year=start, end_of_academic_year=end
        )
        self.assertEqual(AcademicYear.objects.count(), 1)

    def test_get_active_year(self):
        settings.ACADEMIC_YEAR_START_TIME = 'January'
        year_1 = AcademicYear.objects.create(
            academic_year_id=2019,
            start_of_academic_year=datetime(2019, 1, 1),
            end_of_academic_year=datetime(2019, 2, 1),
            is_active=False
        )

        year_2 = AcademicYear.objects.create(
            academic_year_id=2020,
            start_of_academic_year=datetime(2020, 1, 1),
            end_of_academic_year=datetime(2020, 2, 1),
            is_active=True
        )

        self.assertEqual(AcademicYear.get_active_year(), year_2)
