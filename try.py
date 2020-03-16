import casket
print(casket.sessions_list())

s = casket.load_session("jasoc", "casket")

print(s.decrypt_accounts()["pippo2"]["password"])
