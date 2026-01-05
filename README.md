# To-Do-App
A Demo To Do app using claude code where Frontend is build on React js and Backend is build on FastApi Python.


## To-Do App

Created a to do app with claude code using React js for the frontend and python FastApi for the backend.

~~user can create a todo~~
~~user can edit a todo~~
~~user can delete a todo~~
~~user can priortise a todo~~
~~user can mark todo as compeleted~~
~~user can mark todo as failure~~


**for running the application backend**
Go the backend folder and create a virtual environment using uv and than run the backend using uv
you can use the following commands
``` 
cd backend
uv sync
uv run python -m app.main
```

your application will run on

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

**for running application frontend**
Go the frontend install the package using npm and run the application frontend using npm
you can use the following commands
```
cd frontend
npm install 
npm run dev
```

your application frontend will run on 

[http://localhost:5173/](http://localhost:5173/)


## Run applicaiton using docker

```
  # Build and start all services
  docker-compose up --build

  # Or run in detached mode (background)
  docker-compose up --build -d

  Other useful commands:

  # Stop all services
  docker-compose down

  # View logs
  docker-compose logs -f

  # View logs for specific service
  docker-compose logs -f backend
  docker-compose logs -f frontend

  # Restart services
  docker-compose restart

  # Rebuild specific service
  docker-compose build backend
  docker-compose build frontend

  # Remove all containers, volumes, and networks
  docker-compose down -v

  After running docker-compose up --build, your application will be available at:
  - Frontend: http://localhost
  - Backend API: http://localhost:8000
  - API docs: http://localhost:8000/docs
  ```