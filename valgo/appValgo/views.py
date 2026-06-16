from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404, redirect, render

from .models import Usuarios






def login(request):
    if "usuario_id" in request.session:
        return redirect("inicio")

    if request.method == "POST":
        usuario = request.POST.get("username", "").strip()
        contra = request.POST.get("password", "")

        usuario_sistema = Usuarios.objects.filter(
            nombre_usuario=usuario,
            contraseña=contra,
            estatus_usuario="A",
        ).first()

        if usuario_sistema is not None:
            request.session["usuario_id"] = usuario_sistema.id_usuario
            request.session["usuario_nombre"] = usuario_sistema.nombre_usuario
            request.session["nombre_completo"] = usuario_sistema.nombres
            request.session["es_admin"] = False
            return redirect("inicio")

        return render(request, "login/login.html", {"error": True})

    return render(request, "login/login.html")


def logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect("login")


def inicio(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    nombre_usuario_logueado = request.session["usuario_nombre"]
    return render(request, "inicio/inicio.html", {"nombre_usuario": nombre_usuario_logueado})


def usuarios(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    nombre_usuario_logueado = request.session["usuario_nombre"]
    error_creacion = None

    if request.method == "POST":
        nombre_usuario = request.POST.get("nombre_usuario", "").strip()
        nombres = request.POST.get("nombres", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        estatus_usuario = "A" if request.POST.get("estatus_usuario") == "on" else "I"

        if not nombre_usuario or not nombres or not password:
            error_creacion = "El usuario, nombre y contrasena son obligatorios."
            messages.error(request, error_creacion)
        elif password != password_confirm:
            error_creacion = "Las contrasenas no coinciden."
            messages.error(request, error_creacion)
        elif Usuarios.objects.filter(nombre_usuario=nombre_usuario).exists():
            error_creacion = "Ese nombre de usuario ya existe."
            messages.error(request, error_creacion)
        else:
            Usuarios.objects.create(
                nombre_usuario=nombre_usuario,
                nombres=nombres,
                contraseña=password,
                estatus_usuario=estatus_usuario,
            )
            messages.success(request, "Usuario registrado")
            return redirect("usuarios")

    usuarios_registrados = Usuarios.objects.all().order_by("nombre_usuario")

    return render(
        request,
        "usuarios/usuarios.html",
        {
            "nombre_usuario": nombre_usuario_logueado,
            "usuarios": usuarios_registrados,
            "error_creacion": error_creacion,
        },
    )


def cambiar_password_usuario(request, usuario_id):
    if "usuario_id" not in request.session:
        return redirect("login")

    nombre_usuario_logueado = request.session["usuario_nombre"]
    usuario = get_object_or_404(Usuarios, id_usuario=usuario_id)
    error_password = None

    if request.method == "POST":
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not password:
            error_password = "La contrasena no puede estar vacia."
        elif password != password_confirm:
            error_password = "Las contrasenas no coinciden."
        else:
            usuario.contraseña = password
            usuario.save()
            return redirect("usuarios")

    return render(
        request,
        "usuarios/cambiarPasswordUsuario.html",
        {
            "nombre_usuario": nombre_usuario_logueado,
            "usuario_sistema": usuario,
            "error_password": error_password,
        },
    )

