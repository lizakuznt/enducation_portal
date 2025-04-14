from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, CustomUserViewSet, ProgramViewSet, SectionViewSet, SubsectionViewSet, TaskViewSet, ParticipantViewSet, CertificateViewSet, ApplicationViewSet, EducationalMaterialViewSet, CompletedTaskViewSet 


router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'subsections', SubsectionViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'materials', EducationalMaterialViewSet)
router.register(r'completed_tasks', CompletedTaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
