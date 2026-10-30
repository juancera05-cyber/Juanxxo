# Taller: Endpoints en Django nativo (GET, POST, PUT, DELETE)

**Curso:** Desarrollo de aplicaciones Web I – 4E
**Docente:** Jose Javier Torres Vanstrahlen

API REST básica construida **solo con Django** (sin Django REST Framework ni otras librerías externas), usando una **vista basada en clase** (`View`) con los métodos `get()`, `post()`, `put()` y `delete()`.

---

## 1. Archivos modificados

```
Activity/
├── manage.py
├── Activity/
│   └── urls.py      # MODIFICADO: incluye las rutas de App_1 bajo /api/
└── App_1/
    ├── models.py    # Modelo profile (name, last_name, age, status) - sin cambios
    ├── views.py     # MODIFICADO: ProfileView con get, post, put y delete
    └── urls.py      # NUEVO: rutas de la app
```

## 2. Cómo ejecutarlo

```bash
cd Activity
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install django
python manage.py migrate
python manage.py runserver
```

## 3. Endpoints

| Verbo  | URL                    | Operación CRUD | Qué hace                    | Código éxito |
|--------|------------------------|----------------|-----------------------------|--------------|
| GET    | `/api/profiles/`      | **R**ead       | Lista todos los perfiles   | 200          |
| GET    | `/api/profiles/<id>/` | **R**ead       | Obtiene un perfil         | 200          |
| POST   | `/api/profiles/`      | **C**reate     | Crea un perfil            | 201          |
| PUT    | `/api/profiles/<id>/` | **U**pdate     | Actualiza un perfil       | 200          |
| DELETE | `/api/profiles/<id>/` | **D**elete     | Elimina un perfil         | 200          |

Si el id no existe se responde **404**; si el JSON es inválido o faltan `name`, `last_name` o `age`, **400**.

### Ejemplos de prueba (curl o Postman)

```bash
curl -X POST http://127.0.0.1:8000/api/profiles/ -H "Content-Type: application/json" -d "{\"name\":\"Juan\",\"last_name\":\"Perez\",\"age\":20}"
curl http://127.0.0.1:8000/api/profiles/
curl http://127.0.0.1:8000/api/profiles/1/
curl -X PUT http://127.0.0.1:8000/api/profiles/1/ -H "Content-Type: application/json" -d "{\"age\":21}"
curl -X DELETE http://127.0.0.1:8000/api/profiles/1/
```

---

## 4. Investigación: verbos HTTP y su relación con CRUD

| Verbo HTTP | CRUD   | Caso de uso | Características |
|------------|--------|-------------|-----------------|
| **GET**    | Read   | Consultar información: listar productos, ver el perfil de un usuario, buscar. | No modifica datos (seguro) e idempotente. Los parámetros van en la URL, no en el cuerpo. |
| **POST**   | Create | Registrar un usuario, enviar un formulario, crear un pedido. | Envía datos en el cuerpo. **No** es idempotente: repetirlo crea varios registros. Responde 201 Created. |
| **PUT**    | Update | Editar un registro existente identificado por su id (cambiar la edad de un perfil). | Idempotente: enviarlo varias veces deja el mismo resultado. Requiere el id en la URL. |
| **DELETE** | Delete | Eliminar un registro (borrar un perfil, cancelar una cuenta). | Idempotente. Requiere el id en la URL. |

> **Seguro** = no cambia el estado del servidor. **Idempotente** = hacer la misma petición 1 o 10 veces produce el mismo estado final.

### ¿Cómo sabe Django qué método ejecutar?

Cuando llega una petición, `ProfileView.as_view()` crea una instancia de la clase y llama a `dispatch()`. Este método lee `request.method` (por ejemplo `"PUT"`), lo pasa a minúsculas y ejecuta el método de la clase con ese nombre (`put()`). Si la clase no tiene ese método, Django responde automáticamente **405 Method Not Allowed**. Por eso basta con definir `get`, `post`, `put` y `delete` en la clase.

### Diferencia importante entre POST y PUT en Django

Django llena `request.POST` solo para formularios enviados con POST. Para recibir **JSON** (en POST o PUT) se lee el cuerpo crudo con `request.body` y se convierte con `json.loads()`. Ese es el enfoque usado en esta API.

---

## 5. Módulos, funciones y decoradores usados

| Elemento | Se importa desde | Descripción |
|----------|------------------|-------------|
| `View` | `django.views` | Clase base de las vistas basadas en clase. Su método `dispatch()` redirige cada petición al método con el nombre del verbo HTTP (`get`, `post`, `put`, `delete`). |
| `View.as_view()` | (método de `View`) | Convierte la clase en una función que el enrutador de URLs puede usar. Se llama en `urls.py`. |
| `JsonResponse` | `django.http` | Subclase de `HttpResponse` que convierte un diccionario de Python a JSON y pone la cabecera `Content-Type: application/json`. Permite indicar el código HTTP con `status=`. |
| `get_object_or_404` | `django.shortcuts` | Busca un objeto en la base de datos; si no existe, lanza `Http404` y Django responde 404 automáticamente. |
| `csrf_exempt` | `django.views.decorators.csrf` | Decorador que desactiva la verificación CSRF para la vista. Es necesario porque clientes como Postman o una app front-end no envían el token CSRF que Django exige en POST, PUT y DELETE. |
| `method_decorator` | `django.utils.decorators` | Adapta un decorador pensado para funciones (como `csrf_exempt`) para aplicarlo a un método de una clase. Con `name="dispatch"` afecta a todos los verbos. |
| `path` | `django.urls` | Define una ruta URL y la asocia a una vista. Permite convertidores como `<int:pk>` para capturar el id. |
| `include` | `django.urls` | Incluye el archivo `urls.py` de una aplicación dentro del `urls.py` principal del proyecto. |
| `models.Model` | `django.db.models` | Clase base para definir tablas de la base de datos mediante el ORM. |
| `Model.objects` (`all`, `create`) / `save()` / `delete()` | ORM de Django | Métodos del ORM para leer, crear, actualizar y eliminar registros sin escribir SQL. |
| `request.body` / `request.method` | `HttpRequest` | `body` contiene el cuerpo crudo de la petición (bytes); `method` indica el verbo HTTP usado. |
| `json.loads` | `json` (librería estándar de Python) | Convierte el texto JSON recibido en un diccionario de Python. No es una librería externa. |

---

## 6. Fuentes consultadas

1. Django Documentation – *Class-based views (Introduction)*. https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/
2. Django Documentation – *Base views: View, dispatch(), http_method_not_allowed()*. https://docs.djangoproject.com/en/stable/ref/class-based-views/base/
3. Django Documentation – *Request and response objects (HttpRequest, JsonResponse)*. https://docs.djangoproject.com/en/stable/ref/request-response/
4. Django Documentation – *Django shortcut functions (get_object_or_404)*. https://docs.djangoproject.com/en/stable/topics/http/shortcuts/
5. Django Documentation – *Cross Site Request Forgery protection (csrf_exempt)*. https://docs.djangoproject.com/en/stable/ref/csrf/
6. Django Documentation – *Decorating class-based views (method_decorator)*. https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/#decorating-class-based-views
7. Django Documentation – *URL dispatcher (path, include)*. https://docs.djangoproject.com/en/stable/topics/http/urls/
8. MDN Web Docs – *HTTP request methods*. https://developer.mozilla.org/es/docs/Web/HTTP/Methods
9. MDN Web Docs – *Idempotent*. https://developer.mozilla.org/en-US/docs/Glossary/Idempotent
