from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import ClientProfile, DesignerProfile, Project
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ClientProfile, DesignerProfile, Project, Room, RoomImage
from django.conf import settings
from django.conf.urls.static import static
from .ai_service import analyze_room_with_gemini

def home(request):
    return render(request, "front_page.html")


def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password"])

            user.save()

            role = form.cleaned_data["role"]

            if role == "client":
                ClientProfile.objects.create(user=user)

            elif role == "designer":
                DesignerProfile.objects.create(user=user)

            login(request, user)

            if role == "client":
                return redirect("client_dashboard")

            return redirect("designer_dashboard")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if ClientProfile.objects.filter(user=user).exists():
                return redirect("client_dashboard")

            if DesignerProfile.objects.filter(user=user).exists():
                return redirect("designer_dashboard")

            return redirect("home")

        return render(
            request,
            "login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "login.html")


def user_logout(request):

    logout(request)

    return redirect("home")


def client_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    client_profile = ClientProfile.objects.get(user=request.user)

    projects = client_profile.projects.all().order_by("-created_at")

    total_projects = projects.count()
    active_projects = projects.exclude(
        status__in=["completed"]
    ).count()

    completed_projects = projects.filter(
        status="completed"
    ).count()

    return render(
        request,
        "client_dashboard.html",
        {
            "client_profile": client_profile,
            "projects": projects,
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
        }
    )


def designer_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "designer_dashboard.html")
@login_required
def create_project(request):

    if not ClientProfile.objects.filter(user=request.user).exists():
        return redirect("home")

    client_profile = ClientProfile.objects.get(user=request.user)

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        budget = request.POST.get("budget")
        style = request.POST.get("style")

        project = Project.objects.create(
            client=client_profile,
            name=name,
            description=description,
            budget=budget if budget else None,
            style=style,
        )

        return redirect("client_dashboard")

    return render(request, "create_project.html")
@login_required
def room_details(request, project_id):

    client_profile = ClientProfile.objects.get(
        user=request.user
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        client=client_profile
    )

    rooms = project.rooms.all()

    return render(
        request,
        "room_details.html",
        {
            "project": project,
            "rooms": rooms,
        }
    )

@login_required
def add_room(request, project_id):

    client_profile = ClientProfile.objects.get(
        user=request.user
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        client=client_profile
    )

    if request.method == "POST":

        room = Room.objects.create(
            project=project,
            name=request.POST.get("name"),
            length=request.POST.get("length") or None,
            width=request.POST.get("width") or None,
            height=request.POST.get("height") or None,
            requirements=request.POST.get("requirements"),
        )

        image = request.FILES.get("image")

        if image:
            RoomImage.objects.create(
                room=room,
                image=image
            )

        return redirect("room_details", project_id=project.id)

    return render(
        request,
        "add_room.html",
        {
            "project": project
        }
    )
@login_required
def analyze_room(request, room_id):

    if request.method != "POST":
        return redirect("client_dashboard")

    client_profile = ClientProfile.objects.get(
        user=request.user
    )

    room = get_object_or_404(
        Room,
        id=room_id,
        project__client=client_profile
    )

    image = room.images.order_by("-uploaded_at").first()

    if not image:
        return render(
            request,
            "room_details.html",
            {
                "project": room.project,
                "rooms": room.project.rooms.all(),
                "error": "Please upload a room photo before using AI analysis."
            }
        )

    try:
        analysis = analyze_room_with_gemini(image.image.path)

        return render(
            request,
            "room_details.html",
            {
                "project": room.project,
                "rooms": room.project.rooms.all(),
                "analysis": analysis,
                "analyzed_room": room,
            }
        )

    except Exception as e:
        return render(
            request,
            "room_details.html",
            {
                "project": room.project,
                "rooms": room.project.rooms.all(),
                "error": f"AI analysis failed: {str(e)}"
            }
        )