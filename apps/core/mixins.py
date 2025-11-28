import pandas as pd
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from tablib import Dataset

from . import statistics, serializers
from .utils.translation import _


class CachedViewSetMixin(object):
    """
    This mixin provides caching functionality for the list and retrieve views of a ViewSet.
    The cache timeout is set to 15 minutes by default.
    """
    cache_timeout = 60 * 15  # Default cache timeout of 15 minutes

    @method_decorator(cache_page(cache_timeout))
    def list(self, request, *args, **kwargs):
        """
        Cache the list view of the ViewSet for the duration specified in cache_timeout.
        This method handles HTTP GET requests for listing objects.
        """
        return getattr(super(), 'list')(request, *args, **kwargs)

    @method_decorator(cache_page(cache_timeout))
    def retrieve(self, request, *args, **kwargs):
        """
        Cache the retrieve view of the ViewSet for the duration specified in cache_timeout.
        This method handles HTTP GET requests for retrieving a single object.
        """
        return getattr(super(), 'retrieve')(request, *args, **kwargs)


class ActivateModelMixin(object):
    """
    This class contains two methods for activating and deactivating the object.
    This class can be inherited with ViewSet class.
    """

    @property
    def user(self):
        """
        This function is used to return the current user from request.
        @return user.
        """
        request = getattr(self, 'request', None)

        if request is None:
            return

        return getattr(request, 'user', None)

    @action(methods=['POST'], detail=True)
    def active(self, request, *args, **kwargs):
        """
        This method can access a specified object by specifying the detail attribute with the value True,
        and then modify the state of this object to the active state.
        """
        get_object = getattr(self, 'get_object')
        instance = get_object()

        if self.user != instance:
            instance.active()

        return Response({'details': _('The object has been activated successfully')})

    @action(methods=['POST'], detail=True)
    def disable(self, request, *args, **kwargs):
        """
        This method can access a specified object by specifying the detail attribute with the value True,
        and then modify the state of this object to the inactive state.
        """
        get_object = getattr(self, 'get_object')
        instance = get_object()

        if self.user != instance:
            instance.disable()

        return Response({'details': _('The object has been deactivated successfully')})


class StatisticModeMixin(object):
    """
    This class is used to facilitate the process of dealing with statistics by
    providing an interface that contains some basic things.
    """

    def get_choices_data(self, queryset, choices, label_name='label'):
        """
        This method is used to het tje choice value display from queryset and return data
        """

        if not isinstance(choices, dict):
            choices = dict(choices)

        for item in queryset:
            item.update({label_name: choices.get(item[label_name])})

        return queryset

    def get_context(self, *args, **kwargs):
        """
        This method is used to return data in the form of a dictionary.
        """
        context = dict()
        return context

    def get_data(self, queryset, lookup, prefix):
        """
        This method is used to return data in the form of a dictionary.
        """
        stats = statistics.Stats(queryset, None, lookup)
        return stats.get_statistics_data(prefix=prefix)

    def get_response(self, queryset, lookup, prefix):
        """
        This method is used to return data in the form of a Response object
        """
        data = self.get_data(queryset, lookup, prefix)
        return Response(data=data)

    @action(methods=['get'], detail=False, url_name='numeric-stats', url_path='numeric-stats')
    def numeric_stats(self, request, *args, **kwargs):
        """
        This method is used to return numeric data
        """
        return Response(data=self.get_context())


class ExportMixin:
    """
    This mixin provides an export functionality for data in various formats like CSV, JSON, and Excel.
    It requires a ModelResource class to be defined or passed, which handles the export logic.
    """
    resource_class = None  # You can set this to your ModelResource class, or pass it dynamically

    def get_resource_class(self):
        """
        This method returns the resource class that will be used for exporting.
        You can override it or set the resource_class attribute.
        """
        if self.resource_class is None:
            raise ValueError("You must define 'resource_class' or override 'get_resource_class' method.")
        return self.resource_class

    def export_data(self, queryset, export_format):
        """
        Export data from a queryset in the requested format.
        Supported formats: CSV, JSON, XLSX (Excel) file.
        """
        resource = self.get_resource_class()()
        dataset = resource.export(queryset=queryset)

        # Mapping export formats to their corresponding attributes and content types
        export_formats = {
            'csv': {
                'content': dataset.csv,
                'content_type': 'text/csv',
                'extension': 'csv'
            },
            'xlsx': {
                'content': dataset.xlsx,
                'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'extension': 'xlsx'
            }
        }

        if export_format not in export_formats:
            return Response({"detail": f"Unsupported export format: '{export_format}'. Allowed formats: csv, xlsx."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the corresponding export details
        export_info = export_formats[export_format]
        content = export_info['content']
        content_type = export_info['content_type']
        file_extension = export_info['extension']

        # Create HTTP response
        response = HttpResponse(content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="exported_data.{file_extension}"'
        return response

    @action(methods=['get'], detail=False, url_name='export')
    def export(self, request, *args, **kwargs):
        """
        This method handles the request to export data.
        The format can be passed via query parameters (e.g., ?format=csv).
        """
        export_format = request.query_params.get('file_type', 'xlsx')  # Default to CSV if not specified
        queryset = getattr(self, 'get_queryset')()
        filter_queryset = (getattr(self, 'filter_queryset')(queryset))
        return self.export_data(filter_queryset, export_format)


class ImportMixin:
    """
    This mixin provides both importer and export functionality for data in various formats like CSV, JSON, and Excel.
    It requires a ModelResource class to be defined or passed, which handles both the importer and export logic.
    """
    resource_class = None  # You can set this to your ModelResource class, or pass it dynamically

    def get_resource_class(self):
        """
        This method retrieves the resource_class.
        If the resource_class is not set, an exception is raised.
        """
        if self.resource_class is None:
            raise ValueError("You must define 'resource_class' or override 'get_resource_class' method.")
        return self.resource_class

    def import_data(self, file, import_format,user=None):
        """
        This method handles the importer logic.
        It accepts a file and the importer format (e.g., CSV or XLSX).
        """
        resource = self.get_resource_class()()

        # Define the available importer formats. Here, only CSV and XLSX are supported.
        import_formats = {'csv': pd.read_csv, 'xlsx': pd.read_excel}

        # Check if the requested format is supported, otherwise raise an error.
        if import_format not in import_formats:
            raise ValueError(f"Unsupported importer format requested: {import_format}")

        # Get the corresponding importer format instance (either CSV or XLSX).
        df = import_formats[import_format](file)
        df = df.fillna(0)

        # Load the pandas dataframe into a tablib dataset
        dataset = Dataset().load(df)

        try:
            # Import the dataset and run the importer process.
            # 'dry_run' is set too False to actually perform the importer.
            result = resource.import_data(dataset, dry_run=False, raise_errors=True, user=user)

            # If the importer is successful and no errors are present, return a success response.
            if not result.has_errors():
                return Response({'detail': 'Import successful!'}, status=status.HTTP_200_OK)

            # If there are errors in the importer process, return the errors in the response.
            return Response({'detail': 'Import failed!', 'errors': result.row_errors[0]},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch any exceptions during the importer process and return a failure response with the error message.
            return Response({'detail': f'Import failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_name='importer', url_path='importer')
    def import_view(self, request, *args, **kwargs):
        """
        This method is a Django REST Framework action for handling file imports via a POST request.
        """
        serializer = serializers.ImportSerializer(data=request.data)

        # If the serializer is valid, proceed with the importer process.
        if serializer.is_valid():
            # Retrieve the uploaded file and the requested importer format (default is 'xlsx').
            import_file = serializer.validated_data.get('import_file')
            import_format = serializer.validated_data.get('format', 'xlsx')

            # If no file is provided, return an error response.
            if not import_file:
                return Response({'detail': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

            # Call the import_data method to handle the importer process.
            return self.import_data(import_file, import_format,user=request.user)

        # If the serializer validation fails, return the errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
