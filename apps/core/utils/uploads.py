import shortuuid
from django.utils import timezone


def path(parent_folder, instance, filename):
    """
    This function returns the path in which the files are stored,
    whether this file is an image or any other type.
    """

    filename = f"{shortuuid.uuid()}.{filename.split('.')[-1]}"
    date = timezone.now()
    return f'{parent_folder}/{date.year}/{date.month}/{date.day}/{filename}'


def image_folder(instance, filename):
    """
    This function returns the path where the images will be stored.
    """

    return path('images', instance, filename)


def file_folder(instance, filename):
    """
    This function returns the path where the file will be stored.
    """

    return path('files', instance, filename)
