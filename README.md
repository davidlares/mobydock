# MobyDock Project

This project (repository) its a Flask application that connects to Redis and PostgreSQL in a containerized way

The main goal of this demo project is to find a way to import a simple web-based project to containers and empathize around
of the basic concepts about the Docker Engine and the Docker Compose built-in tool.

The project contains, 3 directory structure where:

1. `config` - contains services secrets and environment settings
2. `instance` - intended production settings (used by flask configuration object)
3. `mobydock` - app core file, with templates and static assets


## Dependencies

Check the `requirements.txt` file to details.

You probably will need to update certain packages.

## Usage

Assuming you have `docker` and the `docker-compose` already installed. You will need to start the `docker-compose up`

In parallel you need to create the `modydock` database example, using the `docker-compose` process and the PostgreSQL `createDB` command according to the `PostgreSQL` container, like this.

`docker exec mobydock_postgres_1 createdb -U postgres mobydock`

And then:

`docker exec psql -U postgres -c "CREATE USER mobydock WITH PASSWORD '12346578'; GRANT ALL PRIVILEGES ON DATABASE mobydock to mobydock"`

The password `12345678` and `mobydock` for user and database name should match with the PostgreSQL string connection.

## Credits

 - [David E Lares](https://twitter.com/davidlares3)

## License

 - [MIT](https://opensource.org/licenses/MIT)
