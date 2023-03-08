import logging

from flask import (
    jsonify,
    make_response,
    request,
)
from marshmallow import (
    fields,
    Schema,
    ValidationError,
)

from challenge_halo.redis_utils import RedisUtils


def configure_routes(app):

    class PushQueueBodySchema(Schema):
        key = fields.Str()
        value = fields.Str()

    class PopQueueBodySchema(Schema):
        key = fields.Str()

    redis_utilities = RedisUtils()

    @app.route("/api/queue/push", methods=["POST"])
    def push_queue():
        """
        Receives key value through a json in the http body
        if json contains ONLY a key value it will try store it in redis, else will return a 400
        """
        body = request.get_json(force=True, silent=True)
        schema = PushQueueBodySchema()
        try:
            # Validate request body against schema data types
            schema.load(body)
            if redis_utilities.set(body["key"], body["value"]):
                message = {
                    "status": "ok"
                }
                status_code = 200
            else:
                message = {
                    "status": "error",
                    "message": f"key: {body['key']} already exists"
                }
                status_code = 400
        except ValidationError as err:
            message = {
                "status": "error",
                "message": err.messages,
            }
            status_code = 400

        return make_response(jsonify(message), status_code)

    @app.route("/api/queue/pop", methods=["POST"])
    def pop_queue_by_key():
        """
        Deletes a redis key specified in the request body,
        Returns 200 http status code if the operation is succesful and 400 if the key passed doesn't exist
        """
        body = request.get_json(force=True, silent=True)
        logging.debug(body)
        schema = PopQueueBodySchema()
        try:
            # Validate request body against schema data types
            schema.load(body)
            if redis_utilities.get_and_delete_key(body["key"]):
                message = {
                    "status": "ok",
                    "message": f"Key: {body['key']} deleted succesfully",
                }
                status_code = 200
            else:
                message = {
                    "status": "error",
                    "message": f"Key: {body['key']} doesn't exist",
                }
                status_code = 200
        except ValidationError as err:
            message = {
                "status": "error",
                "message": err.messages,
            }
            status_code = 400

        return make_response(jsonify(message), status_code)

    @app.route("/api/queue/count", methods=["GET"])
    def get_queue_size():
        """
        Gets total number of keys in redis.
        Returns 200 if operation is succesful and 500 if there was an issue.
        """
        total_keys = redis_utilities.db_size()
        if total_keys > -1:
            status_code = 200
            logging.debug(f"{total_keys} total keys")
            message = {
                "status": "ok",
                "count": f"{total_keys}",
            }
        else:
            status_code = 500
            message = {
                "status": "error",
            }
        return make_response(jsonify(message), status_code)

    @app.route("/api/queue/health", methods=["GET"])
    def check_queue_health():
        """
        Returns latest redis healthcheck and total uptime measured by the web server.
        """
        if redis_utilities.check_health():
            message = {
                "status": "ok",
                "total redis uptime": f"{redis_utilities.get_total_uptime()} hours"
            }
            status_code = 200
        else:
            message = {
                "status": "error",
                "message": "There is an issue with redis",
                "total redis uptime": f"{redis_utilities.get_total_uptime()} hours",
            }
            status_code = 500
        return make_response(jsonify(message), status_code)
