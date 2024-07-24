1. From terminal run:  "docker-compose up --build"
2. Before register device, at least one user and one location must be registered
3. To register location use post request with url: localhost:8080/location with json={"name": "lacation_name"}
4. To register user use post request with  url: localhost:8080/apiuser with json={"name": "user_name", "email": "user_email", "password": "user_password"}
5. To register device use post request with  url: localhost:8080/device with json={"name": "device_name", "type": "device_type", "login": "dev_login", "password": "user_password","location_id": location_id, "api_user_id": api_user_id}
6. To change location or user or device use pull request with url: localhost:8080/{location/apiuser/device}/{id} with json with changed params
7. To get location or user or device use get request with url: localhost:8080/{location/apiuser/device}/{id}
7. To get all locations or users or devices use get request with url: localhost:8080/{location/apiuser/device}

To stop container: Ctrl+c

To test use command "docker-compose up -d" to run container in background and then run: "docker-compose run --rm web pytest test.py"

To stop background container: "docker-compose down"

To run app from terminal without docker container, it is needed to create database(or use db_creation.py, where database settings must be set in config) and change DataBase settings in models.py
