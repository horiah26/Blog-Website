"""Run the program from here"""
import app

instance = app.create_app("db")

instance.run()
