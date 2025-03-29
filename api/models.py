from django.db import models

# Роль (Role)
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

# Пользователь (User)
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

# Программа (Program)
class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=100)
    curator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=50)

# Раздел (Section)
class Section(models.Model):
    name = models.CharField(max_length=255)

# Подраздел (Subsection)
class Subsection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    extra_materials = models.TextField(blank=True, null=True)

# Программа Прогресс (ProgramProgress)
class ProgramProgress(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    completed_section = models.ForeignKey(Subsection, on_delete=models.CASCADE)

# Учебный Материал (EducationalMaterial)
class EducationalMaterial(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    file_path = models.TextField()
    uploaded_at = models.DateField(auto_now_add=True)

# Задание (Task)
class Task(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()

# Выполненное Задание (CompletedTask)
class CompletedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    submission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)

# Участник (Participant)
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    education = models.TextField()
    work_experience = models.TextField()

# Сертификат (Certificate)
class Certificate(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=255, unique=True)
    issued_date = models.DateField(auto_now_add=True)
    file_path = models.TextField()

# Заявка на обучение (Application)
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    submission_date = models.DateField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
