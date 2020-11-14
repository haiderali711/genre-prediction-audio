
## How to create Docker container: 

1. You should have Docker installed. 
    ```bash
	# Run the following to create a docker Image 

    	docker build -t djangoapp .
	
	# Run the following to start the Web app from a docker container 

	docker run -p 8000:8000 -i -t djangoapp  
	
	#Open the following link in the browser to access the application 
	
	http://localhost:8000
    ```

