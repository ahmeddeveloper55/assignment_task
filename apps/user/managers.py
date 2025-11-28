from django.contrib.auth.base_user import BaseUserManager as DjangoBaseUserManager
from ..core import managers as core_managers

from . import utils, RoleChoices


class UserQueryset(core_managers.BaseQuerySet):
    def find_by_role(self, role, **filters):
        """
        This method is used for the filter of users based on the type of user
        passed from the variable with the name role
        @param role:The name of the role that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        return self.filter(role=role, **filters)

    def find_by_username(self, username, **filters):
        """
        This method is used for the filter of users based on the username
        passed from the variable with the name username
        @param username:The name of the username that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        return self.filter(username=username, **filters)

    def find_by_email(self, email, **filters):
        """
        This method is used for the filter of users based on the email
        passed from the variable with the name email
        @param email:The name of the email that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        return self.filter(email=email, **filters)

    def find_by_phone_number(self, phone_number, **filters):
        """
        This method is used for the filter of users based on the phone_number
        passed from the variable with the name phone_number
        @param phone_number:The name of the phone_number that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        return self.filter(phone_number=phone_number, **filters)

    def admins(self, **filters):
        """
        This method returns users with administrator role
        @return: QuerySet
        """
        return self.find_by_role(RoleChoices.ADMIN, **filters)

    def clients(self, **filters):
        """
        This method returns users with client role
        @return: QuerySet
        """
        return self.find_by_role(RoleChoices.CLIENT, **filters)

    def editors(self, **filters):
        """
        This method returns users with editors role
        @return: QuerySet
        """
        return self.find_by_role(RoleChoices.EDITOR, **filters)

    


class BaseUserManager(DjangoBaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lower casing the domain part of it.
        """
        if not email:
            return None

        return super(BaseUserManager, cls).normalize_email(email).lower()

    def create_user(self, phone_number, role, username=None, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        @:param phone_number: is the phone number for user
        @:param role: is the user type  for user
        @:param username: is the username for user
        @:param email: is the email for user
        @:param password: is the password for user
        @:param extra_fields: this is the extra attributes like first name,
        last name and others
        @:returns new user
        """
        username = username or utils.generate_username()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.set_role(role)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, **extra_fields):
        """
        Creates and saves an admin with the given phone_number and extra_fields.
        @:param phone_number: is the phone number for user
        @:param extra_fields: this is the extra attributes like email, username, password, first name,
        last name, and others.
        @:returns new user
        """
        extra_fields.update({'role': RoleChoices.ADMIN})
        user = self.create_user(phone_number, **extra_fields)
        return user

    def create_client(self, phone_number, **extra_fields):
        """
        Creates and saves a customer with the given phone_number and extra_fields.
        @:param phone_number: is the phone number for user
        @:param extra_fields: this is the extra attributes like email, username, password, first name,
        last name, and others.
        @:returns new user
        """
        extra_fields.update({'role': RoleChoices.CLIENT})
        user = self.create_user(phone_number, **extra_fields)
        return user

    def create_editor(self, phone_number, **extra_fields):
        """
        Creates and saves an owner with the given phone_number and extra_fields.
        @:param phone_number: is the phone number for user
        @:param extra_fields: this is the extra attributes like email, username, password, first name,
        last name, and others.
        @:returns new user
        """
        extra_fields.update({'role': RoleChoices.EDITOR})
        user = self.create_user(phone_number, **extra_fields)
        return user



    def find_by_role(self, role, **filters):
        """
        This method is used for the filter of users based on the type of user
        passed from the variable with the name role
        @param role:The name of the role that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        filters.update({'role': role})
        return self.get_queryset().find_by_role(**filters)

    def find_by_username(self, username, **filters):
        """
        This method is used for the filter of users based on the username
        passed from the variable with the name username
        @param username:The name of the username that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        filters.update({'username': username})
        return self.get_queryset().find_by_username(**filters)

    def find_by_email(self, email, **filters):
        """
        This method is used for the filter of users based on the email
        passed from the variable with the name email
        @param email:The name of the email that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        filters.update({'email': email})
        return self.get_queryset().find_by_email(**filters)

    def find_by_phone_number(self, phone_number, **filters):
        """
        This method is used for the filter of users based on the phone_number
        passed from the variable with the name phone_number
        @param phone_number:The name of the phone_number that the user holds
        @param filters: Dictionary of different fields
        @return: QuerySet
        """
        filters.update({'phone_number': phone_number})
        return self.get_queryset().find_by_phone_number(**filters)

    def admins(self, **filters):
        """
        This method returns users with administrator role
        @return: QuerySet
        """
        return self.get_queryset().admins(**filters)

    def clients(self, **filters):
        """
        This method returns users with customer role
        @return: QuerySet
        """
        return self.get_queryset().clients(**filters)

    def editors(self, **filters):
        """
        This method returns users with owner role
        @return: QuerySet
        """
        return self.get_queryset().editors(**filters)



class ActivatedUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db).filter(is_active=True)


class DisabledUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db).filter(is_active=False)


class DeletedUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db).filter(is_deleted=True)


class UndeletedUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db).filter(is_deleted=False)


class VerifiedUserManager(BaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db).filter(is_active=True, is_deleted=False)
