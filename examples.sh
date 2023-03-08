# Sample request to push endpoint
curl -X POST http://localhost:5000/api/queue/push \\
    --verbose -d '{"key": "some_key", "value":"some_value"}'

# Sample request to pop endpoint
curl -X POST http://localhost:5000/api/queue/pop \\
    --verbose -d '{"key": "some_key"}'

# Sample request to count endpoint
curl -X POST http://localhost:5000/api/queue/count --verbose

# Sample request to health endpoint
curl http://localhost:5000/api/queue/health --verbose
