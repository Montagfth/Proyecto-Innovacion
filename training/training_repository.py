import libsql
import os

conn = libsql.connect(
  database=os.environ["TURSO_DATABASE_URL"],
  auth_token=os.environ["TURSO_AUTH_TOKEN"],
)