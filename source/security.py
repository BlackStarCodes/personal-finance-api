from pwdlib import PasswordHash


hasher = PasswordHash.recommended()

def pwd_hashed(pwd):
    return hasher.hash(pwd)






