# Christmas Elves

The annual Christmas Elves game server and client

Python North East December brings you the Christmas Elf Challenge. Your task,
should you choose to accept it, is to collect the most

## Running the Server

### Installing Dependencies

The server is self-contained with an SQLite database, so just install the
requirements:

```bash
pip install -r requirements.txt
```

### Running

We're using Django Channels, so running the server is as easy as:

```bash
python server/manage.py runserver
```

## The API

To interact with the server session, we use a simple REST API to send new data
into the server. The full API docs can be found by running a server and
navigating to `/docs/`.

### Starting a New Session

To start a new session, send a `POST` request with a `name` variable
form-encoded to `https://<host>/sessions/`:

```bash
curl https://example.com/sessions/ -X POST -d player_name="Scott"
```

and you'll get a simple JSON object back with a `session` URL that you post your
turns against.

### Taking a Turn


To take a turn, make a `POST` request against the `day` endpoint of a session.


## Creating Clients

## Instructions and Rules

See the [attached Google Doc](https://docs.google.com/document/d/1p3upVEv7zDcT_0ZQKbJqo_nudHUwIoLAo1TkxzBb7ZA/edit?usp=sharing)
for the rules and any of the latest tips and tricks.
