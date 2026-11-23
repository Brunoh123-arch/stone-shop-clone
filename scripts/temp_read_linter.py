with open("scripts/linter_integridade_midia.py", "r", encoding="utf-8") as f:
    linter_code = f.read()

pos = linter_code.find("EXCEPTIONS_CAROUSEL")
print(linter_code[pos:pos+600])
