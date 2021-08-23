from flask import Flask, request
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
def post_drivers():
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["drivers"])
        except ValidationError as err:
            return str(err), 415
        else:
            with session_scope() as session:
                new_driver = Driver(
                    name=content["name"],
                    car=content["car"]
                )
                session.add(new_driver)
                return "Created!", 201
    else:
        return "Bad request", 400


@app.route("/clients", methods=["POST"])
def post_clients():
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["clients"])
        except ValidationError as err:
            return str(err), 415
        else:
            with session_scope() as session:
                new_client = Client(
                    name=content["name"],
                    is_vip=content["is_vip"]
                )
                session.add(new_client)
                return "Created!", 201
    else:
        return "Bad request", 400


@app.route("/orders", methods=["POST"])
def post_orders():
    content = request.get_json()
    if content:
        try:
            jsonschema.validate(content, POST_SCHEMAS["orders"])
        except ValidationError as err:
            return str(err), 415
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
                    return "Created!", 201
            except Exception as err:
                print(err)
                return "Internal Server Error", 500
    else:
        return "Bad request", 400


if __name__ == "__main__":
    app.run()
