from config import app
from controller_functions import index, register, login, logout, dashboard, search, movie_details

app.add_url_rule("/", view_func=index)
app.add_url_rule("/users/create", methods=["POST"], view_func=register)
app.add_url_rule("/users/login", methods=["POST"], view_func=login)
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/dashboard", view_func=dashboard)
app.add_url_rule("/movies/search", methods=["POST"], view_func=search)
app.add_url_rule("/movies/<id>", view_func=movie_details)