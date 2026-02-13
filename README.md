# Gestor Inteligente de Clientes (GIC)

Sistema SaaS de gestion de clientes desarrollado para **SolutionTech**, implementado en Python 3 con Programacion Orientada a Objetos.

## Descripcion

GIC permite gestionar diferentes tipos de clientes (Regular, Premium, Corporativo) con validaciones avanzadas, persistencia multiple (SQLite, JSON, CSV), API REST y interfaz web.

## Tecnologias

- **Python 3.9+**
- **Flask 3.0** - API REST y GUI Web
- **SQLite** - Base de datos
- **pytest** - 47 tests unitarios
- **Loguru** - Sistema de logs
- **email-validator** / **phonenumbers** - Validaciones

## Estructura del Proyecto
cat > README.md << 'ENDOFFILE'
# Gestor Inteligente de Clientes (GIC)

Sistema SaaS de gestion de clientes desarrollado para **SolutionTech**, implementado en Python 3 con Programacion Orientada a Objetos.

## Descripcion

GIC permite gestionar diferentes tipos de clientes (Regular, Premium, Corporativo) con validaciones avanzadas, persistencia multiple (SQLite, JSON, CSV), API REST y interfaz web.

## Tecnologias

- **Python 3.9+**
- **Flask 3.0** - API REST y GUI Web
- **SQLite** - Base de datos
- **pytest** - 47 tests unitarios
- **Loguru** - Sistema de logs
- **email-validator** / **phonenumbers** - Validaciones

## Estructura del Proyecto
```
gic/
├── config.py                  # Configuracion centralizada
├── requirements.txt           # Dependencias
├── scripts/
│   └── run.py                 # Demo del sistema
├── src/
│   ├── models/                # Clases POO (Cliente, Regular, Premium, Corporativo)
│   ├── services/              # Logica de negocio (ClienteService)
│   ├── repositories/          # Persistencia (SQLite, JSON, CSV)
│   ├── database/              # Conexion y migraciones
│   ├── api/                   # API REST Flask
│   │   ├── routes/            # Endpoints CRUD
│   │   └── middlewares/       # Error handler, Auth
│   ├── gui/                   # Interfaz web Flask
│   ├── integrations/          # APIs externas (Identity, Email)
│   ├── exceptions/            # Excepciones personalizadas
│   └── utils/                 # Validadores, logger, helpers
├── tests/
│   ├── test_models/           # Tests de modelos (24 tests)
│   └── test_api/              # Tests de API REST (23 tests)
├── data/                      # Exportaciones JSON/CSV
└── docs/                      # Documentacion y diagramas UML
```

## Instalacion
```bash
git clone https://github.com/daniklagges/Gestor-Inteligente-de-Clientes-GIC-.git
cd Gestor-Inteligente-de-Clientes-GIC-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Uso

### Demo del sistema
```bash
PYTHONPATH=. python3 scripts/run.py
```

### API REST (puerto 5000)
```bash
PYTHONPATH=. python3 src/api/app.py
```

Endpoints disponibles:

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Info del sistema |
| GET | `/health` | Health check |
| GET | `/api/clientes` | Listar clientes |
| GET | `/api/clientes/<id>` | Obtener cliente |
| POST | `/api/clientes` | Crear cliente |
| PUT | `/api/clientes/<id>` | Actualizar cliente |
| DELETE | `/api/clientes/<id>` | Eliminar cliente |
| PATCH | `/api/clientes/<id>/toggle` | Activar/Desactivar |
| GET | `/api/clientes/stats` | Estadisticas |
| POST | `/api/clientes/export/json` | Exportar a JSON |
| POST | `/api/clientes/export/csv` | Exportar a CSV |

Ejemplo crear cliente:
```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"tipo":"Premium","nombre":"Ana Silva","email":"ana@test.com","telefono":"+56944556677","direccion":"Av Providencia 123","nivel_premium":"Gold"}'
```

### Interfaz Web (puerto 5001)
```bash
PYTHONPATH=. python3 src/gui/main_window.py
```
Abrir en navegador: `http://localhost:5001`

### Tests
```bash
PYTHONPATH=. python3 -m pytest tests/ -v
```

## Arquitectura POO

### Jerarquia de Clases
```
Cliente (base abstracta)
├── ClienteRegular    - Puntos de fidelidad, descuento 0-5%
├── ClientePremium    - Niveles Gold/Platinum/Diamond, descuento 10-20%
└── ClienteCorporativo - RUT empresa, descuento 5-20% por empleados
```

### Pilares POO Implementados

- **Encapsulacion**: Atributos privados con propiedades y validacion automatica
- **Herencia**: 3 subclases especializadas con `super()` y extension de metodos
- **Polimorfismo**: `calcular_descuento()` con comportamiento diferente por tipo
- **Abstraccion**: Modelado de entidades reales con atributos esenciales

### Patrones de Diseno

- **Repository Pattern** - Desacopla logica de negocio de persistencia
- **Factory Pattern** - `crear_cliente()` instancia el tipo correcto
- **Service Layer** - `ClienteService` orquesta toda la logica de negocio

### Excepciones Personalizadas
```
Exception
├── GICValidationError
│   ├── EmailInvalidoError
│   ├── TelefonoInvalidoError
│   ├── NombreInvalidoError
│   ├── RutInvalidoError
│   └── DireccionInvalidaError
├── GICDatabaseError
│   ├── RegistroNoEncontradoError
│   └── RegistroDuplicadoError
└── GICAPIError
    ├── APIExternaError
    └── APITimeoutError
```

## Documentacion

- `docs/Documento_Explicativo_POO_GIC.docx` - Documento explicativo sobre POO
- `docs/diagramas/diagrama_clases.md` - Diagrama UML (Mermaid, se renderiza en GitHub)
- `docs/diagramas/diagrama_clases_gic.puml` - Diagrama UML (PlantUML)
- `docs/diagramas/diagrama_clases_gic.png` - Diagrama UML (imagen)

## Autor

Desarrollado para SolutionTech - Febrero 2026
