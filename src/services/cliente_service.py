"""
Servicio de gestión de clientes - Capa de lógica de negocio.
Orquesta operaciones entre repositorios e integraciones.
"""
from typing import List, Optional
from src.models import Cliente, crear_cliente
from src.repositories.sqlite_repository import SQLiteRepository
from src.repositories.json_repository import JSONRepository
from src.repositories.csv_repository import CSVRepository
from src.exceptions.database_errors import RegistroDuplicadoError
from src.utils.logger import logger


class ClienteService:
    """
    Servicio principal para gestión de clientes.
    Actúa como intermediario entre la interfaz y los repositorios.
    """

    def __init__(self):
        self.db = SQLiteRepository()
        self.json_repo = JSONRepository()
        self.csv_repo = CSVRepository()

    def crear_cliente(self, tipo: str, **datos) -> Cliente:
        """
        Crea un nuevo cliente y lo persiste en la BD.
        Valida duplicados por email antes de crear.
        """
        # Verificar duplicados
        existente = self.db.obtener_por_email(datos.get("email", ""))
        if existente:
            raise RegistroDuplicadoError("email", datos["email"])

        # Crear instancia usando el factory
        cliente = crear_cliente(tipo, **datos)

        # Persistir
        self.db.crear(cliente)
        logger.info(f"Servicio: cliente creado ({tipo}) - {cliente.nombre}")
        return cliente

    def obtener_cliente(self, id: str) -> Cliente:
        """Obtiene un cliente por su ID."""
        return self.db.obtener_por_id(id)

    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca un cliente por email."""
        return self.db.obtener_por_email(email)

    def listar_clientes(
        self,
        activos_solo: bool = False,
        tipo: str = None,
        busqueda: str = None,
    ) -> List[Cliente]:
        """Lista clientes con filtros opcionales."""
        return self.db.listar(activos_solo=activos_solo, tipo=tipo, busqueda=busqueda)

    def actualizar_cliente(self, id: str, **datos) -> Cliente:
        """Actualiza los datos de un cliente existente."""
        cliente = self.db.obtener_por_id(id)

        # Actualizar atributos proporcionados
        for campo, valor in datos.items():
            if hasattr(cliente, campo) and valor is not None:
                setattr(cliente, campo, valor)

        self.db.actualizar(cliente)
        logger.info(f"Servicio: cliente actualizado - {cliente.nombre}")
        return cliente

    def eliminar_cliente(self, id: str) -> bool:
        """Elimina un cliente (borrado físico)."""
        return self.db.eliminar(id)

    def desactivar_cliente(self, id: str) -> bool:
        """Desactiva un cliente (borrado lógico)."""
        return self.db.desactivar(id)

    def exportar_json(self) -> str:
        """Exporta todos los clientes a JSON."""
        clientes = self.db.listar()
        return self.json_repo.exportar(clientes)

    def exportar_csv(self) -> str:
        """Exporta todos los clientes a CSV."""
        clientes = self.db.listar()
        return self.csv_repo.exportar(clientes)

    def importar_json(self) -> int:
        """Importa clientes desde JSON a la BD."""
        clientes = self.json_repo.importar()
        count = 0
        for cliente in clientes:
            try:
                self.db.crear(cliente)
                count += 1
            except RegistroDuplicadoError:
                logger.warning(f"Duplicado al importar: {cliente.email}")
        return count

    def estadisticas(self) -> dict:
        """Retorna estadísticas generales del sistema."""
        return {
            "total": self.db.contar(),
            "regulares": self.db.contar("Regular"),
            "premium": self.db.contar("Premium"),
            "corporativos": self.db.contar("Corporativo"),
        }
