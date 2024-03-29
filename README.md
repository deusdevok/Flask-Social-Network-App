# Flask Tutorial Practice

Tutorial from [https://flask.palletsprojects.com/en/2.2.x/tutorial/](https://flask.palletsprojects.com/en/2.2.x/tutorial/)

## How to work with this repository

Create a new virtual environment:

`python -m venv env`

Activate the virtual environment (for example for Windows):

`venv\Scripts\activate`

Install all needed packages. You can do this with the help of the requirements.txt file:

`pip install -r requirements.txt`

To run the Flask app with debug mode on (in this case the app is called `flaskr`):

`flask --app flaskr --debug run`

If you need to initialize the database (warning: this will erase all your previously recorded data from the app):

`flask --app flaskr init-db`

## Testing



## Working on this extra steps 

(from [https://flask.palletsprojects.com/en/2.2.x/tutorial/next/](https://flask.palletsprojects.com/en/2.2.x/tutorial/next/))

* [x] A detail view to show a single post. Click a post’s title to go to its page.
* [x] Like / unlike a post.
* [x] Comments.
* [x] Tags. Clicking a tag shows all the posts with that tag.
* [x] A search box that filters the index page by name.
* [x] Paged display. Only show 5 posts per page.
* [x] Upload an image to go along with a post.
* [x] Format posts using Markdown.
* [x] An RSS feed of new posts.

## More features will be added in the future

* [ ] Each registered user has its own profile page. In that page you can see his name, email, bio, profile picture, posts, statistics, etc.
* [ ] Each registered user have the option to change his password.
* [ ] Visitors can check the registered users information.
* [ ] The body in the blog post can be either Markdown formatted or not via a checkbox.

## Features of the app

* Users can register to the app with a username and a password
* Registered users can log in to the app with their username and password
* Logged in users can create new blog posts
* Blog posts have title (required), body (required, markdown), tags (optional) and an image (optional)
