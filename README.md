# Blog

This is a microblogging platform API built with Django and Django REST Framework. It allows users to create posts, follow other users, like posts, and retrieve their timelines.

## Prerequisites

Before running the application, ensure that you have the following dependencies installed:

- Python 3.x
- PostgreSQL
- Redis

## Installation

1. Clone the repository:

  git clone https://github.com/mithun2003/Backend-for-a-blog.git


2. Create a virtual environment and activate it:

  cd Blog

  Virturalenv env

  env/Scripts/activate




3. Install the required packages:

  pip install -r requirements.txt

4. Start the Redis server:

  redis-server

5. Set up the database and config it:
   
  Add your dbs information in the .env
  
  Python manage.py makemigrations
  
  python manage.py migrate

6. Start the application:

  python manage.py runserver

The API will be accessible at http://localhost:8000/api/.
## API Endpoints
POST /api/users/: Create a new user.
GET /api/users/<int:user_id>/: Retrieve details of a specific user.
PUT/PATCH /api/users/<int:user_id>/: Update the details of a specific user.
POST /api/posts/: Create a new post.
GET /api/posts/<int:post_id>/: Retrieve details of a specific post.
PUT/PATCH /api/posts/<int:post_id>/: Update the details of a specific post.
DELETE /api/posts/<int:post_id>/: Delete a specific post.
GET /api/posts/: Retrieve a list of all posts.
Refer to the API documentation for detailed information on request/response formats and error codes.
## Token-Based Authentication
This application uses token-based authentication. To authenticate requests, include the Authorization header with the value Bearer {access_token} in the request headers.
To obtain an access token, use the /api/login/ endpoint with valid user credentials. The response will include an access token and a refresh token. And also in every refresh token you get a new access and refresh token
## Redis Caching
Redis is used for caching frequently accessed data. The application utilizes Redis to cache the retrieved posts and user data for improved performance.


## Postman Collection
A Postman collection is provided (https://www.postman.com/telecoms-geologist-68488493/workspace/backend-endpoints/collection/25369645-6d19fbf5-4763-477f-9ab7-7fc457e07737?action=share&creator=25369645) to test the API endpoints. Import this collection into Postman to access pre-configured requests.
Setting Collection Variables
To set the collection variables for token authentication, follow these steps:
Open the imported collection in Postman.
Click on the collection name in the sidebar to view the collection details.
Click on the "..." button and select "Edit".
In the "Variables" tab, set the values for the following variables:
token: The access token obtained after successful login.
Save the collection.
Now you can use the pre-configured requests in the collection with the correct authentication tokens.
