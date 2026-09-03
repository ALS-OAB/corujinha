with open('/home/sfy/Corujinha/CIVIL/build_civil_modules.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'q-topic' in l:
        lines[i] = '                  ${{q.tema ? `<span class="q-topic">${{q.tema}}</span>` : (q.modulo_nome ? `<span class="q-topic">${{q.modulo_nome}}</span>` : "")}}\n'
        print(f"✅ Substituído com chaves duplas f-string na linha {i+1}!")

with open('/home/sfy/Corujinha/CIVIL/build_civil_modules.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
