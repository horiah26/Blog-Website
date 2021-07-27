"""Run the program from here"""
import app
from config.config_db import ConfigDB
cf=ConfigDB()

instance = app.create_app()

instance.run()
