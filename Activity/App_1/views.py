# LIBRERIAS
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import profile


def profile_to_dict(p):
    """Convierte un objeto profile en diccionario para devolverlo como JSON."""
    return {
        "id": p.id,
        "name": p.name,
        "last_name": p.last_name,
        "age": p.age,
        "status": p.status,
    }


# VISTA
@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(View):

    # GET -> READ (Leer): lista todos los perfiles, o uno solo si viene pk
    def get(self, request, pk=None):
        if pk is not None:
            p = get_object_or_404(profile, pk=pk)
            return JsonResponse(profile_to_dict(p), status=200)
        perfiles = [profile_to_dict(p) for p in profile.objects.all()]
        return JsonResponse({"profiles": perfiles}, status=200)

    # POST -> CREATE (Crear)
    def post(self, request):
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        faltantes = [c for c in ("name", "last_name", "age") if c not in datos]
        if faltantes:
            return JsonResponse({"error": f"Faltan campos: {', '.join(faltantes)}"}, status=400)

        p = profile.objects.create(
            name=datos["name"],
            last_name=datos["last_name"],
            age=datos["age"],
            status=datos.get("status", True),
        )
        return JsonResponse(profile_to_dict(p), status=201)

    # PUT -> UPDATE (Actualizar)
    def put(self, request, pk):
        p = get_object_or_404(profile, pk=pk)
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        p.name = datos.get("name", p.name)
        p.last_name = datos.get("last_name", p.last_name)
        p.age = datos.get("age", p.age)
        p.status = datos.get("status", p.status)
        p.save()
        return JsonResponse(profile_to_dict(p), status=200)

    # DELETE -> DELETE (Eliminar)
    def delete(self, request, pk):
        p = get_object_or_404(profile, pk=pk)
        p.delete()
        return JsonResponse({"mensaje": f"Perfil {pk} eliminado"}, status=200)
