# Reset de Adaptações do Câmbio 01M

## Quando fazer

- Após qualquer troca de ATF
- Após limpeza ou substituição do corpo de válvulas/solenoides
- Quando as trocas estiverem erráticas após uma falha de bateria
- Como passo de diagnóstico para isolar problema eletrônico vs. mecânico

**SEMPRE trocar o ATF antes do reset** — resetar com ATF velho vai apenas
regravar as mesmas adaptações ruins mais rapidamente.

---

## Método 1: Via VAG-COM (VCDS)

### Reset completo das adaptações

```
1. Conectar VAG-COM/VCDS no OBD-II
2. Selecionar: 02 - Câmbio Automático
3. Ir em: Basic Settings (Configurações Básicas) → Grupo 000
4. Clicar em "Go!" — aguardar beep/confirmação
   Isso zera TODAS as adaptações de marcha
5. Anotar: "Adaptation Reset Complete"
6. Sair do Basic Settings
7. Desligar ignição por 30 segundos
```

### Reset individual por marcha (se quiser granularidade)

```
Módulo 02 → Adaptation (Adaptação):

Canal 1: Pressão de engate 1ª→2ª
Canal 2: Pressão de engate 2ª→3ª
Canal 3: Pressão de engate 3ª→4ª  ← problema relatado (esticando)
Canal 4: Pressão de engate D→2ª  
Canal 5: Ponto de lock-up do conversor
Canal 6: Pressão em marcha lenta

Para zerar individualmente:
  Selecionar canal → valor atual aparece → digitar 0 → "Do it!"
```

---

## Método 2: Sem VAG-COM (reset básico pelo padrão de condução)

Este método não é tão confiável quanto o VAG-COM mas pode ajudar:

```
1. Motor frio, nível de ATF correto
2. Com o carro parado, motor ligado:
   Mover o seletor: P → R → N → D → 3 → 2 → 1 → P
   Aguardar 2 segundos em cada posição
3. Desligar o motor por 5 minutos
4. Ligar novamente
5. Rodar suavemente os primeiros 20 km (o câmbio refaz as adaptações)
```

---

## Procedimento de re-aprendizado após reset

Após o reset, a TCU começa com adaptações zeradas. O re-aprendizado correto:

```
Dia 1 (primeiros 15–20 km):
  - Acelerar suavemente (não passar de 60% do pedal)
  - Deixar o câmbio fazer as trocas normalmente em D
  - Evitar troca manual (tiptronic) nesta fase
  - Pelo menos 5 ciclos completos de P até 4ª em D (parar, acelerar, parar)

Dia 2–3:
  - Aceleração progressivamente mais firme
  - Incluir algumas acelerações a fundo para o câmbio aprender a pressão correta
    em kick-down

Após ~50 km:
  - As trocas devem estar mais firmes e precisas
  - Verificar via VAG-COM se há novas falhas
```

---

## Verificação pós-reset (VAG-COM)

```
Módulo 02 → Blocos de medição → Grupo 003

Campo 1: Temperatura ATF (deve estar ~80°C após 10 min de uso)
Campo 2: Pressão de linha (deve ser ~5–7 bar em marcha lenta D)
Campo 3: Slip do conversor de torque (deve ser 0 em marcha estabilizada)

Se pressão de linha < 4 bar em D com motor quente:
  → Bomba de óleo interna ou solenoide de pressão (N88) com problema
```

---

## Diagnóstico específico: esticando entre 3ª e 4ª

Se após ATF + reset o problema persistir especificamente em 3→4:

```
VAG-COM → Módulo 02 → Adaptation → Canal 3

Valor atual (ex.: 127)
Reduzir em 10–15 unidades (ex.: 112)
Salvar → teste de condução → verificar se troca ficou mais firme/rápida

Repetir em incrementos de 5 até corrigir ou chegar em 90
  (abaixo de 90 pode causar troca muito abrupta)
```

Se o canal 3 estiver no limite e o problema persistir → solenoide MV2
relacionado à 3ª/4ª está desgastado (ver substituição no README.md).
