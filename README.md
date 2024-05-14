# Stakefish take-home exercise by Esteban Sánchez

Hello 👋 This is the code I wrote for the take-home test for Stakefish. If you're a reviewer, please let me start by saying thank you as I had fun writing it. Please, check the commits along with this README file to understand my way of thinking and approach.

This README file is important because I try to express my way of thinking and to manage tasks. If you only focus on evaluating my code you may get a wrong idea about me. The work I write may not be perfect, lacking types, exception handling and many other things. Also the object abstraction could be improved and different I know how to do all of them, but I focused on getting the result. We could discuss on these things if you want to review my test with me 🧑🏻‍💻

## Kicking off 🦵

Normally my language of choice for writing APIs and tools is Python. I'm learning Go and I've already been writing some code that's publicly available. However I still don't feel with enough knowledge to write an API and it would probably take too long to achieve something. For that reason, I'll do the coding exercise with Python.

This is an API, so I think FastAPI is probably the library of choice to do so. It will allow me to focus on writing the code and leave other things like access logs to middlewares or plugins.

I need a good environment, so I'm going to choose [PDM](https://pdm-project.org/latest/) for Python dependencies and management. This is also an amazing tool for this kind of applications.

```bash
pdm init
pdm venv create
pdm venv activate
pdm add fastapi uvicorn metadata toml
```

And some development libraries too:

```bash
pdm add -dG dev pre-commit pytest black isort flake8
```

With pre-commit I can create a very basic hooks to manage code consistency. Check `.pre-commit-config.yaml` file for more.

Let's make our initial commit! 🌟

## First endpoint `/`

This is a good starting point. All I need is the basic FastAPI application with a GET route to `/`. There are 2 basic aspects here:

1. getting the app version

By using `metadata` package or reading the `pyproject.toml` file. I created a function `get_version()` to handle it.

2. and if it's running in k8s or not.

There are many ways that could be complex, but maybe checking for some env variables is more than enough. So I did it with `KUBERNETES_SERVICE_HOST`

To test it and spin the development environment, I've created a PDM script and it can be launched with:

```bash
pdm uvicorn
```

And it works:

```bash
❯ curl localhost:3000 -s |jq
{
  "version": "0.1.0",
  "date": 1715591667.0477376,
  "kubernetes": false
}
```

There's also an easy `/health` endpoint that I'll leave it with a simple JSON `{"status": "up"}` response. I could probably add other checks like database connectivity in the future.

## First application models and structure

I'm reading the swagger files and I see a need a couple of models: `Address` and `Query`.

> :warning: There's some discrepancy between the README file and the definitions in swagger. For example, the README file says the endpoints are versioned, but they're not in the OpenAPI definition. Considering you will review the code using automated tools, I assume the valid endpoints are **NOT** versioned. This will help me simplifying the code too, but I'm aware of versioning techniques using `prefix` for the route and OOP inheritance for the models and routes.

Considering this is a quite small application I started with a simple solution and put all routes and models in the same file. I could use a more complex file structure using Python modules, one file per class... but I'll try to focus on a MVP for now. Refactoring a code like this shouldn't be too much effort on early stages, but time is limited too.

I created a `models.py` with `Address` and `Query` classes using `pydantic` to handle the properties. I needed to validate IP Adresses and `pydantic` has `IPv4Address` fields, which is great for this. `Query` objects have a `list[Address]` in the `addresses` field. Quite simple structure for now.

## Let's start with the routes

Okay, let's start with some routers. Again, I'll try to keep it simple for now and put all routers in the same file. I basically see two routers: `/tools` and  `/history`, not sure if that's enough to create two different classes but I'll do that to create some code structure.

Using the models I created some methods to `resolve()` a `Query` or to verify if a `ValidateIPRequest` is good or nod using `is_valid()`. This way the logic is in the model and we humblely follow SOLID principles.

With these I could write basic code to at least provide some endpoints to play around even if they are dummy tests.

## Persistence

If I want to implement the `/history`, I need to start thinking about persistence. I think I'll go with PostgreSQL as a storage because I prefer it to MySQL.

### Docker and Docker-compose

At this moment and if I want to use a database, I think I need to start using docker to help me developing I'll write a Docker and docker-compose

As for the Dockerfile, I've created a multistaging image and based on [PDM](https://pdm-project.org/latest/usage/advanced/#use-pdm-in-a-multi-stage-dockerfile) documentation. I'm choosing `python:3.12-slim-bookworm` to create a small to have the lastest Python version with bugfixes and quite a small image.

### SQLModel and defining persistence

FastAPI works really well with [SQLModel](https://sqlmodel.tiangolo.com/) and it works great (with small changes) with what I've done. Honestly this is all new to me, so I'm trying to make it work...

I wrote a `database.py` to define the db engine and sessions and also a `config.py` to handle the connection settings using `pydantic_settings` that allows to read settings using environment variables or `.env` files.

Of course, I needed new libraries:

```bash
pdm add sqlmodel pydantic-settings "psycopg[binary]"
```
