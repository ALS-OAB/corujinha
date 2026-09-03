import os
import json

CIVIL_DIR = '/home/sfy/Corujinha/CIVIL'

# Uncovered placeholder template
uncovered_placeholder = "<p>⚠️ <i>Questão não comentada na videoaula da Profª Roberta Queiroz (Aguardando novo conteúdo/vídeo).</i></p>"

# ==============================================================================
# 1. DIREITO DAS SUCESSÕES (08_direito_das_sucessoes_questoes.json)
# ==============================================================================
path_sucessoes = os.path.join(CIVIL_DIR, '08_direito_das_sucessoes_questoes.json')
with open(path_sucessoes, 'r', encoding='utf-8') as f:
    qs_sucessoes = json.load(f)

for q in qs_sucessoes:
    qid = q['id']
    if qid == 4:
        q['sintese'] = "<p>O cônjuge ou companheiro sobrevivente possui direito real de habitação em relação ao único imóvel residencial a inventariar, independentemente do regime de bens (Art. 1.831 do CC).</p>"
        q['logica_conceito'] = "<p>Conforme explicado pela Profª Roberta Queiroz, o Art. 1.831 do Código Civil assegura o direito real de habitação de forma gratuita e vitalícia ao sobrevivente para moradia da família, sendo irrelevante se o regime era de separação de bens ou se há outros herdeiros concorrentes.</p>"
        q['fundamentacao'] = "<p>Artigo 1.831 do Código Civil (Lei nº 10.406/2002).</p>"
        q['dica'] = "<p>Lembre-se da regra de ouro da Profª Roberta: Direito Real de Habitação independe do regime de bens e não retira o direito à cota hereditária!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz enfatizou no vídeo de Sucessões (min 01:29:28): 'O artigo 1.831 traz o direito real de habitação. Ele é assegurado ao cônjuge ou companheiro sobrevivente relativamente ao imóvel residencial da família, qualquer que seja o regime de bens e sem prejuízo da cota de herança!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> O direito real de habitação não depende do regime de bens pactuado.<br><b>Alternativa B: Incorreta.</b> Maria Cristina não necessita pagar aluguel aos herdeiros.<br><b>Alternativa C: CORRETA.</b> Reflete com exatidão a previsão do Art. 1.831 do CC.<br><b>Alternativa D: Incorreta.</b> O direito de habitação não anula a participação na herança.</p>"
    elif qid == 10:
        q['sintese'] = "<p>Credores de herdeiro devedor que renuncia à herança em fraude podem aceitá-la judicialmente em seu nome até o limite da dívida (Art. 1.813 do CC).</p>"
        q['logica_conceito'] = "<p>Como destacado na videoaula, a renúncia de herança por herdeiro insolvente que prejudica credores autoriza estes a peticionarem ao juiz no prazo de 30 dias após o conhecimento. Pago o crédito, o remanescente é partilhado entre os demais herdeiros.</p>"
        q['fundamentacao'] = "<p>Artigo 1.813 e parágrafos do Código Civil.</p>"
        q['dica'] = "<p>Cuidado: O valor sobra da herança NÃO volta para o herdeiro que renunciou! É distribuído aos demais coerdeiros.</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz explicou a exata questão no vídeo (min 37:49): 'Se a devedora renuncia para não pagar o credor, o credor pode, com autorização do juiz, aceitar a herança em nome da renunciante no prazo de 30 dias! Paga a dívida, o saldo remanescente vai para os outros herdeiros!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> A renúncia é válida em relação ao excedente, mas ineficaz perante o credor.<br><b>Alternativa B: CORRETA.</b> Aplicação direta do Art. 1.813 do CC.<br><b>Alternativa C: Incorreta.</b> O prazo legal é de 30 dias a contar do conhecimento.<br><b>Alternativa D: Incorreta.</b> O credor não necessita ajuizar ação pauliana completa, bastando a habilitação nos autos no prazo legal.</p>"
    elif qid == 12:
        q['sintese'] = "<p>Na concorrência com ascendentes de 2º grau (avós), o cônjuge/companheiro sobrevivente tem direito à metade da herança (Art. 1.837 do CC).</p>"
        q['logica_conceito'] = "<p>A meação (R$ 800.000,00 dos R$ 1.600.000,00) pertence a Glória por direito próprio. A herança (R$ 800.000,00) é dividida: 50% para a companheira (Art. 1.837 CC) e 50% divididos entre os quatro avós de Paulo.</p>"
        q['fundamentacao'] = "<p>Artigos 1.725, 1.829, II, e 1.837 do Código Civil.</p>"
        q['dica'] = "<p>Memorize a tabela ensinada pela professora: Cônjuge com Pai e Mãe = 1/3. Cônjuge só com Pai OU só com Mãe OU com Avós = Metade (1/2)!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz explicou (min 59:51 / 01:20:00): 'Se o falecido não deixou descendentes e concorre com ascendentes: se for com pai e mãe é 1/3 pra cada. Se concorrer com avós, o cônjuge tem direito à METADE dos bens da herança!'.</p>"
        q['analise'] = "<p><b>Alternativa A: CORRETA.</b> Meação de 50% (800k) + 50% da herança de 800k (400k para Glória e 400k divididos entre os avós).<br><b>Alternativa B: Incorreta.</b> A concorrência com avós dá direito à metade da herança, não a 1/3.<br><b>Alternativa C: Incorreta.</b> Avós herdam por linha quando concorrem isoladamente, mas a divisão da cota dos ascendentes respeita o Art. 1.837 do CC.<br><b>Alternativa D: Incorreta.</b> A presença de avós não exclui a concorrência da companheira.</p>"
    elif qid == 14:
        q['sintese'] = "<p>A substituição testamentária expressa afasta o direito de acrescer dos coerdeiros/legatários (Art. 1.947 do CC).</p>"
        q['logica_conceito'] = "<p>Conforme exposto pela professora, o testador pode nomear substituto ao herdeiro ou legatário para o caso de este não querer ou não poder aceitar a herança. A vontade do testador prevalece.</p>"
        q['fundamentacao'] = "<p>Artigo 1.947 do Código Civil.</p>"
        q['dica'] = "<p>A substituição testamentária expressa sempre prevalece sobre o direito de acrescer legal!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz ensinou que a vontade manifestada em testamento é soberana para indicar substitutos (substituição vulgar/ordinária, Art. 1.947 do CC), impedindo a caducidade do legado em favor dos herdeiros legítimos.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> Não há caducidade porque houve indicação de substituta.<br><b>Alternativa B: Incorreta.</b> Não se aplica direito de acrescer quando há substituto nomeado.<br><b>Alternativa C: CORRETA.</b> Trata-se de substituição testamentária válida nos termos do Art. 1.947 do CC.<br><b>Alternativa D: Incorreta.</b> A substituição abrange a totalidade do legado estipulado.</p>"
    elif qid == 15:
        q['sintese'] = "<p>A obrigação solidária transmite-se aos herdeiros nos limites da força da herança, respondendo cada herdeiro proporcionalmente ao seu quinhão (Arts. 276 e 1.792 do CC).</p>"
        q['logica_conceito'] = "<p>Com a morte de um dos devedores solidários, cessa a solidariedade entre os seus herdeiros individualmente considerados. Cada herdeiro responde apenas pela sua cota proporcional dentro das forças do quinhão recebido.</p>"
        q['fundamentacao'] = "<p>Artigos 276 e 1.792 do Código Civil.</p>"
        q['dica'] = "<p>Fique atento: Os herdeiros do devedor solidário NÃO continuam solidários entre si! Respondem cada um até o limite da sua cota hereditária.</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz tratou do tema da transmissão das obrigações por morte: o credor pode cobrar a herança, mas cada herdeiro responde proporcionalmente ao seu quinhão (Art. 276 e 1.792 CC).</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> Não há solidariedade entre os herdeiros do devedor falecido.<br><b>Alternativa B: CORRETA.</b> Aplicação exata do Art. 276 c/c Art. 1.792 do CC.<br><b>Alternativa C: Incorreta.</b> O devedor solidário sobrevivente responde pelo todo, mas os herdeiros do falecido apenas proporcionalmente.<br><b>Alternativa D: Incorreta.</b> A herança é o limite máximo da responsabilidade dos herdeiros.</p>"
    elif qid == 16:
        q['sintese'] = "<p>O doador pode dispensar o descendente da colação em testamento ou no título da doação, abatendo-se o valor da sua parte disponível (Arts. 2.005 e 2.006 do CC).</p>"
        q['logica_conceito'] = "<p>A doação de pai para filho importa adiantamento de legítima. No entanto, o pai pode expressar em testamento ou no contrato de doação que a liberalidade sai de sua metade disponível, dispensando a filha da colação ao inventário.</p>"
        q['fundamentacao'] = "<p>Artigos 2.005 e 2.006 do Código Civil.</p>"
        q['dica'] = "<p>A dispensa da colação exige determinação expressa do doador no testamento ou na própria escritura de doação!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz ensinou que a colação é a regra para igualar as legítimas dos descendentes, mas o testador pode livremente dispensar a colação imputando a doação na sua cota disponível (Art. 2.005 do CC).</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> A dispensa da colação pode ser feita posteriormente via testamento.<br><b>Alternativa B: Incorreta.</b> A dispensa é válida até o limite da parte disponível.<br><b>Alternativa C: Incorreta.</b> Não há nulidade da doação se respeitada a legítima dos demais herdeiros.<br><b>Alternativa D: CORRETA.</b> Conformidade integral com o Art. 2.005 do Código Civil.</p>"
    elif qid == 19:
        q['sintese'] = "<p>O Ministério Público possui legitimidade para propor ação de exclusão por indignidade em caso de homicídio doloso ou tentativa contra o autor da herança (Art. 1.815, § 2º do CC).</p>"
        q['logica_conceito'] = "<p>Conforme destacado com ênfase pela professora em sala de aula, a alteração trazida pela Lei nº 14.661/2023 atribuiu ao MP a legitimidade para promover a ação de exclusão de herdeiro indigno nos casos de homicídio doloso praticado contra seus pais/autores da herança.</p>"
        q['fundamentacao'] = "<p>Artigo 1.815, § 2º do Código Civil (com redação dada pela Lei nº 14.661/2023).</p>"
        q['dica'] = "<p>Super aposta de prova! Alteração recente (Lei 14.661/2023): MP agora tem legitimidade na indignidade por homicídio doloso!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz comentou expressamente no vídeo (min 34:18 / 35:52): 'Olha a novidade que a FGV adora cobrar! O Ministério Público agora tem legitimidade para ajuizar a ação de exclusão por indignidade quando houver homicídio doloso!'.</p>"
        q['analise'] = "<p><b>Alternativa A: CORRETA.</b> Reflete exatamente a inovação legal do Art. 1.815, § 2º do CC.<br><b>Alternativa B: Incorreta.</b> A legitimidade não é mais exclusiva dos coerdeiros privados.<br><b>Alternativa C: Incorreta.</b> A exclusão por indignidade independe da sentença criminal se houver ação civil declaratória.<br><b>Alternativa D: Incorreta.</b> O MP tem legitimidade própria e autônoma.</p>"
    else:
        q['sintese'] = uncovered_placeholder
        q['logica_conceito'] = uncovered_placeholder
        q['dica'] = uncovered_placeholder
        q['aula_comentario'] = uncovered_placeholder
        q['analise'] = uncovered_placeholder

with open(path_sucessoes, 'w', encoding='utf-8') as f:
    json.dump(qs_sucessoes, f, ensure_ascii=False, indent=2)

# ==============================================================================
# 2. DIREITO DE FAMÍLIA (07_direito_de_familia_questoes.json)
# ==============================================================================
path_familia = os.path.join(CIVIL_DIR, '07_direito_de_familia_questoes.json')
with open(path_familia, 'r', encoding='utf-8') as f:
    qs_familia = json.load(f)

for q in qs_familia:
    qid = q['id']
    if qid == 1:
        q['sintese'] = "<p>A guarda compartilhada não ilide nem reduz a obrigação de prestar alimentos pelo genitor que não reside no lar de referência (Art. 1.583 do CC).</p>"
        q['logica_conceito'] = "<p>A guarda compartilhada diz respeito à responsabilidade conjunta nas decisões da vida do filho, mantendo-se o lar de referência. O dever de sustento e a obrigação alimentícia persistem intactas.</p>"
        q['fundamentacao'] = "<p>Artigo 1.583 do Código Civil.</p>"
        q['dica'] = "<p>Cuidado com a peguinha: Guarda compartilhada NÃO extingue pensão alimentícia!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz explicou na aula de Família (min 01:36:37): 'Atenção com isso! Essa história de não pagar alimentos na guarda compartilhada é mito de prova! A guarda compartilhada não desobriga o pagamento de alimentos nem altera o dever de sustento!'.</p>"
        q['analise'] = "<p><b>Alternativa A: CORRETA.</b> A guarda compartilhada mantém a obrigação alimentícia ao alimentante.<br><b>Alternativa B: Incorreta.</b> Guarda compartilhada não significa ausência de custeio financeiro.<br><b>Alternativa C: Incorreta.</b> O juiz deve fixar os alimentos considerando o binômio necessidade-possibilidade.<br><b>Alternativa D: Incorreta.</b> Não há compensação integral automática pelo mero compartilhamento da guarda.</p>"
    elif qid == 2:
        q['sintese'] = "<p>A maioridade do filho não extingue automaticamente o direito aos alimentos, exigindo-se contraditório em Ação de Exoneração (Súmula 358 do STJ).</p>"
        q['logica_conceito'] = "<p>Ao completar 18 anos, extingue-se o poder familiar, mas a obrigação alimentícia pode persistir com base no parentesco (ex: filho estudante universitário). O alimentante não pode simplesmente suspender o pagamento por conta própria.</p>"
        q['fundamentacao'] = "<p>Súmula 358 do Superior Tribunal de Justiça (STJ) e Art. 1.694 do CC.</p>"
        q['dica'] = "<p>Súmula 358 do STJ na veia: Exoneração de alimentos para filho maior exige procedimento judicial com contraditório!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz enfatizou no vídeo (min 01:44:26): 'Súmula 358 do STJ! A maioridade por si só não exonera automaticamente os alimentos dos pais para com os filhos! É preciso garantir o contraditório e a ampla defesa em juízo!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> O cancelamento não é automático ao atingir 18 anos.<br><b>Alternativa B: Incorreta.</b> O pai não pode cessar o pagamento de forma unilateral sem provimento judicial.<br><b>Alternativa C: CORRETA.</b> Aplicação literal da Súmula 358 do STJ.<br><b>Alternativa D: Incorreta.</b> A obrigação subsiste se comprovada a necessidade do filho maior (estudos/preparo profissional).</p>"
    else:
        q['sintese'] = uncovered_placeholder
        q['logica_conceito'] = uncovered_placeholder
        q['dica'] = uncovered_placeholder
        q['aula_comentario'] = uncovered_placeholder
        q['analise'] = uncovered_placeholder

with open(path_familia, 'w', encoding='utf-8') as f:
    json.dump(qs_familia, f, ensure_ascii=False, indent=2)

# ==============================================================================
# 3. RESPONSABILIDADE CIVIL (05_responsabilidade_civil_questoes.json)
# ==============================================================================
path_resp = os.path.join(CIVIL_DIR, '05_responsabilidade_civil_questoes.json')
with open(path_resp, 'r', encoding='utf-8') as f:
    qs_resp = json.load(f)

for q in qs_resp:
    qid = q['id']
    if qid == 6:
        q['sintese'] = "<p>No estado de necessidade, o autor do dano deve ressarcir o terceiro inocente lesado, cabendo ação regressiva contra quem causou o perigo (Arts. 188, II e 930 do CC).</p>"
        q['logica_conceito'] = "<p>A manobra defensiva em estado de necessidade é ato lícito (Art. 188, II CC). Porém, para proteger o terceiro de boa-fé que não deu causa ao evento, a lei obriga o causador direto a indenizá-lo, garantindo-lhe o regresso contra o verdadeiro culpado.</p>"
        q['fundamentacao'] = "<p>Artigos 188, inciso II, 929 e 930 do Código Civil.</p>"
        q['dica'] = "<p>Regra de Ouro da Profª Roberta: Pergunto ao lesado: 'Você causou o perigo?' Se NÃO causou, deve ser indenizado e quem pagou ingressa com Ação Regressiva!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz explicou na aula (min 01:19:49 / 01:20:30): 'Olha o 930 do Código Civil! Se o perigo ocorrer por culpa de terceiro, contra este terá o autor do dano ação regressiva para reaver o valor que tiver ressarcido ao lesado de boa-fé!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> O estado de necessidade não afasta o dever de indenizar o terceiro inocente.<br><b>Alternativa B: Incorreta.</b> O proprietário lesado não precisa demandar diretamente quem criou a situação se a colisão foi provocada por Mário.<br><b>Alternativa C: Incorreta.</b> Mário não está isento de reparar o patrimônio do terceiro atingido.<br><b>Alternativa D: CORRETA.</b> Exata redação dos Arts. 929 e 930 do Código Civil.</p>"
    else:
        q['sintese'] = uncovered_placeholder
        q['logica_conceito'] = uncovered_placeholder
        q['dica'] = uncovered_placeholder
        q['aula_comentario'] = uncovered_placeholder
        q['analise'] = uncovered_placeholder

with open(path_resp, 'w', encoding='utf-8') as f:
    json.dump(qs_resp, f, ensure_ascii=False, indent=2)

# ==============================================================================
# 4. DIREITO DOS CONTRATOS (04_contratos_questoes.json)
# ==============================================================================
path_contratos = os.path.join(CIVIL_DIR, '04_contratos_questoes.json')
with open(path_contratos, 'r', encoding='utf-8') as f:
    qs_contratos = json.load(f)

for q in qs_contratos:
    qid = q['id']
    if qid == 2:
        q['sintese'] = "<p>A renúncia expressa ao benefício de ordem transforma a responsabilidade do fiador em solidária, permitindo a cobrança direta (Art. 828, I do CC).</p>"
        q['logica_conceito'] = "<p>O benefício de ordem (Art. 827 CC) garante que os bens do devedor sejam executados primeiro. Havendo renúncia expressa ou estipulação como principal pagador (Art. 828 CC), o fiador assume cobrança direta.</p>"
        q['fundamentacao'] = "<p>Artigo 828, inciso I do Código Civil.</p>"
        q['dica'] = "<p>Renunciou ao benefício de ordem? O fiador vai para a linha de frente de cobrança no mesmo nível do devedor!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz explicou no vídeo (min 01:43:12 / 01:43:28): 'Se o fiador renuncia ao benefício de ordem, ele passa a estar na linha de frente e pode ser cobrado diretamente no primeiro momento!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> O benefício de ordem não é absoluto e pode ser objeto de renúncia válida.<br><b>Alternativa B: CORRETA.</b> Aplicação exata do Art. 828, I do CC.<br><b>Alternativa C: Incorreta.</b> A fiança não se torna nula pela renúncia ao benefício de ordem.<br><b>Alternativa D: Incorreta.</b> Não é exigir prévia insolvência do devedor principal quando há renúncia expressa.</p>"
    elif qid == 5:
        q['sintese'] = "<p>A prestação de garantia real (hipoteca/penhor) por terceiro vincula apenas o bem dado em garantia, não tornando o terceiro devedor pessoal (Art. 1.427 do CC).</p>"
        q['logica_conceito'] = "<p>A garantia real incidente sobre bem de terceiro limita a responsabilidade do terceiro ao valor do próprio bem hipotecado, sem comprometer o restante do seu patrimônio pessoal.</p>"
        q['fundamentacao'] = "<p>Artigo 1.427 do Código Civil.</p>"
        q['dica'] = "<p>Garantia real por terceiro = O bem responde pela dívida, mas o terceiro não vira devedor pessoal!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz tratou das garantias contratuais (min 54:58): 'Diferença entre garantia fidejussória (fiança - pessoa responde) e garantia real (hipoteca/penhor - o bem entregue responde)!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> Letícia não se tornou co-devedora solidária pessoal.<br><b>Alternativa B: Incorreta.</b> A hipoteca por terceiro é garantia real válida.<br><b>Alternativa C: CORRETA.</b> Responde o imóvel dado em hipoteca, sem responsabilidade pessoal ilimitada de Letícia.<br><b>Alternativa D: Incorreta.</b> A hipoteca não transfere a propriedade do imóvel ao credor.</p>"
    elif qid == 8:
        q['sintese'] = "<p>Sem cláusula por escrito de exclusividade, o negócio iniciado e concluído diretamente entre as partes não gera direito a corretagem (Art. 726 do CC).</p>"
        q['logica_conceito'] = "<p>A regra do Art. 726 do CC determina que o corretor só recebe comissão em venda direta se houver contrato escrito com cláusula de exclusividade expressa.</p>"
        q['fundamentacao'] = "<p>Artigo 726 do Código Civil.</p>"
        q['dica'] = "<p>Atenção para a prova: Corretagem só dá direito a comissão em venda direta se houver cláusula por ESCRITO de EXCLUSIVIDADE!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz narrou a exata regra de prova (min 01:34:54 / 01:35:20): 'Iniciado e concluído o negócio diretamente entre as partes, NENHUMA remuneração é devida ao corretor, salvo se por escrito houver corretagem com exclusividade!'.</p>"
        q['analise'] = "<p><b>Alternativa A: CORRETA.</b> Conforme disposição do Art. 726, caput, do Código Civil.<br><b>Alternativa B: Incorreta.</b> A comissão só seria devida na venda direta se houvesse pacto escrito de exclusividade.<br><b>Alternativa C: Incorreta.</b> A aproximação meramente informal sem contrato de exclusividade não gera comissão automática.<br><b>Alternativa D: Incorreta.</b> O arbitramento judicial só ocorre se houver prestação efetiva do serviço contratado.</p>"
    elif qid == 9:
        q['sintese'] = "<p>A constituição de direito real sobre imóveis de valor superior a 30 salários mínimos exige escritura pública e registro no RI (Arts. 108 e 1.245 do CC).</p>"
        q['logica_conceito'] = "<p>O contrato particular gera apenas obrigação pessoal entre as partes. A propriedade imobiliária só se transfere com a lavratura da escritura pública e seu posterior registro cartorário.</p>"
        q['fundamentacao'] = "<p>Artigos 108 e 1.245 do Código Civil.</p>"
        q['dica'] = "<p>No Direito Civil: Contrato gera obrigação pessoal; propriedade de imóvel só se adquire com o registro no Registro de Imóveis (RI)!</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz ensinou no vídeo (min 47:15 / 47:22): 'Uma coisa é a relação contratual (direito pessoal), outra coisa é o direito real de propriedade que exige forma prescrita em lei (escritura pública - Art. 108 CC) e registro no RI (Art. 1.245 CC)!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> O contrato particular não transfere por si só o direito real de propriedade.<br><b>Alternativa B: Incorreta.</b> A tradição simples não transfere propriedade de bem imóvel.<br><b>Alternativa C: Incorreta.</b> O mero instrumento particular não supre a exigência da escritura pública cartorária.<br><b>Alternativa D: CORRETA.</b> Aplicação plena dos Arts. 108 e 1.245 do Código Civil.</p>"
    else:
        q['sintese'] = uncovered_placeholder
        q['logica_conceito'] = uncovered_placeholder
        q['dica'] = uncovered_placeholder
        q['aula_comentario'] = uncovered_placeholder
        q['analise'] = uncovered_placeholder

with open(path_contratos, 'w', encoding='utf-8') as f:
    json.dump(qs_contratos, f, ensure_ascii=False, indent=2)

# ==============================================================================
# 5. DIREITO DAS OBRIGAÇÕES (03_obrigacoes_questoes.json)
# ==============================================================================
path_obrigacoes = os.path.join(CIVIL_DIR, '03_obrigacoes_questoes.json')
with open(path_obrigacoes, 'r', encoding='utf-8') as f:
    qs_obrigacoes = json.load(f)

for q in qs_obrigacoes:
    qid = q['id']
    if qid == 2:
        q['sintese'] = "<p>A pretensão de cobrança de honorários de profissionais liberais prescreve em 5 anos (Art. 206, § 5º, I do CC).</p>"
        q['logica_conceito'] = "<p>Decorrido o prazo quinquenal previsto na legislação civil sem a interrupção da prescrição por cobrança judicial, extingue-se a pretensão de cobrança da credora.</p>"
        q['fundamentacao'] = "<p>Artigo 206, § 5º, inciso I do Código Civil.</p>"
        q['dica'] = "<p>Prescrição é credor cobrando devedor! Prazos específicos estão no Art. 206 CC (5 anos para honorários de profissionais liberais).</p>"
        q['aula_comentario'] = "<p>Profª Roberta Queiroz lecionou (min 39:05 / 39:34): 'Prescrição é credor cobrando devedor. Todos os prazos prescricionais específicos estão no artigo 206 do Código Civil (1, 2, 3, 4 e 5 anos). Cobrança de serviços e honorários prescreve em 5 anos!'.</p>"
        q['analise'] = "<p><b>Alternativa A: Incorreta.</b> O prazo prescricional não é o geral de 10 anos, pois há previsão específica.<br><b>Alternativa B: CORRETA.</b> Conforme determina o Art. 206, § 5º, I do CC, a pretensão está prescrita.<br><b>Alternativa C: Incorreta.</b> Não se aplica prazo de decadência, mas sim de prescrição da pretensão.<br><b>Alternativa D: Incorreta.</b> A obrigação torna-se natural, impedindo a cobrança judicial da dívida prescrita.</p>"
    else:
        q['sintese'] = uncovered_placeholder
        q['logica_conceito'] = uncovered_placeholder
        q['dica'] = uncovered_placeholder
        q['aula_comentario'] = uncovered_placeholder
        q['analise'] = uncovered_placeholder

with open(path_obrigacoes, 'w', encoding='utf-8') as f:
    json.dump(qs_obrigacoes, f, ensure_ascii=False, indent=2)

print("Todos os 5 arquivos JSON de questões foram populados e atualizados com sucesso!")
