from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, ForeignKey, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils.types.choice import ChoiceType


engine = create_engine('postgresql://postgres:91738246@localhost:5432/onyx_taxi')
Base = declarative_base()


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, autoincrement=True,
        comment="Идентификатор водителя")
    name = Column(String(50), nullable=False, comment="Имя водителя")
    car = Column(String(50), nullable=False, comment="Автомобиль водителя")

    def __repr__(self):
        return f"Водитель: {self.name}, автомобиль: {self.car}"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True,
        comment="Идентификатор клиента")
    name = Column(String(50), nullable=False, comment="Имя клиента")
    is_vip = Column(Boolean, default=False, nullable=False,
                    comment="Является ли клиент VIP")

    def __repr__(self):
        return f"Клиент: {self.name}({'Vip' if self.is_vip else 'not Vip'})"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True,
        comment="Идентификатор поездки")
    address_from = Column(String(100), nullable=False, comment="Адрес посадки")
    address_to = Column(String(100), nullable=False, comment="Адрес высадки")
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False,
        comment="Идентификатор клиента")
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False,
        comment="Идентификатор водителя")
    date_created = Column(DateTime(timezone=True), default=func.now(),
        comment="Дата и время создания заказа")
    status = Column(
        ChoiceType(
            [
                ("not_accepted", "not_accepted"),
                ("in_progress", "in_progress"),
                ("done", "done"),
                ("cancelled", "cancelled")
            ], impl=String()
        ),
        nullable=False, comment="Статус поездки"
    )
    clients = relationship("Client", foreign_keys=[client_id])
    drivers = relationship("Driver", foreign_keys=[driver_id])
