from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from ...Core.Data.BaseModel import BaseModel
from ...Validators.RequestValidator import ValidatorTypes

class Plant(BaseModel):
    """ Modelo de datos que la tabla A02_Planta_Empresa

    Args:
        Base (ORMClass): Herede la clase BaseModel

    Returns:
        Plant: Devuelve una instancia correspondiente a una fila de la tabla
    """

    __tablename__ = 'A02_Planta_Empresa'
    id = Column("id_planta", Integer, primary_key=True)
    id_client = Column("id_cliente", Integer, nullable=False)
    name = Column("nombre_corto", String(50))
    longName = Column("nombre_largo", String(150))
    alias = Column("alias", String(100))

    unifilar_points = relationship("UnifilarPoint", back_populates='plant')

    filter_columns = ['id_client']
    relationship_names = ['unifilar_points']
    search_columns = ['name', 'longName', 'alias']
    signed_urls = []

    # This model path is used to know which path will raise the event
    model_path_name = "plant"
    
    def property_map(self) -> Dict:
        return {}
    
    def display_members(self) -> List[str]:
        return [
            "id", "id_client", "name", "longName", "alias"
        ]

    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "name": [ValidatorTypes.REQUIRED.value,ValidatorTypes.STRING.value],
            "longName": [ValidatorTypes.REQUIRED.value,ValidatorTypes.STRING.value],
            "id_client": [ValidatorTypes.REQUIRED.value,ValidatorTypes.NUMERIC.value],
        }
