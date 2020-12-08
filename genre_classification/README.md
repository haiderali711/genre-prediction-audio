# How to create Docker container:

### You should have Docker installed.

```bash
# Run the following to create a docker Image

	docker build -t djangoapp .
```

```bash
# Run the following to start the Web app from a docker container

   	docker run -p 8000:8000 -i -t djangoapp
```

```bash
#Open the following link in the browser to access the application

   	http://localhost:8000
```
