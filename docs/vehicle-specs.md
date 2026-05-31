# Especificações do Veículo

## Identificação

| Campo | Valor |
|-------|-------|
| Modelo | Audi A3 (8L) |
| Ano | 2004 |
| Motor | 1.8T 20v — código **AMK** |
| Potência (stock) | 180cv / 132kW @ 5.500 rpm |
| Torque (stock) | 235 Nm @ 1.950–5.000 rpm |
| Câmbio | 01M — Tiptronic 4 marchas |
| Tração | FWD |
| Combustível (stock) | Gasolina — λ=1,0 (sonda narrow-band) |
| Compressão | 9,5:1 |
| Turbo | K03s |
| Pressão de boost (stock) | ~0,9 bar relativo |
| Injetores (stock) | 315 cc/min @ 3 bar |
| Velas | NGK PFR7S8EG (pré-gap 0,7 mm) |
| Bobinas | N-type integrada (1 por cilindro) |

## ECU

| Campo | Valor |
|-------|-------|
| Fabricante | Bosch |
| Modelo | Motronic ME7.5.20 |
| Processador | Motorola MC68336 |
| Flash | 1 MB (am29f800) |
| Interface | K-Line / KWP2000 (pino 7 OBD-II) |
| Endereço CAN | — (sem CAN neste modelo) |
| Número de parte típico | 8N0 906 018 / 8N0 906 018 A/B/C |

## Câmbio

| Campo | Valor |
|-------|-------|
| Código | 01M |
| Tipo | Hidramático 4 velocidades + Reverse |
| Fabricante | Aisin AW |
| Fluido original | ATF Pentosin ATF 1 (ou equivalente Shell LA2634) |
| Capacidade total | ~6 litros |
| Troca parcial (dreno) | ~3,5 litros |
| TCU | Siemens / VDO (integrada no câmbio) |
| Interface TCU | K-Line / KWP2000 |

## Transmissão — relações

| Marcha | Relação |
|--------|---------|
| 1ª | 2,714 |
| 2ª | 1,444 |
| 3ª | 1,000 |
| 4ª | 0,742 |
| Ré | 2,429 |
| Diferencial | 4,154 |

## Pontos de atenção do motor AMK

- Bobinas de ignição **N-type** (encaixe direto na vela) — falham frequentemente acima de 80.000 km
- Valvetrain: cadeia de distribuição com tensionador hidráulico — verificar ruído na partida a frio
- **MAF sensor** (G70) muito sensível a sujeira e vibrações
- **Sonda lambda NB** (LSF 4.2) — substituição recomendada antes do remap
- Seal do eixo do turbo — verificar fumaça azul na aceleração
- **Blow-off valve** (diverter valve N249) — membrana rasga e causa surging

## Pinagem OBD-II relevante

| Pino | Função |
|------|--------|
| 4 | GND chassis |
| 5 | GND sinal |
| 7 | K-Line (ECU + TCU) |
| 15 | L-Line |
| 16 | +12V |
