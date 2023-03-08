from challenge_halo.redis_utils import RedisUtils
import json


def data_to_dict(data):
    # Helper to decode data from binary to a python dict
    return json.loads(data.decode())


def test_health_endpoint(client):
    url = "/api/queue/health"
    response = client.get(url)
    response_data = data_to_dict(response.data)
    assert "status" in response_data.keys()
    assert "ok" == response_data["status"]


def test_push_queue_endpoint_ok(client):
    url = "/api/queue/push"

    mock_request_data = {
        "key": 'asd',
        "value": "asdasd",
    }

    response = client.post(url, data=json.dumps(mock_request_data))
    assert response.status_code == 200


def test_push_queue_endpoint_error(client):
    url = "/api/queue/push"

    mock_request_data = {
        "wrong schema": "asdksadsa",
    }

    response = client.post(url, data=json.dumps(mock_request_data))
    assert response.status_code == 400


def test_pop_queue_endpoint_key_doesnt_exist(client):
    url = "/api/queue/pop"
    mock_request_data = {
        "key": "asd",
    }
    response = client.post(url, data=json.dumps(mock_request_data))
    response_data = data_to_dict(response.data)
    expected_output = {
        "message": f"Key: {mock_request_data['key']} doesn't exist",
        "status": "error"
    }
    assert expected_output == response_data


def test_count_endpoint(client):
    url = "/api/queue/count"
    redis_utilities = RedisUtils()
    # Adding 10 items to redis, then making sure the total count returns 10
    for i in range(10):
        redis_utilities.set(key=str(i), value=str(i))

    expected_output = {
        "count": "10",
        "status": "ok",
    }
    response = client.get(url)
    response_data = data_to_dict(response.data)
    assert response_data == expected_output
