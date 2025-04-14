from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
from pathlib import Path

from .models import *
from .serializers import *

BASE_DIR = Path(__file__).resolve().parent.parent
pdfmetrics.registerFont(TTFont('Arial', f'/root/{BASE_DIR}/fonts/arial.ttf'))

# Роль (CRUD)
class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# Пользователь (CRUD)
class CustomUserViewSet(viewsets.ModelViewSet):    
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

# Программа (CRUD)
class ProgramViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

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

# Учебный Материал (CRUD) + GET с заданиями
class EducationalMaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EducationalMaterial.objects.all()
    serializer_class = EducationalMaterialSerializer

    @action(detail=False, methods=["get"], url_path="with_tasks")
    def with_tasks(self, request):
        program_id = request.query_params.get("program")
        if not program_id:
            return Response({"detail": "Параметр program обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        materials = EducationalMaterial.objects.filter(program_id=program_id)
        data = []

        for material in materials:
            task = Task.objects.filter(material=material).first()
            task_data = None
            if task:
                task_data = {
                    "id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "extra_materials": task.extra_materials,
                    "section": task.section.id if task.section else None,
                }

            data.append({
                "id": material.id,
                "name": material.name,
                "description": material.description,
                "program": material.program.id if material.program else None,
                "task": task_data
            })

        return Response(data)

# Задание (CRUD) + ответ
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["post"], url_path="response")
    def response(self, request, pk=None):
        task = self.get_object()
        user = request.user
        answer_text = request.data.get("answer")

        if not answer_text:
            return Response({"detail": "Необходимо передать ответ."}, status=status.HTTP_400_BAD_REQUEST)

        CompletedTask.objects.create(
            task=task,
            user=user,
            answer=answer_text,
            submission_date = datetime.now(),
            status = 'Ответ получен'
        )

        return Response({"message": "Ответ отправлен успешно."}, status=status.HTTP_201_CREATED)

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

# Сертификат (CRUD) + генерация PDF
class CertificateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    @action(detail=True, methods=["get"], url_path="download")
    def download_certificate(self, request, pk=None):
        cert = self.get_object()
        user = cert.user
        program = cert.program

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.setFont("Arial", 20)
        p.drawCentredString(300, 750, "СЕРТИФИКАТ")
        p.setFont("Arial", 14)
        p.drawCentredString(300, 700, f"Выдан: {user.username}")
        p.drawCentredString(300, 670, f"За прохождение программы:")
        p.drawCentredString(300, 640, f"{program.name}")
        p.drawCentredString(300, 580, f"Дата выдачи: {cert.issued_date.strftime('%d.%m.%Y')}")

        p.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename="certificate.pdf")

# Заявка на обучение (CRUD)
class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

# Регистрация
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_serializer = CustomTokenObtainPairSerializer()
            refresh = token_serializer.get_token(user)

            return Response({
                "message": "Пользователь успешно зарегистрирован",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# JWT Авторизация
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
