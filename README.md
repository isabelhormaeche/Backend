# Film Locations Blog App

**Film Locations BLog APP** helps you discover and explore amazing film locations around the Basque Country. Its mission is to provide a comprehensive database of film locations, making it easy for film production companies to work and experience the magic of this land. Registered users can participate and shared interesting filming locations for everybody to discover.

The project is built using **React** as the [frontend](https://github.com/isabelhormaeche/Frontend) framework and **Python with FastAPI as the backend**, and a **SQLite database** is used to store the data.

## What can you do in the website?

It is a blog page where the registered users can:

* **Read** posts.
* **Write** posts.
* **Edit** posts.
* **Delete** posts.

Users can register and then log in.

Users don't have to be logged in to read the posts, but they do have to be logged in to write, edit or delete posts.


## How the backend works

The backend is built using Python with FastAPI. The backend is hosted on Render, here:[Film Locations FastAPI app](https://filmlocationsapi.onrender.com/docs)) and the database is sql language: [SQLite](https://www.sqlite.org/). The backend is connected to the frontend using axios.

The backend has the following endpoints:

### POST

*`/api/login` - **Login**

*`/api/blogs/` - **Create Blog**

*`/api/users/` - **Register a new user**

### GET

*`/api/blogs/` - **Get Blogs**

*`/api/blogs/{id}` - **Get a single Blog**

*`/api/users/{id}` - **Get User´s information** (get user´s blogs,etc)

### PUT
*`/api/blogs/update_blog/{blog_id}` - **Edit Blog**

### DELETE
*`/api/blogs/{id}` - **Delete Blog**


## Who can use the backend?

Anyone can use the backend, but it is meant to be used by the frontend. The backend is not meant to be used by itself, but it can be used by anyone who wants to use it.

Some of the endpoints are protected, so you need to be logged in to use them. You can register. If you are not logged in, you will get an error message.


