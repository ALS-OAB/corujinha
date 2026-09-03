import os
import json
import re

CIVIL_DIR = '/home/sfy/Corujinha/CIVIL'

# ==============================================================================
# 1. RESUMOS DAS AULAS (Markdown) - Exclusivamente baseados nos vídeos
# ==============================================================================

resumo_sucessoes = """# Resumo Teórico Didático: Direito das Sucessões
**Profª Roberta Queiroz · Aula Preparatória OAB 47º Exame**

---

## 1. Abertura da Sucessão e Princípio da Saisine
* **Transmissão da Herança:** Pelo princípio da *saisine* (Art. 1.784 do CC), a herança transmite-se, desde logo, aos herdeiros legítimos e testamentários com a abertura da sucessão (momento exato da morte).
* **Indivisibilidade:** Até a partilha, o direito dos coerdeiros quanto à posse e propriedade da herança será indivisível e regular-se-á pelas normas relativas ao condomínio (Art. 1.791 do CC).

---

## 2. Cessão de Direitos Hereditários (Arts. 1.793 a 1.795 do CC)
* **Forma Exigida:** A cessão de direitos hereditários deve ser feita **obrigatoriamente por escritura pública** ou por **termo nos autos do inventário**. Instrumento particular é nulo.
* **Objeto:** Não se pode ceder bem individualizado da herança sem prévia autorização judicial, pois a herança é uma universalidade indivisível.
* **Direito de Preferência:** O coerdeiro não pode ceder sua cota hereditária a pessoa estranha à sucessão se outro coerdeiro a quiser, tanto por tanto.
  * Se não for notificado, o coerdeiro preterido pode haver para si a cota cedida, depositando o preço, no prazo decadencial de **180 dias** após a cessão.

---

## 3. Aceitação e Renúncia da Herança (Arts. 1.804 a 1.813 do CC)
* **Aceitação:** Pode ser expressa (por escrito) ou tácita (resultante de atos próprios da qualidade de herdeiro).
* **Renúncia:** 
  * É **estritamente formal**: exige **escritura pública** ou **termo judicial nos autos do inventário**. Não existe renúncia verbal ou por instrumento particular.
  * É **irrevogável, pura e simples** (não admite condição ou termo).
  * **Renúncia em prejuízo de credores (Art. 1.813 do CC):** Se o herdeiro devedor renunciar à herança para frustrar obrigações, os seus credores podem, com autorização do juiz, aceitá-la em nome do renunciante no prazo de **30 dias** após o conhecimento do fato. Paga-se o valor da dívida ao credor e o saldo remanescente é distribuído entre os demais coerdeiros (nada retorna ao renunciante).

---

## 4. Exclusão da Sucessão: Indignidade e Deserdação (Arts. 1.814 a 1.818 do CC)
* **Indignidade:** Aplica-se a qualquer sucessor (legítimo ou testamentário).
  * *Causas:* Autoria ou cumplicidade em homicídio doloso (ou tentativa) contra o autor da herança, cônjuge, companheiro, ascendente ou descendente; calúnia em juízo/crime contra a honra; fraude ou violência para obstar testamento.
  * *Procedimento:* Exige Ação Declaratória de Indignidade (prazo decadencial de 4 anos a contar da morte). 
  * *Novidade Legislativa (Lei nº 14.661/2023):* O **Ministério Público** possui legitimidade para ajuizar a ação de exclusão por indignidade no caso de homicídio doloso ou tentativa.
  * *Efeito Pessoal (Art. 1.816 do CC):* O herdeiro excluído é considerado como se morto fosse antes da abertura da sucessão. Seus descendentes herdam por representação.

---

## 5. Ordem de Vocação Hereditária e Concorrência do Cônjuge/Companheiro (Arts. 1.829 e 1.837 do CC)
* **Ordem Legal (Art. 1.829):**
  1. Descendentes em concorrência com o cônjuge/companheiro sobrevivente (conforme regime de bens).
  2. Ascendentes em concorrência com o cônjuge/companheiro sobrevivente.
  3. Cônjuge/Companheiro sobrevivente (integralidade da herança).
  4. Colaterais até o 4º grau (irmãos, tios/sobrinhos, tios-avós/primos/sobrinhos-netos). Sobrinhos têm preferência sobre tios (Art. 1.843).
* **Concorrência com Ascendentes (Art. 1.837):** Independe do regime de bens!
  * Concorrendo com pai e mãe do falecido = cabe **1/3** da herança ao cônjuge/companheiro.
  * Concorrendo com apenas um dos pais ou com avós = cabe **metade (1/2)** da herança ao cônjuge/companheiro e a outra metade aos ascendentes.

---

## 6. Direito Real de Habitação (Art. 1.831 do CC)
* Assegurado ao cônjuge ou companheiro sobrevivente, relativamente ao imóvel destinado à residência da família, desde que seja o único daquela natureza a inventariar.
* É **gratuito e vitalício**, prevalecendo **independentemente do regime de bens** e sem prejuízo da cota hereditária.

---

## 7. Sucessão Testamentária, Substituição e Colação (Arts. 1.947 e 2.005 do CC)
* **Substituição Testamentária (Art. 1.947 do CC):** O testador pode indicar substituto para o herdeiro ou legatário, para o caso de este não querer ou não poder aceitar a herança.
* **Dispensa de Colação (Art. 2.005 do CC):** As doações de ascendente a descendente importam adiantamento de legítima, mas o doador pode dispensar a colação via testamento ou no próprio título da doação, abatendo-se da sua parte disponível.
"""

resumo_familia = """# Resumo Teórico Didático: Direito de Família
**Profª Roberta Queiroz · Aula Preparatória OAB 47º Exame**

---

## 1. Impedimentos para o Casamento e Idade Núbil (Arts. 1.517 e 1.521 do CC)
* **Idade Núbil:** Fixada aos **16 anos** (Art. 1.517 do CC), exigindo autorização de ambos os pais ou suprimento judicial.
* **Proibição de Casamento Infantil:** Desde a Lei nº 13.811/2019, **não se permite o casamento de menores de 16 anos** em hipótese alguma (revogadas as exceções de gravidez e evitação de pena criminal).
* **Impedimentos Absolutos (Art. 1.521 do CC):** Não podem casar as pessoas casadas (bigamia), ascendentes com descendentes, irmãos e demais colaterais até o 3º grau, adotante com adotado, ou o cônjuge sobrevivente com o condenado por homicídio contra o seu consorte.

---

## 2. Casamento Nuncupativo (Arts. 1.540 e 1.541 do CC)
* É o casamento celebrado em situação de iminente perigo de vida de um dos contraentes, sem a presença do celebrante oficial.
* Exige a presença de **6 testemunhas** desimpedidas. As testemunhas devem comparecer à autoridade judicial em até **10 dias** para tomar por termo a declaração e validar o ato.

---

## 3. Pacto Antenupcial (Arts. 1.653 a 1.657 do CC)
* Exige **escritura pública** lavrada em Cartório de Notas.
* É nulo se não for feito por escritura pública e **ineficaz se não lhe seguir o casamento**.

---

## 4. Regimes de Bens e Separação Obrigatória (Arts. 1.640 e 1.641 do CC)
* **Comunhão Parcial:** É o regime legal supletivo. Comunicam-se os bens adquiridos onerosamente na constância do casamento. Excluem-se bens anteriores, doações e heranças (bens particulares).
* **Separação Obrigatória / Legal (Art. 1.641 do CC):** Imposta por lei a maiores de 70 anos, pessoas que necessitarem de suprimento judicial para casar e pessoas com causa suspensiva (ex: viúvo/divorciado sem partilha pendente).
  * *Súmula 377 do STF / Jurisprudência STJ:* No regime da separação obrigatória, comunicam-se os bens adquiridos na constância do casamento se comprovado o esforço comum.

---

## 5. Guarda Compartilhada e Dever de Alimentos (Arts. 1.583 a 1.589 do CC e Súmulas STJ)
* **Guarda Compartilhada:** É a regra geral no direito brasileiro. Não significa divisão matemática do tempo de convivência, mas compartilhamento das responsabilidades das decisões sobre a vida do filho.
* **Manutenção do Lar de Referência:** O menor sob guarda compartilhada mantém um lar principal de referência.
* **Guarda Não Exime Alimentos:** A fixação de guarda compartilhada **NÃO afasta a obrigação de prestar alimentos** pelo genitor que não reside habitualmente no lar de referência.
* **Exoneração Automática Proibida (Súmula 358 do STJ):** A maioridade do filho (18 anos) não extingue automaticamente o dever de prestar alimentos. É indispensável ajuizar Ação de Exoneração com contraditório e ampla defesa.
* **Desemprego e Prisão:** Não afastam por si só a obrigação alimentícia do alimentante.
"""

resumo_responsabilidade = """# Resumo Teórico Didático: Responsabilidade Civil
**Profª Roberta Queiroz · Aula Preparatória OAB 47º Exame**

---

## 1. Modalidades de Responsabilidade e Elementos (Arts. 186, 187 e 927 do CC)
* **Responsabilidade Subjetiva (Regra):** Exige conduta (ação/omissão), dano, nexo de causalidade e **culpa em sentido amplo** (dolo ou culpa estrita: negligência, imprudência, imperícia).
* **Responsabilidade Objetiva:** Prescinde da comprovação de culpa. Aplica-se nos casos especificados em lei ou quando a atividade normalmente desenvolvida pelo autor do dano implicar, por sua natureza, risco para os direitos de outrem (teoria do risco criado / Art. 927, parágrafo único).

---

## 2. Prazo Prescricional (Art. 206, § 3º, V do CC)
* A pretensão de reparação civil prescreve em **3 anos**. Se houver relação contratual com inadimplemento geral, aplica-se o prazo geral de **10 anos** (Art. 205 do CC).

---

## 3. Excludentes de Nexo Causal
* Rompem a relação de causa e efeito entre a conduta e o dano, afastando o dever de indenizar:
  * Culpa exclusiva da vítima.
  * Fato exclusivo de terceiro.
  * Caso fortuito e força maior.

---

## 4. Estado de Necessidade e Ação Regressiva (Arts. 188, II, 929 e 930 do CC)
* **Excludente de Ilicitude:** A destruição de coisa alheia ou lesão a pessoa a fim de remover perigo iminente constitui ato lícito (Art. 188, II do CC).
* **Dever de Indenizar o Terceiro Lesado de Boa-Fé:** Se a pessoa lesada não for culpada pelo perigo (ex: condutor que desvia de pedestre imprudente para não atropelá-lo e colide contra o veículo de um terceiro inocente), o autor do dano **deve indenizar o terceiro lesado**.
* **Ação Regressiva (Art. 930 do CC):** Após ressarcir o lesado, o autor do dano terá **direito de regresso** contra o verdadeiro causador da situação de perigo (no exemplo, o pedestre).

---

## 5. Responsabilidade do Incapaz (Art. 928 do CC)
* O incapaz responde pelos prejuízos que causar **apenas se os seus responsáveis não tiverem obrigação de fazê-lo ou não dispuserem de meios suficientes**.
* Trata-se de responsabilidade **subsidiária, mitigada e equitativa** (a indenização não pode privar o incapaz nem os seus dependentes do estritamente necessário à subsistência).

---

## 6. Responsabilidade por Defenestramento e Ruína de Prédio (Arts. 937 e 938 do CC)
* **Coisas Caídas ou Lançadas / Defenestramento (Art. 938 do CC):** Aquele que habitar o prédio ou parte dele responde objetivamente pelo dano proveniente das coisas que dele caírem ou forem lançadas em lugar indevido.
* **Ruína de Prédio (Art. 937 do CC):** O dono do prédio responde pelos danos resultantes de sua ruína se esta provier de falta de reparos cuja necessidade fosse manifesta.
"""

resumo_contratos = """# Resumo Teórico Didático: Direito dos Contratos
**Profª Roberta Queiroz · Aula Preparatória OAB 47º Exame**

---

## 1. Princípios Contratuais e Formação
* **Efeito Inter Partes:** O contrato vincula as partes contratantes. Exceções: estipulação em favor de terceiro, contrato com pessoa a declarar e promessa de fato de terceiro.
* **Transmissão do Direito Real (Art. 1.245 do CC):** O contrato cria a obrigação pessoal de transferir. A transferência da propriedade de bens imóveis só ocorre com o **registro do título no Registro de Imóveis (RI)**, e de bens móveis com a **tradição**.

---

## 2. Compra e Venda entre Ascendente e Descendente (Art. 496 do CC)
* É **anulável** a venda de ascendente a descendente, salvo se os outros descendentes e o cônjuge do alienante houverem expressamente consentido.
* **Prazo Anulatório:** Prazo decadencial de **2 anos** a contar da ciência ou do registro (Art. 179 do CC / Súmula 494 do STF).

---

## 3. Troca ou Permuta (Art. 533 do CC)
* Aplicam-se à troca as mesmas regras da compra e venda.
* É anulável a troca de valores desiguais entre ascendentes e descendentes sem o consentimento dos demais descendentes e do cônjuge.

---

## 4. Contrato de Corretagem (Arts. 725 e 726 do CC)
* **Regra Geral:** A remuneração é devida ao corretor desde que este tenha conseguido o resultado útil previsto no contrato de mediação.
* **Negócio Concluído Directamente Entre as Partes (Art. 726 do CC):** Se o negócio for iniciado e concluído diretamente entre as partes sem mediação eficaz, **nenhuma comissão é devida ao corretor**.
* **Cláusula de Exclusividade Escrita:** Se houver cláusula por escrito de exclusividade, o corretor terá direito à remuneração integral, ainda que o negócio seja realizado diretamente pelo dono, salvo se comprovada inércia ou ociosidade do corretor.

---

## 5. Contrato de Fiança e Benefício de Ordem (Arts. 827, 828 e 1.647 do CC)
* **Outorga Cônjugal (Art. 1.647, III do CC):** A fiança prestada por pessoa casada necessita de autorização do cônjuge (outorga uxória/marital), sob pena de ineficácia total da garantia (Súmula 332 do STJ).
* **Benefício de Ordem (Art. 827 do CC):** O fiador demandado pelo pagamento da dívida tem o direito de exigir, até a contestação da lide, que sejam primeiro executados os bens do devedor principal.
* **Renúncia ao Benefício de Ordem (Art. 828, I do CC):** Se o fiador renunciar expressamente ao benefício de ordem ou se obrigar como **principal pagador / devedor solidário**, ele pode ser cobrado diretamente no mesmo nível do devedor principal.
"""

resumo_obrigacoes = """# Resumo Teórico Didático: Teoria Geral das Obrigações
**Profª Roberta Queiroz · Aula Preparatória OAB 47º Exame**

---

## 1. Formas de Adimplemento e Extinção das Obrigações
* **Pagamento Direto:** Cumprimento da prestação devida na forma e prazo pactuados.
* **Dação em Pagamento (Art. 356 do CC):** Ocorre quando o credor aceita receber prestação diversa da que lhe era devida para extinguir a obrigação.
* **Novação (Art. 360 do CC):** Criação de uma nova obrigação com o objetivo expresso de extinguir a obrigação anterior. Pode ser *objetiva* (mudança de objeto) ou *subjetiva* (mudança de credor ou devedor).
* **Remissão de Dívida (Art. 385 do CC):** É o perdão da dívida concedido pelo credor ao devedor.

---

## 2. Prescrição e Decadência nas Obrigações (Arts. 205 e 206 do CC)
* **Prescrição:** Extingue a pretensão de cobrança do credor contra o devedor.
* **Prazos Prescricionais:** Estão taxativamente previstos nos Arts. 205 (prazo geral de **10 anos**) e 206 (prazos específicos de 1 a 5 anos) do Código Civil.
* **Prestação de Serviços Profissionais (Art. 206, § 5º, I do CC):** A pretensão de cobrança de honorários ou retribuição de serviços prestados por profissionais liberais prescreve em **5 anos**.
* **Interrupção da Prescrição (Art. 202 do CC):** Zera o prazo e pode ocorrer uma **única vez**.

---

## 3. Transmissão das Obrigações (Cessão de Crédito vs Assunção de Dívida)
* **Cessão de Crédito:** Transmissão da posição de credor a terceiro. **Não exige autorização do devedor**, bastando sua notificação para que saiba a quem pagar.
* **Assunção de Dívida (Cessão de Débito):** Substituição do devedor por um terceiro. Exige a **expressa concordância do credor**, pois a solvência do novo devedor afeta diretamente a garantia do crédito.
"""

# Save Resumos
with open(os.path.join(CIVIL_DIR, '08_direito_das_sucessoes_resumo.md'), 'w', encoding='utf-8') as f:
    f.write(resumo_sucessoes)

with open(os.path.join(CIVIL_DIR, '07_direito_de_familia_resumo.md'), 'w', encoding='utf-8') as f:
    f.write(resumo_familia)

with open(os.path.join(CIVIL_DIR, '05_responsabilidade_civil_resumo.md'), 'w', encoding='utf-8') as f:
    f.write(resumo_responsabilidade)

with open(os.path.join(CIVIL_DIR, '04_contratos_resumo.md'), 'w', encoding='utf-8') as f:
    f.write(resumo_contratos)

with open(os.path.join(CIVIL_DIR, '03_obrigacoes_resumo.md'), 'w', encoding='utf-8') as f:
    f.write(resumo_obrigacoes)

print("Todos os 5 resumos em Markdown foram salvos com sucesso!")
