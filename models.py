from database import Base
from sqlalchemy import String, Integer, Float, Column

class Addresses(Base):
    __tablename__='addresses'
    id = Column(Integer, primary_key=True)
    codigo_postal = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    nombre_comuna = Column(String)
    nombre_calle = Column(String)
    numero_municipal = Column(Integer)
    
    def __repr__(self):
        return f"<Addresses id={self.id} codigo_postal={self.codigo_postal} lat={self.lat}  lon={self.lon} nombre_comuna={self.nombre_comuna}> nombre_calle={self.nombre_calle} numero_municipal={self.numero_municipal}"
    
    