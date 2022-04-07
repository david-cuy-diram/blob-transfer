from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from ...Core.Data.BaseModel import BaseModel
from ...Validators.RequestValidator import ValidatorTypes

class UnifilarPoint(BaseModel):
    """ Modelo de datos que la tabla A11_Punto_Unifilar

    Args:
        Base (ORMClass): Herede la clase BaseModel

    Returns:
        UnifilarPoint: Devuelve una instancia correspondiente a una fila de la tabla
    """

    __tablename__ = 'A11_Punto_Unifilar'

    id = Column("id_punto_unifilar", Integer, primary_key=True)
    id_plant = Column("id_planta", Integer, ForeignKey('A02_Planta_Empresa.id_planta'))
    name = Column("punto_unifilar", String(50))
    description = Column("descripcion", String(200))

    plant = relationship("Plant", back_populates='unifilar_points')
    
    filter_columns = ['id_plant']
    relationship_names = ['plant']
    search_columns = ['name', 'description']
    
    # This model path is used to know which path will raise the event
    model_path_name = "unifilar-point"
    
    def property_map(self) -> Dict:
        return {}
    
    def display_members(self) -> List[str]:
        return [
            "id", "name", "description", "id_plant"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "name": [ValidatorTypes.REQUIRED.value,ValidatorTypes.STRING.value],
            "id_plant": [ValidatorTypes.REQUIRED.value,ValidatorTypes.NUMERIC.value],
        }
