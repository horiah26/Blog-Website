"""Run the program from here"""
import app

instance = app.create_app()

instance.run(debug=True)
