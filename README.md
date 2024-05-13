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
