POST_SCHEMAS = {
    "drivers": {
        "type": "object",
        "title": "New driver creation schema",
        "default": {},
        "examples": [{"name": "Ivan Ivanov", "car": "Honda Civic"}],
        "required": ["name", "car"],
        "additionalProperties": False,
        "properties": {
            "name": {
                "description": "Driver's name",
                "type": "string",
            },
            "car": {
                "description": "Driver's car",
                "type": "string",
            }
        },
    },
    "clients": {
        "type": "object",
        "title": "New client creation schema",
        "default": {},
        "examples": [{"name": "Ivan Ivanov", "is_vip": True}],
        "required": ["name", "is_vip"],
        "additionalProperties": False,
        "properties": {
            "name": {
                "description": "Client's name",
                "type": "string",
            },
            "is_vip": {
                "description": "Is client VIP?",
                "type": "boolean",
            }
        },
    },
    "orders": {
        "type": "object",
        "title": "New order creation schema",
        "default": {},
        "examples": [
            {
                "client_id": 0,
                "driver_id": 0,
                "date_created": "2021-08-23T06:31:08.716Z",
                "status": "not_accepted",
                "address_from": "Address",
                "address_to": "Another address",
            }
        ],
        "required": ["client_id", "driver_id", "date_created",
                     "status", "address_from", "address_to"],
        "additionalProperties": False,
        "properties": {
            "client_id": {
                "description": "Client's identifier",
                "type": "integer",
            },
            "driver_id": {
                "description": "Driver's identifier",
                "type": "integer",
            },
            "address_from": {
                "description": "Starting address",
                "type": "string",
            },
            "address_to": {
                "description": "Destination address",
                "type": "string",
            },
            "date_created": {
                "description": "Date of order creation",
                "type": "string",
                "format": "date-time",
            },
            "status": {
                "description": "Order status",
                "type": "string",
                "enum": [
                    "not_accepted",
                    "in_progress",
                    "done",
                    "cancelled",
                ],
            },
        },
    },
}
