# Diagnóstico: Falhas de Ignição ("Pipocando")

## Sintomas típicos no AMK

- Tranco/solavanco em aceleração suave ou cruzeiro
- Perda de potência momentânea
- Consumo aumentado
- Luz de falha piscando (MIL) sob carga
- Falha P0301–P0304 (cilindro específico) ou P0300 (aleatório)

## Causas mais comuns — AMK 1.8T

### 1. Bobinas de ignição (causa #1 — muito comum)

As bobinas N-type do 1.8T VAG são notórias por falhar. Acima de 80.000 km é
praticamente certeza.

**Como diagnosticar:**
```
1. Conectar VAG-COM/VCDS
2. Módulo 01 (Motor) → Blocos de medição → Grupo 14
   - Campo 1–4: adaptação de cilindro (injeção compensatória)
   - Valores acima de ±3 mg/Hub indicam cilindro problemático
3. Ler falhas específicas: P0301 = cil 1, P0302 = cil 2, etc.
```

**Teste rápido sem ferramenta:**
Troque as bobinas de posição (ex.: bobina do cil 1 com cil 3). Se a falha
migrar de cilindro, é a bobina. Se ficar no mesmo cilindro, é vela ou injetor.

**Substituição:**
- Bobinas OEM: Audi/VAG 06B 905 115 E (ou D/F)
- Equivalente: BERU ZSE052 / Bosch 0221604111
- Trocar TODAS as 4 de uma vez — se uma falhou, as outras estão próximas

**Velas junto:**
Ao trocar bobinas, troque as velas:
- NGK PFR7S8EG (original, iridium)
- Gap: 0,7 mm (não forçar para cima sem ajuste no ECU)
- Torque: 25 Nm

---

### 2. MAF sensor (G70) sujo ou com defeito

**Sintomas:** falha suave em aceleração parcial, melhora com acelerador fundo

**Diagnóstico via VAG-COM:**
```
Módulo 01 → Bloco 002
Campo 1: RPM
Campo 2: Carga do motor (g/rev) — deve bater com a tabela abaixo
Campo 3: Temperatura ar admissão

RPM     Carga esperada (WOT, motor quente)
1000    ~1,0 g/rev
2000    ~1,5 g/rev
3000    ~2,2 g/rev
4000    ~2,8 g/rev
```

**Limpeza:** Spray de limpeza de MAF (não WD-40). Secar completamente antes de religar.

**Substituição:** Bosch 0 280 218 088 / VAG 06A 906 461 L

---

### 3. Válvula de desvio (N249 / diverter valve)

A membrana da N249 rasga e deixa vazar boost, causando surging e falhas sob carga.

**Diagnóstico:** Em aceleração brusca, se o carro "engasga" e depois empurra —
é a diverter valve perdendo boost.

**Substituição/delete:**
- OEM: 06A 145 710 N
- Aftermarket: Kit de delete (bloqueia a linha de vácuo da N249) — opção
  mais durável e sem perda de performance

---

### 4. Boost leaks (vazamentos de pressão)

**Teste de fumaça:** conectar gerador de fumaça no intake, pressurizar com
0,5 bar e verificar vazamentos nas mangueiras e abraçadeiras.

**Pontos críticos no AMK:**
- Mangueira do intercooler (inferior)
- Diaphragm do wastegate (N75)
- Junta do intake manifold
- Selagem do MAF no air box

---

### 5. Sonda lambda NB (G39)

Sonda envelhecia fornece leituras erráticas. Com o ECU em malha fechada (idle
e cruzeiro), uma sonda lenta causa correções excessivas de mistura.

**Diagnóstico:**
```
VAG-COM → Módulo 01 → Bloco 003
Campo 1: Tensão lambda (deve oscilar 0,1–0,9V rapidamente)
Campo 3: Correção de mistura (trim) — aceitável até ±10%
```

**Substituição recomendada antes do remap:** Bosch LS4.2 / 0 258 006 028

---

## Checklist pré-remap

- [ ] Bobinas e velas trocadas
- [ ] MAF limpo/verificado
- [ ] Diverter valve (N249) OK
- [ ] Sem boost leaks (teste de fumaça)
- [ ] Sonda lambda respondendo corretamente
- [ ] Distribuição sem ruído (cadeia/tensionador)
- [ ] Pressão de óleo normal (mín. 1,5 bar em marcha lenta quente)
- [ ] Temperatura de arrefecimento estabilizando em ~90°C
- [ ] Sem vazamento pelo turbo (fumaça azul)
- [ ] Backup da ROM original feito e guardado
