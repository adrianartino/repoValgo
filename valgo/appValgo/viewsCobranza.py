
from django.shortcuts import redirect, render
from .models import Usuarios, Fraccionamiento


# CUOTAS DE MANTENIMIENTO ------------------------------------------------------------
def historialCuotasMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasMtto/historialCuotasMtto.html")
    

    else:
        return redirect("login")
    
def cuotasMesMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasMtto/cuotasMesMtto.html")
    

    else:
        return redirect("login")
    
def clientesMorososMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasMtto/clientesMorososMtto.html")
    

    else:
        return redirect("login")
    
def penalizacionesMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasMtto/penalizacionesMtto.html")
    

    else:
        return redirect("login")
    
    
# CUOTAS DE AGUA ---------------------------------------------------------------------------------

def historialCuotasAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasAgua/historialCuotasAgua.html")
    

    else:
        return redirect("login")

def cuotasMesAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasAgua/cuotasMesAgua.html")
    

    else:
        return redirect("login")
    
def clientesMorososAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasAgua/clientesMorososAgua.html")
    

    else:
        return redirect("login")
    
def penalizacionesAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/cuotasAgua/penalizacionesAgua.html")
    

    else:
        return redirect("login")
    
    
    
# REPORTES MTTO
def estadoDeCuentaClienteMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/reportes/cuotasMtto/estadoDeCuentaClienteMtto.html")
    
    else:
        return redirect("login")
    
def resumenMensualFraccMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/reportes/cuotasMtto/resumenMensualFraccMtto.html")
    
    else:
        return redirect("login")
    
def carteraVencidaMtto(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/reportes/cuotasMtto/carteraVencidaMtto.html")
    
    else:
        return redirect("login")


# REPORTES AGUA
def estadoDeCuentaClienteAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/reportes/cuotasAgua/estadoDeCuentaClienteAgua.html")
    
    else:
        return redirect("login")
    
def resumenMensualFraccAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/reportes/cuotasAgua/resumenMensualFraccAgua.html")
    
    else:
        return redirect("login")
    
def carteraVencidaAgua(request):
    if "usuario_id" in request.session:
        
        return render(request, "cobranza/reportes/cuotasAgua/carteraVencidaAgua.html")
    
    else:
        return redirect("login")

