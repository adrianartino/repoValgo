
from django.shortcuts import redirect, render
from .models import Usuarios, Fraccionamiento



def verColonos(request):
    if "usuario_id" in request.session:
        
        return render(request, "colonos/verColonos.html")
    

    else:
        return redirect("login")

