from django.db import models
from django.contrib.auth.models import User


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class DesignerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("designing", "Designing"),
        ("quotation", "Quotation"),
        ("approved", "Approved"),
        ("completed", "Completed"),
    ]

    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    designer = models.ForeignKey(
        DesignerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects"
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    style = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Room(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    name = models.CharField(max_length=100)

    length = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    width = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    height = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    requirements = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="room_images/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image - {self.room.name}"


class Design(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="designs"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    design_image = models.ImageField(
        upload_to="designs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Material(models.Model):

    name = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.name


class Quotation(models.Model):

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="quotation"
    )

    material_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    labour_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    other_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True)

    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quotation - {self.project.name}"


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items"
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.CharField(max_length=200)

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.description


class Revision(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="revisions"
    )

    design = models.ForeignKey(
        Design,
        on_delete=models.CASCADE,
        related_name="revisions"
    )

    description = models.TextField()

    revision_image = models.ImageField(
        upload_to="revisions/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revision - {self.project.name}"


class ProjectFile(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="files"
    )

    name = models.CharField(max_length=200)

    file = models.FileField(upload_to="project_files/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name