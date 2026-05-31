# Câmbio 01M — Diagnóstico e Correção

## Contexto

O 01M é um câmbio hidromático 4 marchas Aisin, usado no A3 8L automático.
É um câmbio robusto mas **muito sensível à qualidade do ATF** e às adaptações
eletrônicas gravadas na TCU. A maioria dos problemas "elétricos" do 01M tem
origem mecânica (ATF velho, solenoides desgastados, corpo de válvulas sujo).

**Problema relatado no seu A3:**
1. Demora para engatar marchas (principalmente ao sair do neutro/ré)
2. Esticando entre 3ª e 4ª (shift point atrasado, tempo longo de troca)

---

## Por que mecânicos gerais recusam trocar o ATF — e o que fazer

É muito comum oficinas gerais se recusarem a trocar ATF de câmbio com
problema. A lógica deles: "o câmbio já está condenado, se eu trocar o ATF
e piorar, fico com a culpa." Isso é proteção de responsabilidade, não
diagnóstico técnico.

**O que isso significa na prática:**
- Um mecânico que diz "câmbio condenado" sem abrir e inspecionar fisicamente
  está chutando. Os sintomas descritos (delay + 3→4 esticando) têm causas
  muito específicas e tratáveis.
- ATF limpo nunca piora um câmbio com solenoides ou corpo de válvulas sujos —
  pelo contrário. A ideia de "ATF velho está vedando folgas" é um mito para
  câmbios desse tipo.

**O que fazer:**

### Opção A: Fazer você mesmo (mais simples e eficaz)

A troca parcial de ATF no 01M é um procedimento direto que qualquer pessoa
com uma chave allen e um elevador ou rampa consegue fazer. Ver procedimento
abaixo. Você não precisa de mecânico para isso.

### Opção B: Especialista em câmbio automático (não mecânico geral)

Procurar especificamente **retífica de câmbio automático** ou **especialista
em câmbio VAG/Audi**. Essa categoria de profissional tem experiência real
com o 01M e não vai recusar ATF por medo.

O que pedir ao especialista:
1. Diagnóstico via VAG-COM (leitura de falhas do módulo 02)
2. Inspeção do corpo de válvulas
3. Teste de pressão de linha (deve ser ≥5 bar em D com motor quente)
4. Somente após diagnóstico: decidir entre limpeza/solenoides ou retífica

**Custo estimado de um diagnóstico especializado:** R$ 150–300  
**Custo de retífica completa do 01M:** R$ 2.000–4.000  
**Câmbio 01M usado em bom estado (sucata):** R$ 800–1.500  

### Decisão

Se o diagnóstico mostrar:
- Solenoides ruins → R$ 400–600 de peças, resolve
- Corpo de válvulas sujo → R$ 200–400 de mão de obra + limpeza
- Embreagens gastas → retífica ou câmbio usado (avaliar custo-benefício)

**Não "condene" o câmbio sem um diagnóstico real via VAG-COM + inspeção física.**

---

## Diagnóstico inicial (via VAG-COM)

```
Selecionar módulo 02 (câmbio automático)

1. Ler falhas (Fault Codes)
   Falhas comuns:
   - 17088 / P0704: Sensor de posição seletor
   - 17105 / P0721: Sensor de velocidade de saída
   - 17109 / P0725: Sinal de RPM do motor para TCU
   - 18038 / P1630: Falha de comunicação ECU-TCU
   - 00615 / P1618: Solenoide de pressão N88 (MV1)

2. Blocos de medição — Grupo 001
   Campo 1: Marcha atual (D1/D2/D3/D4/R/N/P)
   Campo 2: Pressão do circuito principal (bar)
   Campo 3: Temperatura ATF (deve estabilizar ~80–90°C em uso normal)
   Campo 4: Slip da embreagem torquing convertor

3. Grupo 002
   Campo 1: Solenoide de troca MV1 (%)
   Campo 2: Solenoide de troca MV2 (%)
   Campo 3: Solenoide de pressão (duty cycle)
   Campo 4: Velocidade de saída (rpm)
```

---

## Causas dos problemas relatados

### Causa 1: ATF degradado (causa mais comum — verificar primeiro)

O ATF Pentosin ATF1 original tem vida útil de ~60.000 km. ATF velho:
- Perde viscosidade → solenoides não fazem pressão correta
- Contamina a válvula de retenção → delay no engate
- Oxida → depósitos no corpo de válvulas

**Sintomas específicos:** demora no engate saindo de P/N, troca mole entre marchas.

---

### Causa 2: Adaptações corrompidas na TCU

A TCU aprende continuamente os pontos de pressão e timing das trocas. Se o
veículo rodou muito com ATF velho ou houve falha de bateria, as adaptações
ficam erradas.

**Sintomas específicos:** trocas abruptas ou muito lentas, escorregamento entre
marchas, 3ª para 4ª esticando mais do que as outras.

---

### Causa 3: Solenoides desgastados (MV1, MV2, N88)

Os solenoides do 01M têm vida útil limitada. MV1 e MV2 controlam as trocas;
N88 controla a pressão de linha.

**Sintoma específico:** troca específica sempre com problema (ex.: sempre
estica 3→4 mas as outras são OK).

---

### Causa 4: Corpo de válvulas sujo

Depósitos no corpo de válvulas bloqueiam parcialmente as galerias de óleo,
causando variação de pressão nas trocas.

---

## Plano de ação (ordem)

### Passo 1: Troca do ATF

Este passo resolve 60–70% dos casos de câmbio lento/delay.

**Fluido correto:**
- Pentosin ATF 1 (original VAG — G 052 162 A2)
- Shell L4 / Texaco M-III
- **NÃO usar ATF Dexron III genérico** — causa vazamentos nas vedações

**Procedimento de troca parcial:**

```
Materiais:
- 4 litros de ATF Pentosin ATF1
- Chave allen 17mm (tampão de dreno)
- Balde

1. Elevar o carro com o motor FRIO (ATF a ~20°C)
2. Localizar tampão de dreno (parte inferior da carcaça, lado direito)
3. Drenar ~3,5 litros (esperar 10 min até parar de escorrer)
4. Roscar tampão com vedante novo (torque: 30 Nm)
5. Completar pelo tubo de nível (acesso pelo capô, tubo amarelo)
   Nível correto: entre as marcas MIN/MAX com fluido FRIO
6. Dar partida, selecionar cada posição (P-R-N-D) 2x cada, aguardar 1 min
7. Verificar nível novamente (pode ter baixado ligeiramente)

Para troca mais completa: repetir o processo 3x com 40 km de intervalo
(método de diluição — remove mais ATF contaminado do conversor de torque)
```

### Passo 2: Reset de adaptações

**FAZER SOMENTE APÓS A TROCA DO ATF.**

Ver procedimento completo em: [adaptation-reset.md](adaptation-reset.md)

### Passo 3: Limpeza do corpo de válvulas

Se após ATF + reset ainda houver problemas:

```
Requer remoção do câmbio (ou pelo menos baixar para acessar o VB)
1. Remover corpo de válvulas (6 parafusos torx T27)
2. Limpeza com spray de carburador + jato de ar comprimido
3. Verificar desgaste nas laterais dos solenoides (lâminas internas)
4. Substituir solenoides se desgastados: MV1 (01M 927 365) / MV2 (01M 927 365 A)
5. Montar com ATF novo como lubrificante
```

### Passo 4: Solenoides novos

Se limpeza não resolver — substituir MV1, MV2 e N88:

| Componente | Referência VAG | Custo estimado |
|------------|---------------|----------------|
| Solenoide MV1 | 01M 927 365 | R$ 80–150 |
| Solenoide MV2 | 01M 927 365 A | R$ 80–150 |
| Solenoide pressão N88 | 09B 927 365 F | R$ 120–200 |
| Kit vedações | 01M 398 009 | R$ 60–100 |
