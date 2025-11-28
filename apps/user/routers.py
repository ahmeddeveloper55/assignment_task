from rest_framework.routers import DefaultRouter, Route, DynamicRoute


class ProfileRouter(DefaultRouter):
    """
    The default router extends the SimpleRouter, but also adds in a default
    API root view, and adds format suffix patterns to the URLs.
    """

    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'put': 'update',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
    ]
