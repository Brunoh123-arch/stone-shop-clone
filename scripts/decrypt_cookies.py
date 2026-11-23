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

def decrypt_cookie_value(encrypted_val, master_key):
    try:
        nonce = encrypted_val[3:15]
        ciphertext = encrypted_val[15:]
        aesgcm = AESGCM(master_key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
    except Exception as e:
        return None

def get_p95_tiktok_cookies():
    master_key = decrypt_master_key()
    print("Master key decrypted successfully! Length:", len(master_key))
    
    src = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Profile 95\Network\Cookies"
    tmp = "temp_p95_cookies.db"
    shutil.copy2(src, tmp)
    
    conn = sqlite3.connect(tmp)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, path, expires_utc, is_secure, is_httponly, encrypted_value FROM cookies WHERE host_key LIKE '%tiktok%'")
    rows = cursor.fetchall()
    conn.close()
    if os.path.exists(tmp):
        os.remove(tmp)
        
    print(f"Total TikTok rows in Profile 95: {len(rows)}")
    decrypted = []
    for host_key, name, path, expires_utc, is_secure, is_httponly, enc_val in rows:
        val = decrypt_cookie_value(enc_val, master_key)
        if val:
            decrypted.append({
                "name": name,
                "value": val,
                "domain": host_key,
                "path": path,
                "secure": bool(is_secure),
                "httpOnly": bool(is_httponly)
            })
            if any(k in name.lower() for k in ['session', 'uid', 'sid', 'token']):
                print(f"  [DECRYPTED] {host_key} | {name} = {val[:12]}...")
                
    print(f"Total successfully decrypted cookies: {len(decrypted)}")
    with open("decrypted_p95_cookies.json", "w", encoding="utf-8") as f:
        json.dump(decrypted, f, indent=2)
    return decrypted

if __name__ == "__main__":
    get_p95_tiktok_cookies()
