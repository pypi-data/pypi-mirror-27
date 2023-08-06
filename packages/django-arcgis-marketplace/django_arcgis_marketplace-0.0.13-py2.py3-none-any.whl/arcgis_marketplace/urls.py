from django.conf.urls import include, url
from django.views.generic import TemplateView

app_name = 'arcgis_marketplace'

urlpatterns = [
    url(r'^$', TemplateView.as_view(
        template_name='arcgis_marketplace/index.html')),

    url(r'^api/', include(
        'arcgis_marketplace.api.urls',
        namespace='api')),
]
