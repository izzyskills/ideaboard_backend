# Idea Board Backend

this is the backend for the idea board project. It is a simple REST API that allows users to create, read, update, and delete ideas. The API is built using Python, Fastapi, and PostgreSQL. The API is hosted on Heroku and the database is hosted on herokupostgresql. The API is secured using JWT authentication.
ideaboard-11eb55dbd5b9.herokuapp.com

## Features

- Create a new idea
- Read all ideas
- Filter ideas by title and other fields
- Read a single idea
- Update an idea
- Delete an idea
- Create a new user
- Login
- Logout
- Refresh token
- Create a new comment
- Read all comments related to an idea
- like an idea
- dislike an idea
- Read all likes and dislikes related to an idea

## API Endpoints

the api endpoint can be found [here](https://ideaboard-11eb55dbd5b9.herokuapp.com/api/v1/docs) or [here](./api_docs.md)

## Installation

1. Clone the repository

```bash
git clone https://github.com/izzyskills/ideaboard_backend.git
```

2. Change directory to the project directory

```bash
cd ideaboard_backend
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

```bash
source venv/bin/activate
```

5. Install the dependencies

```bash
pip install -r requirements.txt
```

6. Create a .env file in the root directory of the project and add the following environment variables

```.env
DATABASE_URL=""
JWT_SECRET= ""
JWT_ALGORITHM=""
MAIL_USERNAME=""
MAIL_PASSWORD=""
MAIL_SERVER=""
MAIL_PORT=587
MAIL_FROM=""
MAIL_FROM_NAME=""
DOMAIN=""
REDIS_URL=""
ALLOWED_ORIGINS=""
ALLOWED_HOSTS= ""

```

7. Run the application

```bash
fastapi run src/
```

8. The application should be running on http://localhost:8000
