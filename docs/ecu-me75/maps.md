# Mapas ECU — ME7.5.20 AMK 1.8T

Referência dos principais mapas para remap Stage 1, Stage 2 e conversão etanol.
Os offsets variam por versão de software — usar RomRaider com definições para
localização exata.

---

## Mapas de Combustível

### KFMIOP — Mapa de pressão de injeção base
- **Tipo:** 2D (RPM × carga)
- **Unidade:** mg/Hub (miligramas por curso)
- **Stage 1 gasolina:** +5–8% nas células de carga alta
- **Etanol:** +30–35% em toda a faixa de carga
- **Notas:** Maior mapa de injeção. Ponto de partida para conversão flex.

### KFMIOP_O — Mapa de injeção em overrun (desaceleração)
- Controla cutoff de combustível. Não alterar sem razão específica.

### KFURL — Fator de enriquecimento transitório (aceleração brusca)
- Evita tombamento em aceleração rápida. Aumentar levemente ao subir boost.

### LAMFA — Target lambda (faixa de carga alta)
- **Stock:** ~0,85–0,88 (enriquecimento de proteção)
- **Stage 1 gasolina:** 0,85–0,87 mantém segurança
- **Etanol:** pode ir para 0,90–0,95 (etanol é mais refrigerante)

---

## Mapas de Ignição

### KFZW — Mapa de avanço de ignição principal
- **Tipo:** 3D (RPM × carga)
- **Unidade:** graus ATDC (valores negativos = avanço)
- **Stock AMK:** pico de ~22° em carga máxima
- **Stage 1 gasolina 95:** +1–2° em RPM médio, cuidado em carga total
- **Stage 1 gasolina 98:** +2–4° possível em toda faixa
- **Etanol E100:** +6–10° extra (etanol resiste muito mais a detonação)

### KFZW2 — Mapa de avanço secundário (boost parcial)
- Usado em transições de carga. Ajustar junto com KFZW.

### KFWL — Limite de knock (feedback do sensor)
- Não alterar — é o algoritmo de segurança.

### LADVERS — Retardo de ignição máximo por knock
- Quanto a ECU retarda por evento de knock. Valor seguro de fábrica.

---

## Mapas de Boost (Turbo)

### KFLDRL — Mapa de duty cycle da válvula N75 (wastegate solenoid)
- **Tipo:** 3D (RPM × carga desejada)
- **Unidade:** % duty cycle (maior = mais pressão)
- **Stock:** ~75–80% em carga total
- **Stage 1:** até ~88–92% — não forçar além disso no K03s sem upgrade

### LDRMAX — Limite máximo de boost
- Valor absoluto de proteção. Não alterar antes de ter dados de datalog.

### KFLDIMX — Mapa de carga desejada máxima
- Limita a carga que a ECU persegue. Aumentar conforme boost sobe.

### ATMDRUCK — Compensação de pressão atmosférica
- Não alterar normalmente.

---

## Mapas de Carga (Load)

### KFLOAD — Carga calculada vs. sinal do MAF
- Relaciona tensão do MAF com carga em g/rev.
- Ajustar se instalar MAF maior (ex.: swap para MAF do 2.0T).

### LADEFM — Limite de carga no modo enriquecido
- Teto de carga quando lambda < 1. Aumentar para Stage 2+.

---

## Mapas de Temperatura

### KFKTW — Correção de injeção por temperatura do motor
- Enriquecimento a frio. Não alterar para conversão etanol (gerenciar separado).

### KFETA — Eficiência volumétrica por temperatura
- Compensação de ar admitido vs. temperatura. Relevante para IAT alto no Brasil.

---

## Limitadores

### NMAX — Limitador de RPM (corte de combustível)
- **Stock:** 6.850 rpm
- **Recomendado manter:** 6.800–7.000 rpm

### VMAX — Limitador de velocidade
- **Stock:** 210 km/h (pelo câmbio)
- Remover ou elevar para pista.

---

## Mapa de Referência — Avanço KFZW (valores orientativos Stage 1 gasolina 98)

```
         Carga (mg/Hub)
RPM      40    60    80   100   120   140   160
1000     30    28    26    24    22    20    18
1500     30    28    26    24    22    20    18
2000     28    26    24    22    20    18    17
2500     26    24    22    20    18    17    16
3000     24    22    20    18    17    16    15
3500     22    20    18    17    16    15    14
4000     20    18    17    16    15    14    13
4500     18    17    16    15    14    13    12
5000     18    16    15    14    13    12    11
5500     18    16    14    13    12    11    10
6000     17    15    13    12    11    10     9
6500     16    14    12    11    10     9     8
```

> SEMPRE fazer datalog ao vivo com ME7Logger para verificar knock após qualquer
> alteração. Reduzir avanço imediatamente em qualquer evento de knock.

---

## Ordem de modificação recomendada

1. **Boost (KFLDRL)** — aumentar pressão primeiro, com datalog
2. **Carga máxima (KFLDIMX/LADEFM)** — permitir que a ECU aceite mais carga
3. **Lambda em carga (LAMFA)** — verificar mistura está correta
4. **Ignição (KFZW)** — somente após confirmar sem knock com boost novo
5. **Etanol** — refazer combustível e ignição para E100 se for converter
