from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog


urlpatterns = i18n_patterns(
    path('user/', include(('apps.user.urls', 'apps.user'), namespace='user')),
    path('supervisor/', include(('apps.supervisor.urls', 'apps.supervisor'), namespace='supervisor')),
    path('editor/', include(('apps.editor.urls', 'apps.editor'), namespace='editor')),
    path("search/", include("apps.search.urls", namespace="search")),
    path('auth/', include(('apps.auth.urls', 'apps.auth'), namespace='auth')),
    path('tag/', include(('apps.tag.urls', 'apps.tag'), namespace='tag')),
    path('client/', include(('apps.client.urls', 'apps.client'), namespace='client')),
    path('category/',include(('apps.category.urls','apps.category'),namespace='category')),
    path('program/', include(('apps.program.urls', 'apps.program'), namespace='program')),
    path('episode/', include(('apps.episode.urls', 'apps.episode'), namespace='episode')),
    path('importer/', include(('apps.importer.urls', 'apps.importer'), namespace='importer')),

)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
)


