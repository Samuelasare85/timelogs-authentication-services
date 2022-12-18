import bcrypt

def encryptPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def validatePassword(password: str, encrypted: str) -> str:
    return bcrypt.checkpw(password.encode("utf-8"), encrypted.encode("utf-8"))

