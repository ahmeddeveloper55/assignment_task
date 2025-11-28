# If you'd like to re-use custom conditions across policies,
# you can define them globally in a module and point to it via the setttings.
# You can also provide a List of paths to check multiple files.


def anonymous(request, view, action):
    user = request.user

    return bool(user.is_anonymous)


def login_allowed(request, view, action):
    user = request.user
    return bool(user.is_authenticated and user.is_login_allowed)


def admin(request, view, action):
    user = request.user
    return bool(user.is_authenticated and user.is_admin)


def client(request, view, action):
    user = request.user
    return bool(user.is_authenticated and user.is_client)


def owner(request, view, action):
    user = request.user
    return bool(user.is_authenticated and user.is_editor)



