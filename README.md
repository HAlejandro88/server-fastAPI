


```yml
from fastapi import APIRouter, Depends, HTTPException

# Dependencias
def check_permissions(role: str = "user"):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"role": role}

def log_request():
    print("Logging request...")
    return {"log": "request_logged"}

# Crear el APIRouter con múltiples dependencias globales
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(check_permissions), Depends(log_request)]
)

@router.get("/data")
async def get_admin_data():
    return {"message": "Accessing admin data"}
```
Comportamiento:
	1.	Antes de ejecutar cualquier ruta dentro del APIRouter:
	•	Se ejecuta check_permissions para verificar los permisos del usuario.
	•	Se ejecuta log_request para registrar la solicitud (o realizar cualquier acción requerida).
	2.	Si alguna dependencia falla (por ejemplo, lanza un HTTPException), la ruta no se ejecutará.

### Multiples Dependencias

```yml
from fastapi import APIRouter, Depends, HTTPException

# Dependencia 1: Verifica permisos
def check_permissions(role: str = "user"):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"role": role}

# Dependencia 2: Conexión a base de datos
def get_db_connection():
    return {"db": "connected"}

# Ruta con múltiples dependencias
router = APIRouter()

@router.get("/data")
async def get_admin_data(
    role_info: dict = Depends(check_permissions), 
    db_info: dict = Depends(get_db_connection)
):
    # Ambas dependencias se ejecutan antes de entrar al cuerpo de la función
    return {"message": "Accessing admin data", "role": role_info, "db": db_info}
```

¿Cómo funciona?
	1.	check_permissions: Verifica que el rol sea “admin”. Si no lo es, lanza un error.
	2.	get_db_connection: Simula una conexión a la base de datos.
	3.	Ambas dependencias son pasadas como parámetros de la ruta. Depends(check_permissions) y Depends(get_db_connection) indican que la ejecución de estas dependencias debe ocurrir antes de ejecutar el cuerpo de la ruta.

Flujo:
	1.	Primero, FastAPI ejecuta check_permissions para validar el rol del usuario.
	2.	Luego, ejecuta get_db_connection para simular la conexión a la base de datos.
	3.	Finalmente, si ambas dependencias son exitosas, la función get_admin_data se ejecuta, y puedes acceder a sus valores como parámetros (role_info y db_info).