with open('/home/sfy/Corujinha/CIVIL/build_civil_modules.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '<span class="q-topic">${q.tema}</span>'
replacement = "${q.tema ? '<span class=\"q-topic\">' + q.tema + '</span>' : (q.modulo_nome ? '<span class=\"q-topic\">' + q.modulo_nome + '</span>' : '')}"

if target in code:
    code = code.replace(target, replacement)
    with open('/home/sfy/Corujinha/CIVIL/build_civil_modules.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ q.tema corrigido com sucesso em build_civil_modules.py!")
else:
    print("⚠️ Target não encontrado")
