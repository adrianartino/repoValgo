"""
URL configuration for travertinos project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from appValgo.views import (
    cambiar_password_usuario,
    inicio,
    login,
    logout,
    usuarios,
)

from appValgo import viewsFraccionamientos, viewsColonos, viewsCobranza

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login, name="login"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("inicio/", inicio, name="inicio"),
    path("usuarios/", usuarios, name="usuarios"),
    path(
        "usuarios/<int:usuario_id>/password/",
        cambiar_password_usuario,
        name="cambiar_password_usuario",
    ),
    
    # FRACCIONAMIENTOS ------------------------------------
    path("verFraccionamientos/",viewsFraccionamientos.verFraccionamientos, name="verFraccionamientos"), 
    
    # COLONOS ---------------------------------------------
    path("verColonos/", viewsColonos.verColonos, name="verColonos"),
    
    # COBRANZA --------------------------------------------
    
    # Cuotas de mantenimiento
    path("historialCuotasMtto/", viewsCobranza.historialCuotasMtto, name="historialCuotasMtto"),
    path("cuotasMesMtto/", viewsCobranza.cuotasMesMtto, name="cuotasMesMtto"),
    path("clientesMorososMtto/", viewsCobranza.clientesMorososMtto, name="clientesMorososMtto"),
    path("penalizacionesMtto/", viewsCobranza.penalizacionesMtto, name="penalizacionesMtto"),
    
    # Cuotas de agua
    path("historialCuotasAgua/", viewsCobranza.historialCuotasAgua, name="historialCuotasAgua"),
    path("cuotasMesAgua/", viewsCobranza.cuotasMesAgua, name="cuotasMesAgua"),
    path("clientesMorososAgua/", viewsCobranza.clientesMorososAgua, name="clientesMorososAgua"),
    path("penalizacionesAgua/", viewsCobranza.penalizacionesAgua, name="penalizacionesAgua"),
    
    # Reportes cuotas mantenimiento
    path("estadoDeCuentaClienteMtto/", viewsCobranza.estadoDeCuentaClienteMtto, name="estadoDeCuentaClienteMtto"),
    path("resumenMensualFraccMtto/", viewsCobranza.resumenMensualFraccMtto, name="resumenMensualMtto"),
    path("carteraVencidaMtto/", viewsCobranza.carteraVencidaMtto, name="carteraVencidaMtto"),
    # Reportes cuotas agua
    path("estadoDeCuentaClienteAgua/", viewsCobranza.estadoDeCuentaClienteAgua, name="estadoDeCuentaClienteAgua"),
    path("resumenMensualFraccAgua/", viewsCobranza.resumenMensualFraccAgua, name="resumenMensualAgua"),
    path("carteraVencidaAgua/", viewsCobranza.carteraVencidaAgua, name="carteraVencidaAgua"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
