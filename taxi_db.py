from typing import Any

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType


engine = create_engine("postgresql://postgres:91738246@localhost:5432/onyx_taxi")
Base: Any = declarative_base()


class Driver(Base):
    """Define drivers table in DataBase."""

    __tablename__ = "drivers"

    id = Column(
        Integer, primary_key=True, autoincrement=True, comment="Идентификатор водителя"
    )
    name = Column(String(50), nullable=False, comment="Имя водителя")
    car = Column(String(50), nullable=False, comment="Автомобиль водителя")


class Client(Base):
    """Define clients table in DataBase."""

    __tablename__ = "clients"

    id = Column(
        Integer, primary_key=True, autoincrement=True, comment="Идентификатор клиента"
    )
    name = Column(String(50), nullable=False, comment="Имя клиента")
    is_vip = Column(
        Boolean, default=False, nullable=False, comment="Является ли клиент VIP"
    )


class Order(Base):
    """Define orders table in DataBase."""

    __tablename__ = "orders"

    id = Column(
        Integer, primary_key=True, autoincrement=True, comment="Идентификатор поездки"
    )
    address_from = Column(String(100), nullable=False, comment="Адрес посадки")
    address_to = Column(String(100), nullable=False, comment="Адрес высадки")
    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="SET DEFAULT"),
        nullable=False,
        server_default="-404",
        comment="Идентификатор клиента",
    )
    driver_id = Column(
        Integer,
        ForeignKey("drivers.id", ondelete="SET DEFAULT"),
        nullable=False,
        server_default="-404",
        comment="Идентификатор водителя",
    )
    date_created = Column(
        DateTime, nullable=False, comment="Дата и время создания заказа"
    )
    status = Column(
        ChoiceType(
            [
                ("not_accepted", "not_accepted"),
                ("in_progress", "in_progress"),
                ("done", "done"),
                ("cancelled", "cancelled"),
            ],
            impl=String(),
        ),
        nullable=False,
        comment="Статус поездки",
    )
    clients = relationship("Client", foreign_keys=[client_id])
    drivers = relationship("Driver", foreign_keys=[driver_id])
