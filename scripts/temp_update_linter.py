with open("scripts/linter_integridade_midia.py", "r", encoding="utf-8") as f:
    linter_code = f.read()

old_exc = '''    EXCEPTIONS_CAROUSEL = {
        (47, 49), (49, 47),
        (21, 74), (74, 21),
        (21, 99), (99, 21),
        (6, 94), (94, 6), # bikes fitness/spinning
        (53, 59), (59, 53), # starlink antenas
    }'''

new_exc = '''    EXCEPTIONS_CAROUSEL = {
        (47, 49), (49, 47),
        (21, 74), (74, 21),
        (21, 99), (99, 21),
        (6, 94), (94, 6), # bikes fitness/spinning
        (53, 59), (59, 53), # starlink antenas
        (34, 79), (79, 34), # redirect Praxis
        (48, 84), (84, 48), # redirect Gallant
        (61, 83), (83, 61), # redirect Joog Break X1
        (73, 81), (81, 73), # redirect Waaw Hyperboom
        (47, 78), (78, 47), # redirect Spot Cleaner
    }'''

assert old_exc in linter_code, "old_exc not found"
linter_code = linter_code.replace(old_exc, new_exc)

with open("scripts/linter_integridade_midia.py", "w", encoding="utf-8") as f:
    f.write(linter_code)

print("Linter exceptions updated with redirect aliases!")
