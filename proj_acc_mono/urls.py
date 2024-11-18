from django.contrib import admin
from django.urls import path, include

from app_banco.views import test_chart, get_modal

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('<str:empresa>/banco/', include("app_banco.urls")),
    path('', include("app_empresa.urls")),
    path('upload_files/', include("app_upload_files.urls")),
    path('<str:empresa>/contabilidad/', include("app_contabilidad.urls")),
    path('chart/', test_chart, name= 'test-chart'), # TEST CHART
    path('chart/modal/', get_modal, name= 'get-modal'), # TEST MODAL
]