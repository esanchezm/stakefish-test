# Stakefish take-home exercise by Esteban Sánchez

Hello 👋, this is the code I wrote for the take-home test for Stakefish. If you're a reviewer, please let me start by saying thank you, as I had fun writing it. Please check the commits along with this README file to understand my way of thinking and approach.

This README file is important because I try to express my way of thinking and how I manage tasks. If you only focus on evaluating my code, you may get a wrong idea about me. The work I write may not be perfect, lacking types, exception handling, and many other things. Also, the object abstraction could be improved and different. I know how to do all of these, but I focused on getting the result. We could discuss these things if you want to review my test with me 🧑🏻‍💻


## Kicking off 🦵

Normally, my language of choice for writing APIs and tools is Python. I'm learning Go and have already written some code that's publicly available. However, I still don't feel knowledgeable enough to write an API, and it would probably take too long to achieve something. For that reason, I'll do the coding exercise with Python.

This is an API, so I think FastAPI is probably the library of choice. It will allow me to focus on writing the code and leave other things like access logs to middlewares or plugins.

I need a good environment, so I'm going to choose [PDM](https://pdm-project.org/latest/) for Python dependencies and management. This is also an amazing tool for this kind of application.


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

With pre-commit, I can create very basic hooks to manage code consistency. Check the `.pre-commit-config.yaml` file for more.

Let's make our initial commit! 🌟

## First endpoint `/` 1️⃣

This is a good starting point. All I need is the basic FastAPI application with a GET route to `/`. There are two basic aspects here:

1. Getting the app version

Using the `metadata` package or reading the `pyproject.toml` file, I created a function `get_version()` to handle it.

2. Checking if it's running in k8s or not

There are many ways that could be complex, but maybe checking for some environment variables is more than enough. So I did it with `KUBERNETES_SERVICE_HOST`.

To test it and spin the development environment, I've created a PDM script that can be launched with:

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

There's also an easy `/health` endpoint that I'll leave with a simple JSON `{"status": "up"}` response. I could probably add other checks like database connectivity in the future.

## First application models and structure 🏗️

I'm reading the Swagger files and I see a need for a couple of models: `Address` and `Query`.

> :warning: There's some discrepancy between the README file and the definitions in Swagger. For example, the README file says the endpoints are versioned, but they're not in the OpenAPI definition. Considering you will review the code using automated tools, I assume the valid endpoints are **NOT** versioned. This will help me simplify the code too, but I'm aware of versioning techniques using `prefix` for the route and OOP inheritance for the models and routes.

Considering this is quite a small application, I started with a simple solution and put all routes and models in the same file. I could use a more complex file structure using Python modules, one file per class... but I'll try to focus on an MVP for now. Refactoring code like this shouldn't be too much effort in the early stages, but time is limited too.

I created a `models.py` with `Address` and `Query` classes using `pydantic` to handle the properties. I needed to validate IP addresses, and `pydantic` has `IPv4Address` fields, which is great for this. Query objects have a `list[Address]` in the `addresses` field. Quite a simple structure for now.

## Let's start with the routes 🔀

Okay, let's start with some routers. Again, I'll try to keep it simple for now and put all routers in the same file. I basically see two routers: `/tools` and `/history`. Not sure if that's enough to create two different classes, but I'll do that to create some code structure.

Using the models, I created some methods to `resolve()` a `Query` or to verify if a `ValidateIPRequest` is good or not using `is_valid()`. This way the logic is in the model, and we humbly follow SOLID principles.

With these, I could write basic code to at least provide some endpoints to play around, even if they are dummy tests.

## Persistence 💾

If I want to implement the `/history` endpoint, I need to start thinking about persistence. I think I'll go with PostgreSQL as storage because I prefer it to MySQL.

### Docker and Docker-compose 🚢

At this moment, if I want to use a database, I think I need to start using Docker to help me with development. I'll write a Docker and Docker-compose file.

As for the Dockerfile, I've created a multi-stage image based on [PDM](https://pdm-project.org/latest/usage/advanced/#use-pdm-in-a-multi-stage-dockerfile) documentation. I'm choosing `python:3.12-slim-bookworm` to create a small image to have the latest Python version with bug fixes.

### SQLModel and defining persistence 🧮

FastAPI works really well with [SQLModel](https://sqlmodel.tiangolo.com/), and it works great (with small changes) with what I've done. Honestly, this is all new to me, so I'm trying to make it work...

I wrote a `database.py` to define the db engine and sessions, and also a config.py to handle the connection settings using `pydantic_settings` that allows reading settings using environment variables or `.env` files.

Of course, I needed new libraries:

```bash
pdm add sqlmodel pydantic-settings "psycopg[binary]"
```

### Changes to models 🦾

I was using `BaseModel` from `pydantic` to define the models, and to persist them to a database using SQLModel, I need to use the `SQLModel` base class instead. Fields can be defined the same way, and using `Field()`, I can specify database properties such as primary keys, nullables, or default values.

I wasn't sure if `Address` should be persisted, due to its nature of pure data, but since I already had a model, I decided to do it. The relationship is 1-N for code simplicity, though this should have been N-M because some domains may share IP addresses.

### Changes to routers 🦿

With that in place, all I had to do was create a session in the database and save the objects within a transaction. To follow SQLModel and FastAPI good practices, I'll create a `crud.py` file with the model operations, like `create_query()` and `get_queries_history()`. Doing so, the db session can be injected as a dependency from the controllers.

To have proper responses, it's a good practice to define a better class structure for the `Address` and `Query` classes, so I created `*Base` and `*Output` classes as well. This could be a point where refactoring the models into a better file structure should be considered...

### Manual testing 🧪

With all of that, it's time to do some manual tests and remember to test with basic errors (malformed requests, unknown domains...) to catch some exceptions I may have forgotten. It looks like everything works and I can see data being stored.

However, when I get the `/history` endpoint, I'm getting a validation error. Apparently, SQLModel stores IPv4 addresses with the netmask, but that's not a valid IPv4 address...

```
fastapi.exceptions.ResponseValidationError: 2 validation errors:
  {'type': 'ip_v4_address', 'loc': ('response', 0, 'client_ip'), 'msg': 'Input is not a valid IPv4 address', 'input': '127.0.0.1/32'}
  {'type': 'ip_v4_address', 'loc': ('response', 0, 'addresses', 0, 'ip'), 'msg': 'Input is not a valid IPv4 address', 'input': '142.250.184.174/32'}
```

I found a workaround, and I saw I could fix it by creating an `IPv4AddressType` for SQLAlchemy to use it when storing and retrieving the database value.


## Improvements and missing things ⏫

With the basic implementation now, it's time to add other requirements like logging and metrics.

### Metrics using prometheus

For this I used [Prometheus FastAPI instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)

```bash
pdm add prometheus-fastapi-instrumentator
```

Adding it to the application gives me basic HTTP counters, response time histogram buckets, and Python metrics. That's more than enough, but I believe in custom metrics, so I added a counter metric for the number of queries stored in the database. For that, I created a `count_queries_per_domain()` and a `queries_total()` metric generator under a new `metrics.py` file.

After some more coding to create the Prometheus instrumentator and add the metric, I can get these metrics, among others:

```
# HELP queries_total Number of total queries per domain.
# TYPE queries_total gauge
queries_total{domain="goo.com"} 1.0
queries_total{domain="archive.org"} 1.0
queries_total{domain="stake.fish"} 1.0
queries_total{domain="facebook.com"} 1.0
queries_total{domain="google.com"} 2.0
```

I could add more custom metrics like a counter per `client_ip`, IP addresses per domain...

### Access log 🛂

Another requirement is to have an access log. FastAPI has it out-of-the-box, but I think it's better to have it in a JSON format. Well, I was looking at ways to do it and all I could find were a lot of complexity and [discussions](https://github.com/tiangolo/fastapi/discussions/7457) on GitHub. However, after some testing, I found this [repository](https://github.com/sheshbabu/fastapi-structured-json-logging-demo) on GitHub with a very good example.

It basically needs to define a middleware (created in `middleware.py`) that captures requests and responses to log them using a specific `JSONFormatter` handler.


```
{"message": "Incoming request", "req": {"method": "GET", "url": "http://localhost:3000/health", "client": "127.0.0.1", "user-agent": "curl/8.2.1"}, "res": {"status_code": 200}}
{"message": "Incoming request", "req": {"method": "GET", "url": "http://localhost:3000/history", "client": "127.0.0.1", "user-agent": "curl/8.2.1"}, "res": {"status_code": 200}}
{"message": "Incoming request", "req": {"method": "POST", "url": "http://localhost:3000/tools/lookup", "client": "127.0.0.1", "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}, "res": {"status_code": 200}}

```

### End of the development 🔚

Well, I think this finishes everything regarding functionality and requirements. The next part is the DevOps exercise, where I need to create some CI/CD pipelines. But I have no tests! This is a good moment :smile:

## Creating some tests 🤖

I wrote some basic tests, just to have something for the pipelines.

> :warning: I don't plan on writing an extensive test suite. Please consider this is an exercise and I just want to have something, not everything covered.


I started with a basic test for the `/health` endpoint and I got a deprecation warning for a feature I used, so that's actually quite good because now my code is more modern :tada:

I created some tests also for the `/tools/validate` endpoint, which is pretty simple.

At this point, I'm thinking if I should add integration tests using a database. I think I should, but honestly, this is getting bigger and bigger and taking a lot of time. I'm sorry about this.

### CI/CD using github actions 🧑‍🏭

I created a simple `test-and-build.yaml` application to run the test suite and to build the Docker image. It's a 2-job workflow since I wanted to have everything in the same file. Again, for development simplicity and also to avoid building and publishing Docker images whose tests are failing.


The Docker image is published in the GitHub artifact registry and signed using cosign for verification.

I found on the first runs that I was missing some environment variables and also that it would affect me to create a development environment, so I decided to create a `.env-development` file with dummy credentials and also use them in the Docker compose file.

### Helm chart 💹

I started by running `helm create stakefish-test` that will help me with the basic structure of an application, quite enough that I only changed the values to point to the image I deployed and tweak it.

I deleted all unneeded fields from the `values.yaml` file so only the changes I made are there. I disabled `Ingress`, `ServiceAccount` and other things.

> :info: Instead of storing credentials using k8s `Secret`, we should use a external secret provider like [External Secrets](https://external-secrets.io/latest/), so we could store them securely in the cloud provider Secret Manager. To being able to read them, we should limit the nodes IAM role to read them or, even better, create a specific service account bound to an IAM role to access only the application secrets.

The pods will require `imagePullSecrets` so I'm just referencing to a Secret that should be created and managed using External Secrets. I added `ExternalSecret` and `SecretStore` HELM templates just to give an example of it. Values are dummy and needs further resource definitions.

The complexity and security implications could go further, and I just highlighted some details and things to do secure systems. I'm not implementing everything here because there's no specifications about it. What I've done is a basic example that renders like this:

```yaml
---
# Source: stakefish-test/templates/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    kubernetes.io/metadata.name: stakefish-test
  name: stakefish-test
spec:
  finalizers:
  - kubernetes
---
# Source: stakefish-test/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: release-name-stakefish-test
  labels:
    helm.sh/chart: stakefish-test-0.1.0
    app.kubernetes.io/name: stakefish-test
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  ports:
    - port: 3000
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: stakefish-test
    app.kubernetes.io/instance: release-name
---
# Source: stakefish-test/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-name-stakefish-test
  labels:
    helm.sh/chart: stakefish-test-0.1.0
    app.kubernetes.io/name: stakefish-test
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: stakefish-test
      app.kubernetes.io/instance: release-name
  template:
    metadata:
      labels:
        app.kubernetes.io/name: stakefish-test
        app.kubernetes.io/instance: release-name
    spec:
      imagePullSecrets:
        - name: pull-secrets
      securityContext:
        {}
      containers:
        - name: stakefish-test
          securityContext:
            capabilities:
              drop:
              - ALL
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 1000
          image: "ghcr.io/esanchezm/stakefish-test:latest"
          imagePullPolicy: Allways
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            limits:
              cpu: 100m
              memory: 128Mi
            requests:
              cpu: 100m
              memory: 128Mi
---
# Source: stakefish-test/templates/externalsecret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: application-secrets
  namespace: stakefish-test
spec:
  dataFrom:
  - extract:
      key: application-secrets
  refreshInterval: 15m
  secretStoreRef:
    kind: SecretStore
    name: stakefish-secret-store
  target:
    creationPolicy: Owner
    deletionPolicy: Retain
    name: application-secrets
---
# Source: stakefish-test/templates/externalsecret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: pull-secrets
  namespace: stakefish-test
spec:
  dataFrom:
  - extract:
      key: pull-secrets
  refreshInterval: 15m
  secretStoreRef:
    kind: SecretStore
    name: stakefish-secret-store
  target:
    creationPolicy: Owner
    deletionPolicy: Retain
    name: pull-secrets
---
# Source: stakefish-test/templates/secretstore.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name:
  namespace: stakefish-test
spec:
  provider:
    gcpsm:
      auth:
        workloadIdentity:
          serviceAccountRef:
            name: node-sa

```

### Publish helm package 🍡

Since I'm already publishing the Docker image to ghcr.io, I think I could use the [chart-releaser-action](https://github.com/helm/chart-releaser-action) to publish it using Github pages. I created a github action to do that.

```bash
helm repo add stakefish-test https://esanchezm.github.io/stakefish-test/
helm repo update
```

> :info: The repo is private and that doesn't work as you need to use Github credentials to access the page

## Missing things 🤔

Here's a list of things to consider but I didn't do due to lack of time

- Refactor the code to put models in a subdirectory
- Document Helm chart
- Added tests for Helm chart and kubeval to verify the output against different k8s APIs
- Publish it to Artifact Hub or OCI compatible artifact repository

## Wrapping up and personal notes 😃

:pray: Thanks for the opportunity.

Honestly, this was a big test, creating a API with just so little information was a bit challenging. And well, I think this should be a more DevOps oriented test since the only things I've done are a couple of Github actions and a Helm chart.

Anyway, I hope this gives you enough information to understand how I work and what I'm capable of. There may have been some mistakes, but I think this is a test for you to see my skills.

Talk to you soon!
Esteban
