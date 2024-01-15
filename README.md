Robô de Negociação Desenvolvido por Fernando Borges Rocha

Este repositório contém a versão 1.0 do robô de negociação desenvolvido como parte da defesa de Trabalho de Conclusão de Curso (TCC).

Visão Geral:
  O robô implementa uma estratégia de negociação baseada no indicador RSI (Relative Strength Index) 
  e na teoria das cadeias de Markov. Esta versão inicial representa o trabalho realizado como parte dos requisitos para a conclusão bem-sucedida do curso.

Principais Funcionalidades:

Indicador RSI:
  Utiliza o Relative Strength Index (RSI) para análise de condições de sobrecompra e sobrevenda.
  Auxilia nas decisões de compra e venda, identificando potenciais pontos de reversão de tendência.

Cadeia de Markov:
  Implementa a teoria das cadeias de Markov para modelar estados futuros do mercado.
  Informa as decisões de negociação com base nas probabilidades calculadas pela cadeia de Markov.

Armazenamento de Dados:

  Principais Recursos:
    Utiliza o SQLite para registrar dados das ordens. (Ainda em Desenvolvimento)
      Armazenamento SQLite:
        Fornece uma estrutura organizada para armazenar informações relevantes, incluindo hora, volume, spread, ponto de entrada, ponto de saída, e o resultado (vitória ou derrota).

Análises Posteriores:
  Permite uma análise detalhada do histórico de negociações.
  Possibilita a identificação de padrões, tendências e áreas de melhoria na estratégia de negociação.

Virtualização de Ordens:
Simulação de Estratégias:
  Oferece a opção de virtualizar ordens, evitando a execução no mercado real.
  Permite testar estratégias sem impacto financeiro direto.

Integração com Redes Neurais:
  Facilita o treinamento de redes neurais com dados ricos e específicos da estratégia.

Treinamento de Modelos:
  Permite calcular a probabilidade de trades bem-sucedidos, contribuindo para decisões mais informadas.

  
Notas de Lançamento:
  Destaque quaisquer atualizações significativas, correções de bugs ou melhorias planejadas nas versões futuras.

Autor:
Fernando Borges Rocha

Observação: Este projeto é fornecido "como está" e está sujeito a ajustes e melhorias contínuas. Use-o com cautela e de acordo com suas necessidades específicas.
