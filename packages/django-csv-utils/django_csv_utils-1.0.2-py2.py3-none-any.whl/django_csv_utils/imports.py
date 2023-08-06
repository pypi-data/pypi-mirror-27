import csv
from datetime import datetime

from django.db import transaction
from django.utils import formats
from django.utils.translation import ugettext_lazy as _

from .exceptions import CSVImportException
from .utils import write_row
from .views import make_csv_response


class Importer:
    """Base importer class"""
    header = None  # type: List[str]
    type_name = 'import'
    default_verbosity = 1

    def __init__(self, handler, verbosity=None, *args, **kwargs):
        super(Importer, self).__init__(*args, **kwargs)
        self.handler = handler
        self.verbosity = verbosity if verbosity is not None else self.default_verbosity
        self.bad_rows = {}
        self.good_rows = {}
        self.rows = []

    def collect_csv(self, filestream):
        """Collect the rows the importer needs from the filestream"""
        if filestream.isatty():
            exit('Please provide a file instead of using stdin')
        reader = csv.DictReader(filestream)
        reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]
        if sorted(reader.fieldnames) != sorted(self.get_header()):
            exit('Please provide a CSV with only the rows {}'.format(','.join(self.get_header())))
        self.rows = [row for row in reader]
        filestream.close()

    def pre_import(self):
        """Things done within the run_import method before the import."""

    def post_import(self):
        """Things done within the run_import method after the import."""

    @transaction.atomic
    def run_import(self, filestream):
        """Create Activity types from CSV"""
        self.pre_import()
        self.collect_csv(filestream)
        for num, row in enumerate(self.rows, start=2):
            try:
                success = self.import_row(row)
            except CSVImportException as ex:
                self.bad_rows[num] = str(ex)
                self.handler.stderr.write('Failure (row {:4d}): {}'.format(num, str(ex)))
            else:
                self.good_rows[num] = success
                if self.verbosity > 1:
                    self.handler.stdout.write('Success (row {:4d}): {}'.format(num, success))
        self.post_import()
        self.print_result()
        if len(self.bad_rows):
            raise CSVImportException(_(
                "Import was not successfully completed. No data was imported."))

    def print_result(self):
        """Show the results. Defaults to success/failure counts"""
        if self.verbosity > 0:
            result = "Result:\n"
            result += "\t{} Successes (rows: {})\n".format(
                len(self.good_rows),
                ', '.join([str(x) for x in sorted(self.good_rows.keys())]))
            result += "\t{} Failures (rows: {})\n".format(
                len(self.bad_rows),
                ', '.join([str(x) for x in sorted(self.bad_rows.keys())]))
            self.handler.stdout.write(result)

    def import_row(self, row):
        raise NotImplementedError('There is no import for this import type')

    def get_header(self):
        """Get the header for a CSV"""
        if self.header is None:
            raise NotImplementedError('There is no header for this import type')
        return self.header

    def make_sample_csv(self):
        return write_row(self.get_header())

    def get_sample_csv(self):
        return make_csv_response(self.make_sample_csv(), 'example_{}'.format(self.type_name))

    @staticmethod
    def get_int_errbad(row, name, errors, error_message=None, default=''):
        """Retrieve an integer, error if a bad value is given"""
        if error_message is None:
            error_message = _('Invalid value in column {}. Requires an integer').format(name)
        val = row.get(name, default).strip()
        if default != '' and val == '':
            val = default
        try:
            return int(val)
        except ValueError:
            errors.append(error_message)
        return val

    @staticmethod
    def get_date_errbad(row, name, errors, error_message=None, default=''):
        """Retrieve a date, error if a bad value is given"""
        if error_message is None:
            error_message = _('Invalid value in column {}. Requires a date').format(name)
        input_formats = formats.get_format_lazy('DATE_INPUT_FORMATS')
        val = row.get(name, default).strip()
        if default != '' and val == '':
            val = default
        success = False
        for input_format in input_formats:
            if not success:
                try:
                    val = datetime.strptime(val, input_format)
                except (ValueError, TypeError):
                    continue
                else:
                    success = True
        if not success:
            errors.append(error_message)
        return val

    @staticmethod
    def get_str_errblank(row, name, errors, error_message=None):
        """Retrieve a string, error if a blank value is given"""
        if error_message is None:
            error_message = _('No value in column {}').format(name)
        val = row.get(name, '').strip()
        if val == '':
            errors.append(error_message)
        return val

    @staticmethod
    def get_str_errbad(row, name, choices, errors, error_message=None, default=''):
        """Retrieve a string, error if a bad value is given"""
        error_message = _('Invalid value in column {}. Must be one of {}').format(name, ', '.join(choices))
        val = row.get(name, default).strip()
        if default != '' and val == '':
            val = default
        success = False
        for choice in choices:
            if not success:
                if choice.lower() == val.lower()[:len(choice)]:
                    val = choice
                    success = True
        if not success:
            errors.append(error_message)
        return val
