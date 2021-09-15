from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import *

def nuevo_mensaje_comentario(request, tipo_texto):
    print(request.POST)
    if request.method == "POST":
        if tipo_texto == 'mensaje':
            errors = Mensaje.objects.validador_mensajes(request.POST)
        elif tipo_texto == 'comentario':    
            errors = Comentario.objects.validador_mensajes(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

        else:
            if tipo_texto == 'mensaje':
                mensaje_nuevo = Mensaje.objects.create(
                    contenido=request.POST['contenido'],
                    usuario=User.objects.get(id=int(request.session['user']['id']))
                )
                mensaje_nuevo.save()
                messages.success(request, "El mensaje se publico con exito.")

            elif tipo_texto == 'comentario':
                comentario_nuevo = Comentario.objects.create(
                    contenido=request.POST['contenido'],
                    usuario=User.objects.get(id=int(request.session['user']['id'])),
                    mensaje=Mensaje.objects.get(id=int(request.POST['id_mensaje']))
                )
                comentario_nuevo.save()
                messages.success(request, "El comentario se publico con exito.")
    
    return redirect('/')

@login_required
def index(request):

    mensajes = Mensaje.objects.all()
    comentarios = Comentario.objects.all()

    context = {
        'user_id': request.session['user']['id'],
        'mensajes': mensajes,
        'comentarios': comentarios
    }
    
    return render(request, 'index.html', context)
