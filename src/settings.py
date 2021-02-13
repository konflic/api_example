import os

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'BLABLA']

DB_NAME = "database.db"

ADMIN = {
    "login": os.getenv("LOGIN"),
    "password": os.getenv("PASSWORD")
}

style = """
<head>
    <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 5px;
          text-align: left;
        }
    </style>
</head>
"""