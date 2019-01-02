from database import init_db, db_session
from models import User, Scrap
from werkzeug.security import generate_password_hash

init_db()

flag1 = "GoN{flask_default_session_is_weird_and_k33p_s3cr37_k3y_r3ally_s3cur3}"
flag2 = "GoN{I_hate_SQLi73_injec7i0n}"


# flag1 - flask session control due to leaked secret_key

admin_id = "admin"
admin_pw = "super_admin"
admin = User(admin_id, generate_password_hash(admin_pw))
db_session.add(admin)

fname = "f1r57_fl4g"
f = open(f"scraps/{fname}", 'w')
f.write(flag1)
f.close()

flag_scrap1 = Scrap(admin_id, fname, "Here is a flag")
db_session.add(flag_scrap1)


# flag2 - sqlite injection due to poor ORM usage

real_admin_id = "7h3_4dm1n"
real_admin_pw = "v3ry_s3cur3_qlalfqjsgh"
real_admin = User(real_admin_id, generate_password_hash(real_admin_pw))
db_session.add(real_admin)

flag_scrap = Scrap(real_admin_id, flag2, flag2) # not stored in file
db_session.add(flag_scrap)

db_session.commit()
db_session.remove()

