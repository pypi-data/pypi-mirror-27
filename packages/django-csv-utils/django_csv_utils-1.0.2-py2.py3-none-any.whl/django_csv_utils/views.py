import itertools
from datetime import datetime

from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic.base import View

from .utils import write_row


def make_csv_response(stream, filename, datestamp=True):
    """ Send an iterable of csv rows (e.g.: from write_row) through a
        HttpResponse
    """
    response = HttpResponse(
        ''.join(stream), status=200, content_type='text/csv'
    )
    if datestamp:
        full_filename = '{filename} - {date}.csv'.format(
            filename=filename,
            date=datetime.now().strftime('%Y-%m-%d %H:%m')
        )
    else:
        full_filename = '{filename}.csv'.format(filename=filename)

    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(full_filename)
    return response


class StreamingCSVView(View):
    """Class based view for outputting streaming CSV responses"""
    base_filename = "export"
    header = None  # type: List[str]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        contents = (write_row(row) for row in self.get_all(queryset))
        filename = self.get_filename()
        response = StreamingHttpResponse(contents, content_type='text/csv')
        disposition = 'attachment; filename={0}'.format(filename)
        response['Content-Disposition'] = disposition
        return response

    def get_all(self, queryset):
        """Return the entire contents of the CSV file"""
        header = [self.get_header()]
        rows = (self.get_row(item) for item in queryset)
        return itertools.chain(header, rows)

    def get_base_filename(self):
        return self.base_filename

    def get_filename(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        return "{0}_{1}.csv".format(self.get_base_filename(), timestamp)

    def get_row(self, item):
        raise NotImplementedError('Override get_row to output an iterable '
                                  'for an item from the queryset')

    def get_header(self):
        """Get the headers for a CSV"""
        if self.header is None:
            raise NotImplementedError('Override headers or get_headers with a '
                                      'list of headers for this response')
        return self.header
