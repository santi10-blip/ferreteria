# src/db.py
import os
from sqlalchemy import (create_engine, Column, Integer, String, Numeric, Text,
                        ForeignKey, Date, JSON, TIMESTAMP, Table, MetaData)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Leer DATABASE_URL desde variable de entorno, si no existe construye una local
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:12345@localhost:5432/ferreteria")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)

class Proveedor(Base):
    __tablename__ = "proveedor"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20))
    email = Column(String(120))
    direccion = Column(Text)

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10,2))
    stock = Column(Integer)
    id_categoria = Column(Integer, ForeignKey("categoria.id"))
    especificaciones = Column(JSON)
    fecha_actualizacion = Column(TIMESTAMP, default=datetime.utcnow)

class Compatibilidad(Base):
    __tablename__ = "compatibilidad"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"))
    compatible_con = Column(Integer, ForeignKey("producto.id"))
    descripcion = Column(Text)

class Compra(Base):
    __tablename__ = "compra"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"))
    proveedor_id = Column(Integer, ForeignKey("proveedor.id"))
    cantidad = Column(Integer)
    costo_total = Column(Numeric(10,2))
    fecha_compra = Column(Date)

def init_db(create_sample_data: bool = True):
    """Crea las tablas y opcionalmente inserta datos de ejemplo."""
    Base.metadata.create_all(bind=engine)
    if create_sample_data:
        seed_data()

def seed_data():
    session = SessionLocal()
    # Evitar duplicados simples
    if session.query(Categoria).first():
        session.close()
        return

    # Categorías
    c1 = Categoria(nombre="Herramientas manuales", descripcion="Martillos, destornilladores, llaves")
    c2 = Categoria(nombre="Herramientas eléctricas", descripcion="Taladros, sierras, pulidoras")
    c3 = Categoria(nombre="Construcción", descripcion="Cemento, arena, varilla")
    session.add_all([c1, c2, c3])
    session.commit()

    # Proveedores
    p1 = Proveedor(nombre="Proveedor ABC", telefono="3170000000", email="abc@proveedor.com", direccion="Calle 1")
    p2 = Proveedor(nombre="Distribuciones XYZ", telefono="3100000000", email="xyz@proveedor.com", direccion="Calle 2")
    session.add_all([p1, p2])
    session.commit()

    # Productos
    prod1 = Producto(nombre="Martillo de Acero 16oz", descripcion="Martillo para carpintería", precio=28000, stock=15, id_categoria=c1.id, especificaciones={"peso":"16oz","material":"acero"})
    prod2 = Producto(nombre="Taladro percutor 850W", descripcion="Taladro para uso mixto", precio=230000, stock=8, id_categoria=c2.id, especificaciones={"potencia":"850W","voltaje":"110V"})
    prod3 = Producto(nombre="Tornillo rosca fina 1/4 x 1\"", descripcion="Bolsa 100 unidades", precio=1500, stock=500, id_categoria=c3.id, especificaciones={"unidad":"bolsa","cantidad":100})
    session.add_all([prod1, prod2, prod3])
    session.commit()

    # Compatibilidades
    comp = Compatibilidad(producto_id=prod2.id, compatible_con=prod3.id, descripcion="Taladro compatible con tornillo 1/4 para fijaciones")
    session.add(comp)
    session.commit()

    # Compras (entradas)
    compra1 = Compra(producto_id=prod1.id, proveedor_id=p1.id, cantidad=20, costo_total=500000)
    compra2 = Compra(producto_id=prod2.id, proveedor_id=p2.id, cantidad=10, costo_total=2000000)
    session.add_all([compra1, compra2])
    session.commit()
    session.close()
    print("Seed de datos completada.")
