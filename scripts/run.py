"""
Script principal de entrada para el proyecto GIC.
Inicializa la base de datos y ejecuta la interfaz seleccionada.
"""
import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(__file__))

from src.database.migrations import crear_tablas
from src.services.cliente_service import ClienteService
from src.utils.logger import logger


def demo():
    """Ejecuta una demostración básica del sistema."""
    print("=" * 60)
    print("  GESTOR INTELIGENTE DE CLIENTES (GIC) - Demo")
    print("=" * 60)

    # Inicializar BD
    crear_tablas()
    service = ClienteService()

    # Crear clientes de ejemplo
    try:
        c1 = service.crear_cliente(
            "Regular",
            nombre="Juan Pérez",
            email="juan@example.com",
            telefono="+56944556677",
            direccion="Av. Siempre Viva 123, Santiago",
        )
        print(f"\n✅ Creado: {c1}")

        c2 = service.crear_cliente(
            "Premium",
            nombre="María López",
            email="maria@example.com",
            telefono="+56955667788",
            direccion="Los Leones 789, Providencia",
            nivel_premium="Platinum",
        )
        print(f"✅ Creado: {c2}")

        c3 = service.crear_cliente(
            "Corporativo",
            nombre="Carlos Díaz",
            email="carlos@empresa.cl",
            telefono="+56966778899",
            direccion="Apoquindo 1000, Las Condes",
            rut_empresa="76.124.890-1",
            razon_social="TechCorp SpA",
            cantidad_empleados=100,
        )
        print(f"✅ Creado: {c3}")

    except Exception as e:
        print(f"⚠️  {e}")

    # Listar clientes
    print(f"\n📋 Clientes en el sistema:")
    print("-" * 60)
    for cliente in service.listar_clientes():
        print(f"  {cliente}")

    # Estadísticas
    stats = service.estadisticas()
    print(f"\n📊 Estadísticas:")
    print(f"  Total: {stats['total']}")
    print(f"  Regulares: {stats['regulares']}")
    print(f"  Premium: {stats['premium']}")
    print(f"  Corporativos: {stats['corporativos']}")

    # Demostrar polimorfismo
    print(f"\n💰 Descuentos sobre $100.000 (Polimorfismo):")
    for cliente in service.listar_clientes():
        dcto = cliente.calcular_descuento(100000)
        print(f"  {cliente.nombre} ({cliente.tipo_cliente}): ${dcto:,.0f}")

    # Exportar
    ruta_json = service.exportar_json()
    ruta_csv = service.exportar_csv()
    print(f"\n💾 Exportado a: {ruta_json}")
    print(f"💾 Exportado a: {ruta_csv}")

    print("\n" + "=" * 60)
    print("  Demo completada exitosamente ✅")
    print("=" * 60)


if __name__ == "__main__":
    demo()
