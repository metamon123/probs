from app import *

if __name__ == "__main__":
    init_db()
    try:
        app.run("0.0.0.0", 8080)
    finally:
        db_session.remove()
