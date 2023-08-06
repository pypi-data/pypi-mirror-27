django-csv-utils - Tools for working with CSV data in Django
============================================================

Contains helpers for CSV interaction.

There are two primary uses:

* Running an import command with a list of importers
* Exporting a streaming CSV response export

Example import:
---------------

.. code:: python

    from django_csv_utils import CSVImportException, ImportCommand, Importer
    from users.models import User


    class UserImporter(Importer):
        """Imports User objects from a CSV."""
        header = [
            "first_name",
            "last_name",
            "email",
        ]

        def import_row(self, row):
            errors = []
            first_name = row.get("first_name", "")
            last_name = row.get("last_name", "")
            email = self.get_str_errblank(row, "email", errors).lower()
            if User.objects.filter(email=email).exists():
                errors.append("The email {} is already in use".format(email))
            if errors:
                raise CSVImportException(', '.join([str(e) for e in errors]))
            new_user = User.objects.create(
                email=email, first_name=first_name, last_name=last_name)
            return "Imported {0}".format(new_user.get_full_name())


    class Command(ImportCommand):
        imports = {'users': UserImporter}


Example StreamingHTTPResponse:
------------------------------

.. code:: python

    from django_csv_utils import StreamingCSVView
    from users.models import User


    class UserCSVView(StreamingCSVView):
        """Give the list of users."""
        header = [
            'fist_name',
            'last_name',
            'email',
        ]

        def get_queryset(self):
            """Return the right list of users."""
            return User.objects.filter(is_active=True, is_superuser=False)

        def get_row(self, item):
            return (
                item.first_name,
                item.last_name,
                item.email,
            )
