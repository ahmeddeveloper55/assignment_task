from django.contrib.auth.models import AbstractUser
from ..core import _, models as core_models, modelfields as core_modelfields
from . import RoleChoices, modelfields, managers, utils


class User(AbstractUser, core_models.CommonModel, core_models.VerifiedModel, core_models.TrackedModel):
    """
    Users within the Django authentication system are represented by this model.
    """
    first_name = None

    last_name = None

    date_joined = None

    name = modelfields.NameField()

    role = modelfields.RoleField()

    phone_number = modelfields.PhoneNumberField()

    username = modelfields.UsernameField()

    email = modelfields.EmailField()


    objects = managers.BaseUserManager()
    activated_objects = managers.ActivatedUserManager()
    disabled_objects = managers.DisabledUserManager()
    deleted_objects = managers.DeletedUserManager()
    undeleted_objects = managers.UndeletedUserManager()
    verified_objects = managers.VerifiedUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    class Meta:
        ordering = ['-created_at']
        unique_together = [['phone_number', 'role']]
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """
        This method used to return string of object.
        @return: str
        """
        return f'@{self.username}'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.name if self.name else _('unknown')

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.get_full_name().split()[0]

    def get_phone_number(self):
        """
        this function return full phone_number using as_e164 format
        :return:
        """
        return self.phone_number.as_e164

    @property
    def is_login_allowed(self):
        """
        A method used to check if an object is_activate and nor is_deleted.
        """
        return bool(self.is_active and not self.is_deleted)

    @property
    def is_admin(self):
        """
        A method used to check if an object is an admin or not.
        @return: True if role equal 'admin' else False.
        """
        return bool(self.role == RoleChoices.ADMIN and self.is_login_allowed)

    @property
    def is_member(self):
        """
        A method used to check if an object is a member or not.
        @return: True if role equal 'member' else False.
        """
        return bool(self.role == RoleChoices.MEMBER and self.is_login_allowed)

    @property
    def is_client(self):
        """
        A method used to check if an object is a customer or not.
        @return: True if role equal 'admin' else False.
        """
        return bool(self.role == RoleChoices.CLIENT and self.is_login_allowed)

    @property
    def is_editor(self):
        """
        A method used to check if an object is an editor or not.
        @return: True if role equal 'property_editor' else False.
        """
        return bool(self.role == RoleChoices.EDITOR and hasattr(self, 'editoruser') and self.is_login_allowed)

    @property
    def is_developer(self):
        """
        A method used to check if an object is a developer or not.
        @return: True if role equal 'developer' else False.
        """
        return self.phone_number.as_e164 == '+966500000000'

    @property
    def is_request_deletion(self):
        """
        this function used to check if the user request to deletion account
        :return:
        """
        return bool(getattr(self, 'deletion_requests').filter(is_active=True))

    def set_role(self, role):
        """
        A method used to assign a user type to an object
        @param role: user type such as Admin, Supervisor or Investor
        """
        self.role = role

    def block(self):
        """
        block the user
        @return: None
        """
        self.disabled()

    def delete(self):
        """
        This method deletes user data from the database.
        """
        return self.hard_delete()


class Profile(core_models.CommonModel):
    """
    This class represents additional information about the user as it has a one-to-one relationship
    with the user class
    """

    gender = modelfields.GenderField()

    timezone = core_modelfields.TimezoneField()

    user = modelfields.UserOneToOneField()

    class Meta:
        default_permissions = ()
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        """
        This method used to return string of object.
        @return: str
        """
        return f"{self.user.__str__()}"


    def get_age(self):
        """
        This method is used to return the age from birthdate.
        @return: age.
        """
        return utils.get_age(self.birthdate)

    def update(self, **kwargs):
        """
        This function is used to update the instance data, as it will facilitate
        the modification of the instance data without making a new query
        """
        if 'image' in kwargs.keys() and not kwargs['image']:
            kwargs.pop('image')

        return super(Profile, self).update(**kwargs)
