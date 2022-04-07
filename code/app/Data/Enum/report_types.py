from enum import Enum

class ReportType(Enum):
    """
    Enum que contiene los diferentes tipos de solicitudes al GRAM.

    Args:
        Enum (int): ID de tipo de reporte.
    """
    # Notificación de cumplimiento
    ACCOMPLISHMENT = 2
    # Reporte oficial
    OFFICIAL = 1
    # Reporte transaccional
    TRANSACTIONAL = 3
