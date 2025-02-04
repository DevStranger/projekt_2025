app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'twoj_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'twoje_haslo'
app.config['MAIL_DEFAULT_SENDER'] = 'twoj_email@gmail.com'
mail = Mail(app)
