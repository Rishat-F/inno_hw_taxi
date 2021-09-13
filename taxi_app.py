import json
from typing import Any, Union

from flask import Flask, request, Response
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import jsonschema
from jsonschema.exceptions import ValidationError

from taxi_db import engine, Base, Driver, Client, Order
from validations import POST_SCHEMAS


SUPER_DRIVER = -404
SUPER_CLIENT = -404


class SuperDriverError(Exception):
    """Raise error when trying to delete SuperDriver with id -404."""

    pass


class SuperClientError(Exception):
    """Raise error when trying to delete SuperClient with id -404."""

    pass


Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope() -> Any:
    """Open session for working with DataBase."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


app = Flask(__name__)


@app.route("/")
def hello_world() -> tuple:
    """Index GET-requests handler."""
    return "<p>Welcome to the Onyx.Taxi!</p>", 200


@app.route("/drivers", methods=["POST"])
def post_driver() -> Response:
    """POST-requests handler for creating new driver."""
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["drivers"])
        except ValidationError:
            return Response("Unsupported Media Type", status=415, mimetype="text/html")
        else:
            try:
                with session_scope() as session:
                    new_driver = Driver(name=content["name"], car=content["car"])
                    session.add(new_driver)
                    added_driver = (
                        session.query(Driver)
                        .filter(
                            Driver.name == content["name"], Driver.car == content["car"]
                        )
                        .all()[-1]
                    )
                    response_data = {
                        "id": added_driver.id,
                        "name": added_driver.name,
                        "car": added_driver.car,
                    }
                    return Response(
                        json.dumps(response_data),
                        status=201,
                        mimetype="application/json",
                    )
            except Exception:
                return Response(
                    "Internal Server Error", status=500, mimetype="text/html"
                )
    else:
        return Response("Bad request", status=400, mimetype="text/html")


@app.route("/clients", methods=["POST"])
def post_client() -> Response:
    """POST-requests handler for creating new client."""
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["clients"])
        except ValidationError:
            return Response("Unsupported Media Type", status=415, mimetype="text/html")
        else:
            try:
                with session_scope() as session:
                    new_client = Client(name=content["name"], is_vip=content["is_vip"])
                    session.add(new_client)
                    added_client = (
                        session.query(Client)
                        .filter(
                            Client.name == content["name"],
                            Client.is_vip == content["is_vip"],
                        )
                        .all()[-1]
                    )
                    response_data = {
                        "id": added_client.id,
                        "name": added_client.name,
                        "is_vip": added_client.is_vip,
                    }
                    return Response(
                        json.dumps(response_data),
                        status=201,
                        mimetype="application/json",
                    )
            except Exception:
                return Response(
                    "Internal Server Error", status=500, mimetype="text/html"
                )
    else:
        return Response("Bad request", status=400, mimetype="text/html")


@app.route("/orders", methods=["POST"])
def post_order() -> Response:
    """POST-requests handler for creating new order."""
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["orders"])
        except ValidationError:
            return Response("Unsupported Media Type", status=415, mimetype="text/html")
        else:
            try:
                with session_scope() as session:
                    new_order = Order(
                        address_from=content["address_from"],
                        address_to=content["address_to"],
                        client_id=content["client_id"],
                        driver_id=content["driver_id"],
                        date_created=content["date_created"],
                        status=content["status"],
                    )
                    session.add(new_order)
                    added_order = (
                        session.query(Order)
                        .filter(
                            Order.client_id == content["client_id"],
                            Order.driver_id == content["driver_id"],
                            Order.date_created == content["date_created"],
                        )
                        .all()[-1]
                    )
                    response_data = {
                        "id": added_order.id,
                        "client_id": added_order.client_id,
                        "driver_id": added_order.driver_id,
                        "date_created": added_order.date_created,
                        "status": added_order.status,
                        "address_from": added_order.address_from,
                        "address_to": added_order.address_to,
                    }
                    return Response(
                        json.dumps(response_data),
                        status=201,
                        mimetype="application/json",
                    )
            except Exception:
                return Response(
                    "Internal Server Error", status=500, mimetype="text/html"
                )
    else:
        return Response("Bad request", status=400, mimetype="text/html")


@app.route("/drivers", methods=["GET"])
def get_driver_by_id() -> Response:
    """GET-requests handler for get driver by id."""
    try:
        driver_id = int(request.args["driver_id"])
        if driver_id == SUPER_DRIVER:
            raise SuperDriverError("Super Driver is untouchable!")
    except (SuperDriverError, Exception):
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            driver = session.query(Driver).filter(Driver.id == driver_id).all()
            if driver:
                [driver] = driver
                response_data = {
                    "id": driver.id,
                    "name": driver.name,
                    "car": driver.car,
                }
                return Response(
                    json.dumps(response_data), status=200, mimetype="application/json"
                )
            else:
                return Response("Driver not found", status=404, mimetype="text/html")
    except Exception:
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/clients", methods=["GET"])
def get_client_by_id() -> Response:
    """GET-requests handler for get client by id."""
    try:
        client_id = int(request.args["client_id"])
        if client_id == SUPER_CLIENT:
            raise SuperClientError("Super Client is untouchable!")
    except (SuperClientError, Exception):
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            client = session.query(Client).filter(Client.id == client_id).all()
            if client:
                [client] = client
                response_data = {
                    "id": client.id,
                    "name": client.name,
                    "is_vip": client.is_vip,
                }
                return Response(
                    json.dumps(response_data), status=200, mimetype="application/json"
                )
            else:
                return Response("Client not found", status=404, mimetype="text/html")
    except Exception:
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/orders", methods=["GET"])
def get_order_by_id() -> Response:
    """GET-requests handler for get order by id."""
    try:
        order_id = int(request.args["order_id"])
    except Exception:
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            order = session.query(Order).filter(Order.id == order_id).all()
            if order:
                [order] = order
                response_data = {
                    "id": order.id,
                    "client_id": order.client_id,
                    "driver_id": order.driver_id,
                    "date_created": str(order.date_created),
                    "status": str(order.status),
                    "address_from": order.address_from,
                    "address_to": order.address_to,
                }
                return Response(
                    json.dumps(response_data), status=200, mimetype="application/json"
                )
            else:
                return Response("Order not found", status=404, mimetype="text/html")
    except Exception:
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/drivers/<driver_id>", methods=["DELETE"])
def delete_driver_by_id(driver_id: Union[str, int]) -> Response:
    """DELETE-requests handler for delete driver by id."""
    try:
        driver_id = int(driver_id)
        if driver_id == SUPER_DRIVER:
            raise SuperDriverError("Super Driver is untouchable!")
    except (SuperDriverError, Exception):
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            query_to_delete = session.query(Driver).filter(Driver.id == driver_id)
            driver_to_delete = query_to_delete.all()
            if driver_to_delete:
                [driver_to_delete] = driver_to_delete
                response_data = {
                    "id": driver_to_delete.id,
                    "name": driver_to_delete.name,
                    "car": driver_to_delete.car,
                }
                query_to_delete.delete()
                return Response(
                    json.dumps(response_data), status=200, mimetype="application/json"
                )
            else:
                return Response("Driver not found", status=404, mimetype="text/html")
    except Exception:
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/clients/<client_id>", methods=["DELETE"])
def delete_client_by_id(client_id: Union[str, int]) -> Response:
    """DELETE-requests handler for delete client by id."""
    try:
        client_id = int(client_id)
        if client_id == SUPER_CLIENT:
            raise SuperClientError("Super Client is untouchable!")
    except (SuperClientError, Exception):
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            query_to_delete = session.query(Client).filter(Client.id == client_id)
            client_to_delete = query_to_delete.all()
            if client_to_delete:
                [client_to_delete] = client_to_delete
                response_data = {
                    "id": client_to_delete.id,
                    "name": client_to_delete.name,
                    "is_vip": client_to_delete.is_vip,
                }
                query_to_delete.delete()
                return Response(
                    json.dumps(response_data), status=200, mimetype="application/json"
                )
            else:
                return Response("Client not found", status=404, mimetype="text/html")
    except Exception:
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/orders/<order_id>", methods=["PUT"])
def update_order_by_id(order_id: Union[str, int]) -> Response:
    """PUT-requests handler for update order by id."""
    try:
        order_id = int(order_id)
    except Exception:
        return Response("Bad request", status=400, mimetype="text/html")
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["orders"])
        except ValidationError:
            return Response("Unsupported Media Type", status=415, mimetype="text/html")
        else:
            try:
                with session_scope() as session:
                    order_to_update = (
                        session.query(Order).filter(Order.id == order_id).all()
                    )
                    if order_to_update:
                        session.query(Order).filter(Order.id == order_id).update(
                            content
                        )
                        updated_order = (
                            session.query(Order).filter(Order.id == order_id).all()
                        )
                        [updated_order] = updated_order
                        response_data = {
                            "id": updated_order.id,
                            "client_id": updated_order.client_id,
                            "driver_id": updated_order.driver_id,
                            "date_created": updated_order.date_created,
                            "status": updated_order.status,
                            "address_from": updated_order.address_from,
                            "address_to": updated_order.address_to,
                        }
                        return Response(
                            json.dumps(response_data),
                            status=200,
                            mimetype="application/json",
                        )
                    else:
                        return Response(
                            "Order not found", status=404, mimetype="text/html"
                        )
            except Exception as err:
                print(err)
                return Response(
                    "Internal Server Error", status=500, mimetype="text/html"
                )
    else:
        return Response("Bad request", status=400, mimetype="text/html")


if __name__ == "__main__":
    app.run()
