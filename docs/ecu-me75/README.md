# ECU Bosch Motronic ME7.5.20 — AMK 1.8T

## Visão geral

A ME7.5 é uma ECU muito bem suportada pela comunidade de tuning. Existe um
ecossistema maduro de ferramentas abertas (EcuFlash, RomRaider, ME7Logger)
e documentação extensiva para o motor AMK.

## Procedimento de leitura

### Opção A: Via OBD (mais simples — funciona se não houver proteção)

```
Hardware: Galletto 1260 clone (~R$80) ou cabo KKL USB
Software: EcuFlash 1.44 (gratuito)

Passos:
1. Conectar Galletto no OBD-II (pino 7 = K-Line)
2. Ignição ON (não ligar o motor)
3. EcuFlash → Connect → selecionar porta COM correta
4. Protocol: KWP2000 / Bosch ME7.x
5. Read ECU → salvar como [DATA_HORA]_AMK_stock.bin (1 MB)
6. Verificar checksum — EcuFlash indica se está correto
7. GUARDAR BACKUP EM LOCAL SEGURO (nuvem + pendrive externo)
```

### Opção B: Via BDM (boot mode — se OBD estiver protegido ou para leitura completa)

```
Hardware: BDM programmer + BDM frame para ME7.5 (CMD BDM100 ou similar)
Pinos BDM na ME7.5.20: conector de 10 pinos no canto da placa principal

Passos:
1. Abrir ECU (4 parafusos torx + vedação de borracha)
2. Encaixar frame BDM nos pinos
3. Ler flash completo (1 MB) + EEPROM (512 bytes)
4. Salvar ambos separadamente
```

> BDM é mais seguro pois lê/grava diretamente no chip — não depende
> do software da ECU estar funcionando. Recomendado para qualquer ECU
> que já tenha sido mexida antes.

## Estrutura da ROM (1 MB)

```
Offset 0x000000 – 0x007FFF: Bootloader (não modificar)
Offset 0x008000 – 0x0FFFFF: Código principal + mapas de calibração

Mapas ficam entre ~0x080000 e ~0x0FFFFF dependendo da versão
```

## Definições de mapas (RomRaider)

Usar arquivo de definições para ME7.5 disponível em:
`maps/definitions/me75_AMK.xml`

Principais mapas documentados em: [maps.md](maps.md)

## Ferramentas

### EcuFlash
- Gratuito, open-source
- Suporte nativo a ME7.5
- Leitura/gravação via OBD e BDM

### RomRaider
- Gratuito, open-source
- Editor de mapas com visualização 3D
- Suporte a datalogs do ME7Logger

### ME7Logger
- Gratuito
- Datalog em tempo real via K-Line
- Registra: RPM, carga, lambda, temperatura, knock, boost, TPS, timing

### WinOLS (opcional, pago)
- Padrão profissional
- Melhor para identificar mapas desconhecidos
- Checksum automático

## Fluxo de trabalho

```
1. Leitura da ROM (backup)
         ↓
2. Identificar versão exata do SW (últimos 4 bytes da ROM)
         ↓
3. Abrir no RomRaider com definições me75_AMK.xml
         ↓
4. Fazer datalog antes de qualquer alteração (baseline)
         ↓
5. Editar mapas conforme objetivo (ver maps.md)
         ↓
6. Calcular checksum (EcuFlash ou WinOLS)
         ↓
7. Gravar na ECU
         ↓
8. Datalog pós-gravação — comparar com baseline
```

## Checksum

O ME7.5 verifica o checksum da ROM na inicialização. **Gravação sem checksum
correto = ECU em modo de emergência (limp mode) ou não inicializa.**

EcuFlash recalcula automaticamente. No RomRaider, usar o plugin de checksum ME7.
