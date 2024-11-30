# PyDSL

PyDSL is a FastAPI based application that allows users to execute python code with HTTP calls.

## Installation

To install the project, you can use Docker. Ensure you have Docker installed on your machine.

1. Clone the repository:

    ```sh
    git clone https://github.com/GustasG/PyDSL.git
    cd PyDSL
    ```

2. Build and run the Docker container:

    ```sh
    docker-compose up --build
    ```

## Usage

Once the application is running, you can interact with it using HTTP requests.

Go to /docs to review swagger documentation about the project

## Running tests

To run the tests, use the following command:

```sh
uv run pytest tests
```
