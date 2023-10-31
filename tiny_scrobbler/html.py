def auth_result(got_token):
    info = '<h1>Authorization successful!</h1> \
            <p>You can close this window and return to the application</p>' \
            if got_token else \
            '<h1>Authorization failed!</h1>\
             <p>Something went wrong. Please try again</p>'
    
    return (f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tiny Scrobbler</title>
</head>
<body>
    {info}
</body>
<style>
    body {{
        background-color: #252526;
        font-family: Helvetica;
        color: white;
        font-size: large;
        text-align: center;
    }}
    h1 {{
        color: #d51007;
        font-size: xx-large;
    }}
</style>
</html>
''')