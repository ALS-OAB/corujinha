import os
import json

CIVIL_DIR = '/home/sfy/Corujinha/CIVIL'

# Additional pedagogical insights directly from Profª Roberta Queiroz's 46º Exame OAB Playlist
lecture_46_pedagogy = {
    # PARTE GERAL
    "robson, advogado de sucesso": {
        "aula_comentario": "<p><b>Profª Roberta Queiroz (46º OAB - Parte Geral):</b> 'Gente, atenção máxima: a prisão civil do devedor de alimentos (ou penal) não extingue a dívida nem cancela o dever do pai de sustentar o filho! Se a capacidade financeira de Robson se alterar pela prisão, a via correta é a Ação Revisional de Alimentos, mas a obrigação alimentar permanece hígida!'</p>",
        "dica": "<p>🔥 <b>Dica de OAB da Profª Roberta:</b> Prisão não perdoa alimentos! Menor não deixa de ter fome porque o pai foi preso. A obrigação alimentar persiste!</p>"
    },
    "joana, conhecida durante toda a sua vida em sua cidade natal pelo prenome giovanna": {
        "aula_comentario": "<p><b>Profª Roberta Queiroz (46º OAB - Parte Geral):</b> 'No direito ao nome (Art. 16 CC), o apelido público notório ou a situação em que a pessoa é conhecida notória e publicamente por outro prenome autoriza a retificação do registro civil de nascimento! A imutabilidade do nome não é absoluta no Direito Brasileiro.'</p>",
        "dica": "<p>🔥 <b>Dica de OAB da Profª Roberta:</b> Pessoa conhecida publicamente por outro nome (prenome social/apelido notório) tem direito resguardado à alteração do prenome civil!</p>"
    },
    "gabriel cervantes teve graves problemas": {
        "aula_comentario": "<p><b>Profª Roberta Queiroz (46º OAB - Parte Geral):</b> 'Cuidado com o Estatuto da Pessoa com Deficiência! A curatela hoje é medida extraordinária e fica restrita EXCLUSIVAMENTE aos atos de natureza patrimonial e negocial (Art. 1.782 CC). A pessoa mantém capacidade para casar, votar, trabalhar e exercer direitos existenciais!'</p>",
        "dica": "<p>🔥 <b>Dica de OAB da Profª Roberta:</b> Curatela afeta APENAS atos patrimoniais e negociais! Direitos existenciais pertencem integralmente à pessoa curatelada.</p>"
    },

    # NEGÓCIO JURÍDICO
    "nicolas, servidor do tribunal de justiça": {
        "aula_comentario": "<p><b>Profª Roberta Queiroz (46º OAB - Negócio Jurídico):</b> 'Servidor público não tem legitimação para arrematar ou comprar bens em hasta pública da própria vara em que atua! A proibição do Art. 497, III do Código Civil visa proteger a moralidade e a imparcialidade. A compra e venda realizada nessas condições é NULA de pleno direito!'</p>",
        "dica": "<p>🔥 <b>Dica de OAB da Profª Roberta:</b> Servidor comprando em leilão da própria vara = NULIDADE ABSOLUTA (Art. 497, III CC). Não convalesce nem gera efeitos válidos!</p>"
    },

    # DIREITOS REAIS
    "waldo é titular de vultoso patrimônio": {
        "aula_comentario": "<p><b>Profª Roberta Queiroz (46º OAB - Direitos Reais / Coisas):</b> 'A doação de bem imóvel é contrato solene e exige OBRIGATORIAMENTE instrumento escrito (escritura pública ou instrumento particular conforme o Art. 108 e 541 CC). A simples entrega verbal das chaves não transfere a propriedade e não convalida a doação imobiliária!'</p>",
        "dica": "<p>🔥 <b>Dica de OAB da Profª Roberta:</b> Doação de imóvel NUNCA é verbal! Exige forma escrita obrigatória. Doação verbal só vale para bens móveis de pequeno valor seguidos de tradição imediata!</p>"
    },

    # FAMÍLIA
    "pedro e joana casaram-se pelo regime da comunhão parcial": {
        "aula_comentario": "<p><b>Profª Roberta Queiroz (46º OAB - Direito de Família):</b> 'Na comunhão parcial de bens, prestem atenção na pegadinha da OAB: herança e doação recebidas por um dos cônjuges SÃO BENS PARTICULARES (Art. 1.659, I CC) e NÃO se partilham! Já o prêmio de loteria é bem comum adquirido por fato eventual (Art. 1.660, II CC) e ENTRA na partilha do divórcio!'</p>",
        "dica": "<p>🔥 <b>Dica de OAB da Profª Roberta:</b> Herança/Doação = NÃO partilha (bem particular)! Prêmio de Loteria = PARTILHA (fato eventual entra na comunhão)!</p>"
    }
}

# Update JSON files with lecture updates
json_files = sorted([f for f in os.listdir(CIVIL_DIR) if f.endswith('_questoes.json')])

updated_count = 0
for jf in json_files:
    path = os.path.join(CIVIL_DIR, jf)
    with open(path, 'r', encoding='utf-8') as f:
        qs = json.load(f)
        
    for q in qs:
        txt = q.get('enunciado', '').lower()
        for snippet, pedagogy in lecture_46_pedagogy.items():
            if snippet.lower() in txt:
                q['aula_comentario'] = pedagogy['aula_comentario']
                q['dica'] = pedagogy['dica']
                updated_count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)

print(f"✨ Atualização concluída com base na Playlist do 46º Exame OAB!")
print(f"  - Cartões enriquecidos diretamente com ensinamentos da Profª Roberta Queiroz: {updated_count}")
