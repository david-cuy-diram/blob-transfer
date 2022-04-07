from enum import Enum

class ReportStatus(Enum):
    """ Clase que contiene los status generales de un reporte transaccional
    """

    PENDING             = 1
    IN_PROCCESS         = 2
    COMPLETED_CORRECT   = 3
    ERROR               = 4
    COMPLETED_HOLES     = 5
    ERROR_WRONG_PERIOD  = 6
    NO_DATA             = 7