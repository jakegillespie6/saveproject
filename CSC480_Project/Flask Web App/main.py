from website import create_app

#comes from our __init.py__ file where we define what happens when we run our server
app=create_app()

#enables a debug mode for us :)
if(__name__ == '__main__'):
    app.run(debug=True)
