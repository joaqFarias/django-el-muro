from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z.áéíóúÁÉÍÓÚ ]+$')

        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name_len'] = "El nombre debe tener al menos 2 caracteres de largo.";

        if len(postData['last_name']) < 2:
            errors['last_name_len'] = "El apellido debe tener al menos 2 caracteres de largo.";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido. Ingrese correo valido."

        all_users = User.objects.all()
        for user in all_users:
            if postData['email'] == user.email:
                errors['email_repetido'] = "Este correo ya ha sido ocupado."

        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras'] = "El nombre solo debe contener letras."

        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_letras'] = "El apellido solo debe contener letras."

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=70)

    # mensaje
    # comentario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

class MensajeComentarioManager(models.Manager):
    def validador_mensajes(self, postData):
        # (r'^[a-zA-Z.áéíóúÁÉÍÓÚ_-,.;+"¡¿!? ]+$')
        PARRAFOS = re.compile(r'^[a-zA-Z.áéíóúÁÉÍÓÚ,.;+"¡¿!? ]+$')

        errors = {}

        if len(postData['contenido']) < 1:
            errors['contenido_len'] = "El texto no puede estar vacio.";


        if not PARRAFOS.match(postData['contenido']):
            errors['solo_parrafos'] = "Se encontraron caracteres extraños en el texto."

        return errors

class Mensaje(models.Model):
    contenido = models.CharField(max_length=1000)
    usuario = models.ForeignKey(User, related_name="mensaje", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MensajeComentarioManager()

    def __str__(self):
        return f"{self.contenido}"

    def __repr__(self):
        return f"{self.contenido}"

class Comentario(models.Model):
    contenido = models.CharField(max_length=1000)

    usuario = models.ForeignKey(User, related_name="comentario", on_delete=models.CASCADE)
    mensaje = models.ForeignKey(Mensaje, related_name="mensaje", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MensajeComentarioManager()

    def __str__(self):
        return f"{self.contenido}"

    def __repr__(self):
        return f"{self.contenido}"

