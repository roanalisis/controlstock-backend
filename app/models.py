from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, func
from app.database import Base


class Usuario(Base):
    """Modelo de usuario para autenticación."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)


class Reporte(Base):
    """Modelo del reporte de ventas y stock."""
    __tablename__ = "reporte"

    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(255), nullable=False, index=True)
    stock_actual = Column(Numeric(10, 2), nullable=False, default=0)
    cantidad_vendida = Column(Numeric(10, 2), nullable=False, default=0)
    fecha = Column(DateTime, server_default=func.current_timestamp(), index=True)


class StockCritico(Base):
    """Configuración de stock crítico por producto."""
    __tablename__ = "stock_critico"

    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(255), unique=True, nullable=False, index=True)
    valor_critico = Column(Numeric(10, 2), nullable=False, default=0)
