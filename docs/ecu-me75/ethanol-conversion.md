# Conversão para Etanol — ME7.5.20 AMK 1.8T

## Por que etanol no AMK?

O etanol E100 permite:
- **+10–15% mais potência** (mais boost e avanço de ignição)
- **Temperatura de admissão menor** (efeito refrigerante na vaporização)
- **Combustível mais barato** no Brasil
- **Motor mais seguro** contra knock em dias quentes

O desafio: os injetores de 315 cc/min stock ficam no limite para E100 em boost
mais alto. Com Stage 1 conservador (~0,9–1,0 bar), ainda é viável.

---

## Opções de conversão

### Opção A: Remap direto para E100 (mais simples)

Requisitos:
- Usar **somente etanol** (sem mistura com gasolina)
- Injetores stock (315 cc/min) suportam até ~200cv com E100 se o remap for
  conservador no boost
- Sonda lambda narrow-band precisa ser substituída por **wideband** para
  calibração correta

**Prós:** simples, uma ROM  
**Contras:** não pode misturar combustíveis; partida a frio abaixo de 15°C pode ser difícil

---

### Opção B: Flex Fuel com sensor de etanol (mais versátil)

Adicionar um sensor de etanol (Continental Flex Fuel Sensor ou similar) na linha
de combustível. Um Arduino/módulo intercepta o sinal do MAF e corrige a injeção
proporcionalmente à concentração de etanol detectada.

**Hardware:**
- Sensor de composição flex: ~R$ 150 (sensor universal para linha de 8mm)
- Arduino Nano ou módulo FlexFuel dedicado: ~R$ 80–150
- Não altera a ROM original — funciona como piggyback

**Prós:** pode usar qualquer mistura; ideal para uso misto  
**Contras:** não aproveita todo o potencial de avanço de ignição do etanol sem
remap adicional

---

### Opção C: ROM dual (gasolina / etanol) com switch

Dois arquivos de calibração: um para gasolina, um para etanol.
Trocar a ROM conforme o combustível usando interruptor ou via OBD.

**Prós:** aproveita 100% de cada combustível  
**Contras:** precisar gravar a ECU a cada troca (trabalhoso no dia a dia)

---

## Passo a passo: Remap ECU para E100

### 1. Hardware necessário

- Sonda lambda **wideband** (AEM UEGO, Innovate LC-2, ou similar)
  instalada no coletor de escapamento (~15 cm da saída do cabeçote)
- Injetores limpos (ou substituídos): 315 cc/min stock é o limite
  - Para Stage 2 etanol: upgrade para **550–630 cc/min** (injetores do 2.0T FSI ou similar)

### 2. Parâmetros a modificar na ROM

#### Combustível (aumento de ~30–35%)

```
Mapa KFMIOP (injeção base):
  Multiplicar todas as células por 1,32 como ponto de partida
  Ajuste fino com datalog via wideband

Mapa LAMFA (target lambda em carga):
  Stock gasolina:  0,85–0,87
  Etanol E100:     0,88–0,92 (etanol resfria melhor, pode rodar mais magro)

Mapa KFURL (transitório):
  Aumentar 20–25% para evitar tombamento
```

#### Ignição (ganho de +6–10°)

```
Mapa KFZW — adicionar por faixa:
  2000–3000 rpm: +5–7°
  3000–4500 rpm: +7–10°
  4500–6500 rpm: +6–8°
  (etanol resiste muito mais a detonação — KI (knock index) muito maior que gasolina)

Verificar via datalog: ausência total de eventos de knock (KLOPF = 0)
```

#### Boost

```
Mapa KFLDRL — aumentar duty cycle em +5–8%:
  K03s suporta bem 1,0–1,1 bar com etanol
  Acima de 1,1 bar no K03s original: risco de desgaste precoce do turbo

Mapa LDRMAX — elevar limite para aceitar boost maior
```

### 3. Partida a frio com etanol

O etanol puro tem dificuldade de vaporizar abaixo de ~15°C.
No Brasil (especialmente SP/RS no inverno) pode ser necessário:

- **Partida a frio enriquecida:** ajustar mapa `KFKTW` para mais combustível
  até ~30°C de temperatura do motor
- **Resistência de pré-aquecimento** no intake (solução física)
- Ou manter gasolina para partida (Opção B/C acima)

### 4. Injetores para Stage 2 etanol (>200cv)

| Injetor | CC/min | Impedância | Obs |
|---------|--------|------------|-----|
| Stock AMK | 315 cc | High Z | Limite ~200cv E100 |
| Siemens Deka 60lb | 630 cc | High Z | Drop-in sem troca de resistores |
| Bosch 0280158040 | 550 cc | High Z | Boa opção intermediária |
| USCAR 525cc | 525 cc | High Z | Popular em builds AMK |

**Atenção:** injetores acima de ~550 cc exigem ajuste do mapa de injeção em
marcha lenta para não afogar (pulse width muito pequeno).

---

## Datalog de validação pós-conversão

Campos mínimos para logar via ME7Logger ao fazer pull completo em 3ª marcha:

```
- RPM
- Carga calculada (g/rev)
- Lambda (wideband — externo via serial)
- Temperatura ar admissão (IAT)
- Temperatura arrefecimento
- Knock events (KLOPF 1–4)
- Boost atual (MAP)
- Duty cycle N75
- Avanço real de ignição (ZW)
- Correção lambda (FRA)
```

**Critérios de aprovação:**
- Lambda entre 0,88–0,95 em carga total
- KLOPF = 0 em toda a faixa
- IAT < 50°C (se mais alto: intercooler com água ou spray)
- Temperatura arrefecimento estável < 100°C

---

## Estimativa de potência (K03s original)

| Configuração | Boost | Potência estimada |
|-------------|-------|-------------------|
| Stock gasolina | 0,9 bar | 180cv |
| Stage 1 gasolina 98 | 1,0 bar | 200–210cv |
| Stage 1 etanol E100 | 1,0 bar | 210–225cv |
| Stage 2 etanol + K03s | 1,1 bar | 230–245cv |
| Stage 2 etanol + K04 | 1,3 bar | 260–280cv |
