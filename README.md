# vilma_agno

## TODO 

- [ ] (prioritário) dicionário como estrutura de dados à parte ao invés de inserir no prompt 
    - verificar tools de memória: ler documentação, preparar exemplos de código e explicação para próxima reunião
    - tentar incorporar na solução e ver se funciona bem 
    - ao invés de passar lista de imagens no prompt, passar me um arquivo txt ou dizer que elas estão em uma pasta e ver se a llm se vira
    - salvar 100 imagens da base de dados mnist em uma pasta, mas colocar uma quantidade desbalanceada por dígito para que a gente consiga perceber se o modelo estiver roubando e chutando uma quantidade de 1/10 * quantidade de imagens para todas as classes.

- [ ] tentar trocar o gemini por um modelo local (llava1.5, por exemplo) ou algum qwen multimodal para evitar problemas de block do número de requisições. TENTANDO

- [ ] retirar dos prompts tudo que seja relacionado às perguntas que estão sendo feitas depois. Colocar coisas relacionados (e.g., um one-shot example falando de quantidades de pessoas e depois perguntar sobre isso), pode fazer a gente achar que o sistema está funcionando melhor do que realmente está (porque a resposta já está meio que dada no prompt). PRONTO

- [ ] modificar o agente que processa a estrutura de dados para produzir código python ao invés de usar a calculadora. PRONTO

- [ ] colocar prompts em ingles PRONTO

- [ ] ver se é possível fazer apenas o agente que processa imagens receber a imagem como entrada PRONTO (+/-)

- [ ] (pouca prioridade) ver se é possível passar a saída de um agente como entrada para outro como "mídia". Nós gostaríamos de passar o json produzido pelo leitor de imagens para o que gera código. PRONTO

- [ ] verificar se precisa de um agente para a calculadora ou se basta colocar ela como tool do manager. Cada agente que conseguirmos economizar, seria um gasto menor de tokens para uma empresa, por exemplo, que usasse a solução. 
NÃO FUNDIONA MUITO BEM


## Perguntas para investigar (deixar para o final porque é difícil)

- [ ] como iteração pelas imagens acontece? 

- [ ] como manager decide de pode parar e gerar resposta para usuário? ele é invocado ao final da chamada de cada agente?

- [ ] agentes executam em paralelo?