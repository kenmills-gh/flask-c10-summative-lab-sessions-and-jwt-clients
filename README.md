# Secure Notes API

## Description
A secure Flask RESTful API backend for a productivity Notes application. It features full session-based authentication, password hashing with bcrypt, and complete protected CRUD operations for user-owned notes.

## Installation Instructions
1. Clone the repository.
2. Run `pipenv install` to install dependencies.
3. Run `pipenv shell` to enter the virtual environment.
4. Run migrations:
   - `flask db init`
   - `flask db migrate -m "Initial migration"`
   - `flask db upgrade`
5. Seed the database: `python seed.py`

## Run Instructions
Start the server by running: `python app.py` 
The API will run on `http://127.0.0.1:5555`.
Switch to a new terminal and run the commands below:
```bash
   cd client-with-sessions
   npm install
   npm start
```
The application will open in your browser at http://localhost:4000 and is set up to proxy

## API Endpoints
* **POST `/signup`**: Registers a new user.
* **POST `/login`**: Authenticates a user and starts a session.
* **DELETE `/logout`**: Ends the user session.
* **GET `/check_session`**: Returns the currently logged-in user.
* **GET `/notes`**: Retrieves a paginated list of notes for the logged-in user (Params: `page`, `per_page`).
* **POST `/notes`**: Creates a new note.
* **PATCH `/notes/<id>`**: Updates a specific note.
* **DELETE `/notes/<id>`**: Deletes a specific note.