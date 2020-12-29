# Genre-recognition

## How to create Docker container to run the application:

1. [Install Docker](https://docs.docker.com/get-docker). 
2. `cd` into `genre_classification`.
3. Run the application as follows:
```bash
# Create a docker Image
docker build -t djangoapp .
```

```bash
# Start Web app from a docker container
docker run -p 8000:8000 -i -t djangoapp
```

```bash
# Go to following link in the browser
http://localhost:8000
```

## Libraries used
* numpy
* Django v3.1.3
* joblib
* matplotlib
* pandas
* sqlite3
* scikit-learn
* scipy
* sqlparse
* gunicorn
* librosa
* keras v2.4.3
* tensorflow v2.3.0

## Thanks to
* Tailwind CSS
* Alpine.js
* Chart.js