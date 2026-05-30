# Audi A3 1.8T AMK — Remapeamento ECU + Câmbio + Etanol

**Veículo:** Audi A3 1.8T 180cv Tiptronic 2004 (chassi 8L)
**Motor:** AMK — 1.8T 20v, 180cv / 235Nm de fábrica
**ECU:** Bosch Motronic ME7.5.20
**Câmbio:** 01M — Tiptronic 4 marchas (Aisin)
**Protocolo OBD:** K-Line / KWP2000 (pino 7 e 15 do OBD-II)

---

## Problemas a resolver

| # | Problema | Causa provável | Seção |
|---|----------|---------------|-------|
| 1 | Pipocando / falhando | Bobinas de ignição (N-type) queimando | [Diagnóstico](docs/diagnostics/misfiring.md) |
| 2 | Câmbio demorando engatar | ATF degradado + solenoides gastos + adaptação zerada | [Câmbio 01M](docs/transmission-01m/README.md) |
| 3 | Esticando entre 3ª e 4ª | Ponto de troca no mapa TCU + condição do ATF | [Remap TCU](docs/transmission-01m/tcu-remap.md) |
| 4 | Conversão para etanol | Remapeamento de injeção, ignição e boost | [Etanol](docs/ecu-me75/ethanol-conversion.md) |
| 5 | Performance geral | Remap ECU completo | [ECU ME7.5](docs/ecu-me75/README.md) |

---

## Hardware necessário (sem ferramenta oficial VAG)

### Para o ECU (motor)
| Ferramenta | Custo | Para que serve |
|------------|-------|----------------|
| **Cabo KKL USB** (clone KL001 ou similar) | R$ 40–80 | Ler/gravar ECU via OBD (sem proteção) |
| **Galletto 1260** (clone) | R$ 60–120 | Ler/gravar ECU via OBD — mais confiável |
| **BDM Programmer** (CMD/MPPS com BDM frame) | R$ 300–600 | Leitura em boot mode se ECU tiver proteção ativa |
| **VAG-COM clone** (VCDS HEX-V2 clone) | R$ 100–200 | Diagnóstico, adaptações, leitura de falhas |

> O ME7.5.20 do AMK normalmente permite leitura via OBD com Galletto 1260 ou KKL sem precisar de BDM.

### Para o câmbio (TCU 01M)
| Ferramenta | Custo | Para que serve |
|------------|-------|----------------|
| **VAG-COM clone** | R$ 100–200 | Reset de adaptações, leitura de falhas TCU |
| **VCDS** (original Ross-Tech) | ~R$ 1.500 | Melhor suporte para adaptações 01M |

---

## Software (gratuito e pago)

### ECU
- **EcuFlash** — gratuito, leitura/gravação ME7.x
- **RomRaider** — gratuito, editor de mapas com definições ME7.5
- **WinOLS** — pago (~€400), padrão profissional de edição de mapas
- **ECM Titanium** — pago, interface mais amigável
- **ME7Logger** — gratuito, datalog em tempo real via K-Line

### Câmbio
- **VCDS** / **OBD11** — adaptações e reset
- Remap do TCU 01M: suporte muito limitado, foco em adaptação mecânica

---

## Estrutura do repositório

```
audi/
├── docs/
│   ├── vehicle-specs.md          # Especificações completas
│   ├── diagnostics/
│   │   └── misfiring.md          # Guia diagnóstico falhas de ignição
│   ├── ecu-me75/
│   │   ├── README.md             # ECU ME7.5 — visão geral
│   │   ├── maps.md               # Descrição de todos os mapas relevantes
│   │   └── ethanol-conversion.md # Conversão para etanol passo a passo
│   └── transmission-01m/
│       ├── README.md             # Câmbio 01M — visão geral e problemas
│       ├── adaptation-reset.md   # Reset de adaptações via VCDS
│       └── tcu-remap.md          # Remap TCU (limitações e alternativas)
├── maps/
│   ├── stock/                    # ROM original (backup antes de qualquer mudança)
│   └── modified/                 # Versões remapeadas
├── tools/
│   ├── log_analyzer.py           # Análise de datalogs ME7Logger
│   ├── map_visualizer.py         # Visualização 3D de mapas ECU
│   └── requirements.txt
└── README.md
```

---

## Ordem de trabalho recomendada

1. **Diagnóstico primeiro** — ler falhas com VAG-COM, confirmar bobinas/velas
2. **Backup do ECU** — guardar ROM original antes de qualquer alteração
3. **Resolver mecânica** — bobinas, velas, MAF, boost leaks
4. **Câmbio** — trocar ATF, limpar corpo de válvulas, reset de adaptações
5. **Remap ECU Stage 1** — ajuste de ignição, boost, lambda na gasolina
6. **Conversão etanol** — ajuste de injeção, avanço de ignição, boost

> **NUNCA grave na ECU sem ter o backup da ROM original salvo em local seguro.**
