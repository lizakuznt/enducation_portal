from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Роль (CRUD)
class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# Пользователь (CRUD)
class UserViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

# Программа (CRUD)
class ProgramViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции для таблицы Program (Программа)
    """
    
    permission_classes = [IsAuthenticated]

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
    
    permission_classes = [IsAuthenticated]

    queryset = Section.objects.all()
    serializer_class = SectionSerializer

# Подраздел (CRUD)
class SubsectionViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    queryset = Subsection.objects.all()
    serializer_class = SubsectionSerializer

# Программа Прогресс (CRUD)
class ProgramProgressViewSet(viewsets.ModelViewSet):
    queryset = ProgramProgress.objects.all()
    serializer_class = ProgramProgressSerializer

# Учебный Материал (CRUD)
class EducationalMaterialViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    queryset = EducationalMaterial.objects.all()
    serializer_class = EducationalMaterialSerializer

# Задание (CRUD)
class TaskViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Выполненное Задание (CRUD)
class CompletedTaskViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    queryset = CompletedTask.objects.all()
    serializer_class = CompletedTaskSerializer

# Участник (CRUD)
class ParticipantViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

# Сертификат (CRUD)
class CertificateViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

# Заявка на обучение (CRUD)
class ApplicationViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Регистрация доступна всем

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Генерируем JWT-токен
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Пользователь успешно зарегистрирован",
                "access": access_token,
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)