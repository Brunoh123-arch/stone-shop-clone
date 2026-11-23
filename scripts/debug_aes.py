import os
import json
import base64
import sqlite3
import shutil
import ctypes
from ctypes import wintypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', ctypes.POINTER(ctypes.c_byte))
    ]

def decrypt_master_key():
    local_state_path = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Local State"
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:] # Strip 'DPAPI'
    
    blob_in = DATA_BLOB(len(encrypted_key), ctypes.cast(ctypes.create_string_buffer(encrypted_key), ctypes.POINTER(ctypes.c_byte)))
    blob_out = DATA_BLOB()
    
    crypt32 = ctypes.windll.crypt32
    if crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        key = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return key
    else:
        raise Exception("Failed to decrypt master key via DPAPI")

def test():
    key = decrypt_master_key()
    tmp = "tmp.db"
    shutil.copy2(r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Profile 95\Network\Cookies", tmp)
    c = sqlite3.connect(tmp)
    for r in c.execute("SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%tiktok%' LIMIT 5").fetchall():
        enc = r[1]
        print(f"Cookie: {r[0]}, Len: {len(enc)}, Prefix: {enc[:3]}")
        try:
            val = AESGCM(key).decrypt(enc[3:15], enc[15:], None)
            print("  Decrypted:", val[:20])
        except Exception as e:
            print("  Error:", type(e), e)
    c.close()
    os.remove(tmp)

if __name__ == "__main__":
    test()
