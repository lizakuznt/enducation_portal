from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Роль (CRUD)
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# Пользователь (CRUD)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Программа (CRUD)
class ProgramViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции для таблицы Program (Программа)
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    # Дополнительный API-метод для поиска активных программ
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_programs = Program.objects.filter(status="Активен")
        serializer = ProgramSerializer(active_programs, many=True)
        return Response(serializer.data)

# Раздел (CRUD)
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

# Подраздел (CRUD)
class SubsectionViewSet(viewsets.ModelViewSet):
    queryset = Subsection.objects.all()
    serializer_class = SubsectionSerializer

# Программа Прогресс (CRUD)
class ProgramProgressViewSet(viewsets.ModelViewSet):
    queryset = ProgramProgress.objects.all()
    serializer_class = ProgramProgressSerializer

# Учебный Материал (CRUD)
class EducationalMaterialViewSet(viewsets.ModelViewSet):
    queryset = EducationalMaterial.objects.all()
    serializer_class = EducationalMaterialSerializer

# Задание (CRUD)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Выполненное Задание (CRUD)
class CompletedTaskViewSet(viewsets.ModelViewSet):
    queryset = CompletedTask.objects.all()
    serializer_class = CompletedTaskSerializer

# Участник (CRUD)
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

# Сертификат (CRUD)
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

# Заявка на обучение (CRUD)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
