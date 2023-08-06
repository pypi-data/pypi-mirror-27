import argparse

from django.core.management.base import BaseCommand

from .imports import Importer  # NOQA


class ImportCommand(BaseCommand):
    """Import data from CSVs"""
    imports = None  # type: Dict[str, Importer]

    def __init__(self, *args, **kwargs):
        """Provide the 'help' argument Django expects"""
        self.help = self.__doc__
        super(ImportCommand, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        """Conditionally add the csv_type name arg, and add the filename arg"""
        imports = self.get_imports()
        parser.add_argument('csv_type', nargs=1, type=str, choices=imports.keys())
        parser.add_argument('filename', nargs=1, type=argparse.FileType('r'))

    def get_imports(self):
        """Get the list of supported importers"""
        if self.imports is None:
            raise NotImplementedError('Please provide a list of imports')
        return self.imports

    def get_importer(self, name, verbosity):
        """Determine which importer to use"""
        if name is None:  # expect a class, return instantiated
            return self.get_imports()(handler=self, verbosity=verbosity)  # pylint: disable=not-callable
        return self.get_imports()[name](handler=self, verbosity=verbosity)

    def handle(self, *args, **kwargs):
        """Pull in the contents of the CSV, send to the correct method"""
        verbosity = int(kwargs.get('verbosity', 1))
        name = kwargs.get('csv_type', [None])[0]
        importer = self.get_importer(name, verbosity)
        filestream = kwargs['filename'][0]
        importer.run_import(filestream)
