# Beanstalk Farmer

Beanstalk farmer is designed to be a very simple web-based interface for monitoring the status of pipes in a Beanstalkd install. It's built using Flask and is meant to be run as a standalone application when developing with Beanstalkd.

## Installation

Beanstalk farmer is distributed as a docker image. You can pull the latest version from Docker Hub:

```bash
docker pull tharbakim/beanstalk-farmer:latest
```

## Usage

Once the container has been started, you can access the web interface by navigating to `http://localhost:5000` in your web browser. The interface will display the status of all the tubes in your Beanstalkd instance, including the number of jobs in each tube and their current state.

## Configuration

Beanstalk farmer can be configured using environment variables. The following variables are available:
- `BEANSTALK_HOST`: The hostname or IP address of the Beanstalkd server (default: `localhost`)
- `BEANSTALK_PORT`: The port number of the Beanstalkd server (default: `11300`)
