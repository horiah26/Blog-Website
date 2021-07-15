"""Run the program from here"""
import app
from database.erase import erase_all_posts
from database.create_tables import create_post_table
from database.connection import get_connection

#erase_all_posts()
#create_post_table(get_connection())
instance = app.create_app()

instance.run(debug=True)
