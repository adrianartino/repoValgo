
from django.shortcuts import redirect, render
from .models import Usuarios, Fraccionamiento



def verFraccionamientos(request):
    if "usuario_id" in request.session:
        
        return render(request, "fraccionamientos/verFraccionamientos.html")
    

    else:
        return redirect("login")

