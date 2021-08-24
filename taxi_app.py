import json

from flask import Flask, request, jsonify, Response
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import jsonschema
from jsonschema.exceptions import ValidationError

from taxi_db import engine, Base, Driver, Client, Order
from validations import POST_SCHEMAS


Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope():
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Welcome to the Onyx.Taxi!</p>", 200


@app.route("/drivers", methods=["POST"])
def post_driver():
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["drivers"])
        except ValidationError as err:
            return Response(str(err), status=415, mimetype="text/html")
        else:
            try:
                with session_scope() as session:
                    new_driver = Driver(
                        name=content["name"],
                        car=content["car"]
                    )
                    session.add(new_driver)
                    added_driver = session.query(Driver).filter(
                        Driver.name==content["name"], Driver.car==content["car"]).all()[-1]
                    response = {"id": added_driver.id, "name": added_driver.name, "car": added_driver.car}
                    return Response(json.dumps(response), status=201, mimetype="application/json")
            except Exception as err:
                print(err)
                return Response("Internal Server Error", status=500, mimetype="text/html")
    else:
        return Response("Bad request", status=400, mimetype="text/html")


@app.route("/clients", methods=["POST"])
def post_client():
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["clients"])
        except ValidationError as err:
            return Response(str(err), status=415, mimetype="text/html")
        else:
            try:
                with session_scope() as session:
                    new_client = Client(
                        name=content["name"],
                        is_vip=content["is_vip"]
                    )
                    session.add(new_client)
                    added_client = session.query(Client).filter(
                        Client.name == content["name"], Client.is_vip == content["is_vip"]).all()[-1]
                    response = {"id": added_client.id, "name": added_client.name, "is_vip": added_client.is_vip}
                    return Response(json.dumps(response), status=201, mimetype="application/json")
            except Exception as err:
                print(err)
                return Response("Internal Server Error", status=500, mimetype="text/html")
    else:
        return Response("Bad request", status=400, mimetype="text/html")


@app.route("/orders", methods=["POST"])
def post_order():
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["orders"])
        except ValidationError as err:
            return Response(str(err), status=415, mimetype="text/html")
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
                    added_order = session.query(Order).filter(
                        Order.client_id == content["client_id"], Order.driver_id == content["driver_id"],
                        Order.date_created==content["date_created"]).all()[-1]
                    response = {
                        "id": added_order.id, "client_id": added_order.client_id, "driver_id": added_order.driver_id,
                        "date_created": added_order.date_created, "status": added_order.status,
                        "address_from": added_order.address_from, "address_to": added_order.address_to
                    }
                    return Response(json.dumps(response), status=201, mimetype="application/json")
            except Exception as err:
                print(err)
                return Response("Internal Server Error", status=500, mimetype="text/html")
    else:
        return Response("Bad request", status=400, mimetype="text/html")


@app.route("/drivers", methods=["GET"])
def get_driver():
    try:
        driver_id = int(request.args["driver_id"])
    except:
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            driver = session.query(Driver).filter(Driver.id==driver_id).all()
            if driver:
                [driver] = driver
                response = {"id": driver.id, "name": driver.name, "car": driver.car}
                return Response(json.dumps(response), status=200, mimetype="application/json")
            else:
                return Response("Driver not found", status=404, mimetype="text/html")
    except Exception as err:
        print(err)
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/clients", methods=["GET"])
def get_client():
    try:
        client_id = int(request.args["client_id"])
    except:
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            client = session.query(Client).filter(Client.id==client_id).all()
            if client:
                [client] = client
                response = {"id": client.id, "name": client.name, "is_vip": client.is_vip}
                return Response(json.dumps(response), status=200, mimetype="application/json")
            else:
                return Response("Client not found", status=404, mimetype="text/html")
    except Exception as err:
        print(err)
        return Response("Internal Server Error", status=500, mimetype="text/html")


@app.route("/orders", methods=["GET"])
def get_order():
    try:
        order_id = int(request.args["order_id"])
    except:
        return Response("Bad request", status=400, mimetype="text/html")
    try:
        with session_scope() as session:
            order = session.query(Order).filter(Order.id==order_id).all()
            if order:
                [order] = order
                response = {
                    "id": order.id, "client_id": order.client_id, "driver_id": order.driver_id,
                    "date_created": str(order.date_created), "status": str(order.status),
                    "address_from": order.address_from, "address_to": order.address_to
                }
                return Response(json.dumps(response), status=200, mimetype="application/json")
            else:
                return Response("Order not found", status=404, mimetype="text/html")
    except Exception as err:
        print(err)
        return Response("Internal Server Error", status=500, mimetype="text/html")


if __name__ == "__main__":
    app.run()
