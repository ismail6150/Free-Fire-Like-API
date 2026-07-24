import requests
import json

UIDPASS_FILE = "uidpass.json"
TOKEN_FILE = "tokens.json"

# الـ API الخاص بك
API_URL = "http://187.127.175.208:5001/Bmw"

def read_uidpass():
    try:
        with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"خطأ: الملف {UIDPASS_FILE} غير موجود.")
        return []

def fetch_token(uid, password):
    params = {
        "uid": uid,
        "password": password
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # استخراج JwT_ToKeN و staTuS حسب استجابة الـ API في الصورة
        jwt_token = data.get("JwT_ToKeN")
        status = data.get("staTuS")
        
        if jwt_token and status == "success":
            return jwt_token
        else:
            print(f"فشل جلب التوكن للـ UID {uid}: {status}")
            return None
            
    except Exception as e:
        print(f"خطأ أثناء جلب التوكن للـ UID {uid}: {e}")
        return None

def update_token_file(token_list):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_list, f, ensure_ascii=False, indent=4)

def main():
    uidpass_list = read_uidpass()
    if not uidpass_list:
        return

    new_tokens = []
    for item in uidpass_list:
        uid = item.get("uid")
        password = item.get("password")
        
        if uid and password:
            token = fetch_token(uid, password)
            if token:
                new_tokens.append({
                    "uid": uid,
                    "token": token
                })

    if new_tokens:
        update_token_file(new_tokens)
        print(f"تم تحديث {len(new_tokens)} توكن في ملف {TOKEN_FILE} بنجاح.")
    else:
        print("لم يتم العثور على توكنات جديدة لتحديثها.")

if __name__ == "__main__":
    main()
