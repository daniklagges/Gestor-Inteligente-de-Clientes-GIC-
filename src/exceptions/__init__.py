from src.exceptions.validation_errors import (
    GICValidationError,
    EmailInvalidoError,
    TelefonoInvalidoError,
    DireccionInvalidaError,
    NombreInvalidoError,
    RutInvalidoError,
)
from src.exceptions.database_errors import (
    GICDatabaseError,
    ConexionDBError,
    RegistroNoEncontradoError,
    RegistroDuplicadoError,
)
from src.exceptions.api_errors import (
    GICAPIError,
    APIExternaError,
    APITimeoutError,
)
