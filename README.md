# Forex Bot RSI + MARKOV 

#### Este repositório contém a versão 1.0 do robô de negociação desenvolvido como parte da defesa de Trabalho de Conclusão de Curso (TCC).

Autor:
Fernando Borges Rocha

[![](https://i.ibb.co/nbnGSCM/973a9dae-2058-42ae-930a-8fbba5c5846d.png)](https://bdta.ufra.edu.br/jspui/retrieve/973a9dae-2058-42ae-930a-8fbba5c5846d)

---
#
## Visão Geral:
- O robô implementa uma estratégia de negociação baseada no indicador RSI (Relative Strength Index) e na teoria das cadeias de Markov. Esta versão inicial representa o trabalho realizado como parte dos requisitos para a conclusão bem-sucedida do curso.

## Principais Funcionalidades:

- Este algoritmo faz uso do Relative Strength Index (RSI) para analisar as condições de sobrecompra e sobrevenda. O RSI é empregado como uma ferramenta que contribui nas decisões de compra e venda, fornecendo insights sobre a força da tendência em vigor. No contexto específico deste projeto, o RSI é utilizado para medir a intensidade da tendência, não para identificar pontos de reversão.
- Log detalhado
- [![](https://i.ibb.co/LJCKJZp/log.png)](https://bdta.ufra.edu.br/jspui/retrieve/973a9dae-2058-42ae-930a-8fbba5c5846d) 
#
- Cadeia de Markov: Implementa a teoria das cadeias de Markov para modelar estados futuros do mercado. Informa as decisões de negociação com base nas probabilidades calculadas pela cadeia de Markov.
#
- Armazenamento de Dados:
- Utiliza o SQLite para registrar dados das ordens.(Parcialmente Implementado *)
- [![](https://openfinancecorp.com.br/wp-content/uploads/2024/01/database.png)](https://bdta.ufra.edu.br/jspui/retrieve/973a9dae-2058-42ae-930a-8fbba5c5846d) 
- Fornece uma estrutura organizada para armazenar informações relevantes, incluindo hora, volume, spread, ponto de entrada, ponto de saída, e o resultado (vitória ou derrota). *
- Análises Posteriores: Permite uma análise detalhada do histórico de negociações. Possibilita a identificação de padrões, tendências e áreas de melhoria na estratégia de negociação. *
- Virtualização de Ordens: Oferece a opção de virtualizar ordens, evitando a execução no mercado real. Permite testar estratégias sem impacto financeiro direto.

## Integração com Redes Neurais: 

- Facilita o treinamento de redes neurais com dados ricos e específicos da estratégia. (Em desenvolvimento)

- Treinamento de Modelos: Permite calcular a probabilidade de trades bem-sucedidos, contribuindo para decisões mais informadas. (Em desenvolvimento)


## Observação:

 Este projeto é fornecido "como está" e está sujeito a ajustes e melhorias contínuas. Use-o com cautela e de acordo com suas necessidades específicas.
 
 
 ## Contato:
 
 [![](https://i.ibb.co/bX0sdnX/116340.png)](https://bdta.ufra.edu.br/jspui/retrieve/973a9dae-2058-42ae-930a-8fbba5c5846d) 
 #
 engfernando.atendimento@gmail.com | Apenas por aqui. 
