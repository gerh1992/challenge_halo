# Challenge halo
This repo contains a simple api server to interact with a message queue that uses redis, [design instructions](instructions.txt)

### Prerequisites
[Docker](https://docs.docker.com/engine/install/)

### Installation
1. Clone the repo
```bash
git clone git@github.com:gerh1992/challenge_halo.git
```
2. Change directory to the application code
```bash
cd challenge_halo
```
3. Spin up the application & redis
```bash
make run
```

### Usage
The application has endpoints to handle:
 - pushing key values on the message queue
 - popping keys on the message queue
 - returning total keys stored
 - Returning health status and total uptime of the queue 

 There are some examples using `curl` to see how those endpoints behave under [examples.sh](examples.sh)

##### Configuring the app to use an external redis 
The application uses environment variables to connect to redis, so if it needs to change where to connect to its a matter of tuning the variables:
 - `FLASK_REDIS_HOST`
 - `FLASK_REDIS_PORT`
 - `FLASK_REDIS_PASSWORD`


### Development

##### Running tests
```bash
make test
```

##### Rebuilding application
```bash
make build
```


