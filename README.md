# AccessVerifier microservice

This is a simple project containing source code for the Access Verifier microservice.\
General idea behind this project is to check the list of AWS IP addresses daily and allow or deny access to other services if the IP is on the list.

## Application

Application is written in Python. For better management of dependencies, we're using Poetry to keep them in one place.
You can find them in `app\pyproject.toml` file\
The source code for the app is under `app\python` folder.\
You can extend the project by adding some unit tests into `app\test` directory.


## Docker

Application is designed to run as a microservice in a Docker container.
To build the image, simply run:
```
docker build -t access-verifier:<YOUR_TAG> .
```

## Helm

We're also providing basic Helm Chart if you want to deploy the app to your Kubernetes cluster.
In such case, use following command:

```
helm upgrade --install access-verifier ./helm --namespace default
```

Helm is not required to run the app, you can host the app on any orchestrator you want, but it simplifies solution if you're using Kubernetes.

## CI-CD

The project lacks the configuration of CI-CD tool, which might be helpful in the future to automate changes and deployment of the app. If you're using Jenkins, you can always create here simple `Jenknisfile`, which would be source of truth for your pipeline in which you'd add steps for testing the app, building the image and deploying it to K8S using Helm.