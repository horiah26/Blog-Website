import app


instance = app.create_app()
instance.run(debug=True)