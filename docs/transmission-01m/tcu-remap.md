# Remap TCU 01M — Limitações e Alternativas

## Situação atual do suporte

O remap do TCU do câmbio 01M é **significativamente mais limitado** do que o
remap do ECU do motor. Não existe suporte aberto/gratuito equivalente ao
EcuFlash/RomRaider para o TCU 01M.

Opções existentes:

| Opção | Disponibilidade | Custo | Resultado |
|-------|----------------|-------|-----------|
| Remap TCU profissional (especialistas VAG) | Raro no Brasil | R$ 800–2.000 | Shift points, firmeza |
| Ajuste via adaptações VCDS (canal por canal) | Disponível | R$ 0 (com VCDS) | Parcial |
| Substituição por TCU remapeada | Importar | R$ 500–1.500 | Bom |
| Upgrade para câmbio DSG (swap) | Viável | R$ 3.000–8.000 | Excelente |

---

## O que é possível sem remap TCU

Usando apenas **adaptações via VCDS**, é possível ajustar:

### Firmeza das trocas (Canal 1–4)
- Cada canal controla a pressão de engate de uma troca específica
- Valores mais altos = troca mais firme e rápida
- Limite prático sem hardware novo: ~+15% da pressão original

### Ponto de troca (shift point)
- **NÃO é ajustável diretamente via adaptações VCDS** — os shift points
  estão compilados no firmware da TCU
- O que simula shift points mais altos: o modo **Manual/Tiptronic** (você
  controla manualmente quando trocar)

### Lock-up do conversor de torque (Canal 5)
- Ajustar para lock-up mais cedo = menos escorregamento = melhor eficiência
  em cruzeiro
- Cuidado: lock-up muito cedo em baixa carga causa trancos

---

## Alternativa prática: Modos de condução por pedal

Uma forma de "simular" shift points mais altos sem remap TCU é ajustar o
ECU para que a ECU comunique carga mais alta para a TCU. O 01M usa o sinal
de carga do motor para decidir quando trocar — com o ECU remapeado para mais
torque e carga, o câmbio naturalmente segura as marchas mais.

---

## Para quem precisa de mais controle sobre o câmbio

### Opção 1: Modo Tiptronic aggressivo (curto prazo)
- Usar trocas manuais para controlar RPM
- Trocar de 3→4 apenas acima de 4.500 rpm
- Solução imediata, zero custo

### Opção 2: Remap TCU por especialista (médio prazo)
Especialistas em tuning VAG no Brasil (SP/PR especialmente) têm ferramentas
proprietárias para remap do 01M. Procurar por "remap 01M VAG" — existem
profissionais que fazem o mapa de shift points e lock-up.

### Opção 3: Upgrade TCU de 01M com software de sport
Alguns 01M de outros modelos VAG têm software com shift points mais altos.
Swap de TCU entre modelos compatíveis pode dar resultado.

### Opção 4: Swap para DSG (longo prazo)
O DSG 02E (6 velocidades, usado no A3 8P 2.0T) é o upgrade natural.
- Requer crossmember adaptado, driveshafts, TCM DSG
- Custo total: R$ 4.000–8.000 mas transforma o carro
- Compatível com ECU AMK remapeado via mapa de shift points DSG

---

## Resumo: o que eu faço no câmbio do meu A3

**Prioridade 1 — Esta semana:**
```
1. Trocar ATF por Pentosin ATF1 (R$ 80–120 por 4L)
2. Reset de adaptações via VAG-COM (ou oficina com VCDS)
3. Ajuste do canal 3 de adaptação (3ª→4ª) para valor mais firme
```

**Prioridade 2 — Junto com o remap ECU:**
```
4. Remap TCU por especialista (se encontrar profissional confiável)
   ou aceitar o câmbio com as adaptações otimizadas + modo manual
```

**A troca de ATF + reset de adaptações vai resolver 70–80% dos sintomas
relatados. Fazer isso antes de qualquer outra intervenção.**
