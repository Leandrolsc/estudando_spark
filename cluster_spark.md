# ✨ Entendendo um Cluster Spark
Um cluster Spark é, em essência, um grupo de computadores trabalhando em conjunto para processar grandes volumes de dados de forma muito mais rápida do que um único computador conseguiria. É a base do processamento de Big Data e o que torna o Spark tão poderoso.

A ideia principal é o **processamento paralelo**: em vez de uma única máquina ler um arquivo de 100GB linha por linha, um cluster Spark divide esse arquivo em 100 pedaços de 1GB e coloca 100 máquinas para trabalhar, cada uma em seu próprio pedaço, ao mesmo tempo.

## 🏛️ A Arquitetura de um Cluster
Um cluster Spark Standalone (como o que usamos no Docker) possui dois componentes principais:

1. Nó Mestre (Master Node): É o "cérebro" ou o "gerente" do cluster. Ele não processa os dados, mas coordena todo o trabalho. Sua função é saber quais máquinas estão disponíveis e distribuir as tarefas entre elas. No nosso ``docker-compose.yml``, este é o serviço ``spark-master``.

2. Nós de Trabalho (Worker Nodes): São os "trabalhadores" do cluster. São as máquinas que efetivamente executam as tarefas de processamento de dados. Eles recebem ordens do Master e reportam o status de volta. Em nosso ``docker-compose.yml``, são os serviços ``spark-worker`` e ``spark-worker-2``.

## ⚙️ Como um Job é Executado no Cluster? (O Fluxo de Trabalho)
Entender este fluxo é crucial para depurar e otimizar seus jobs. Vamos ver o que acontece passo a passo quando você executa o comando ``spark-submit`` ou uma célula no Jupyter.

#### Componentes em Jogo:

* **Driver Program:** É o seu processo principal, onde a ``SparkSession`` é criada. Ele roda no Jupyter ou no terminal de onde você lançou o ``spark-submit``.

* **Cluster Manager (Master):** O serviço ``spark-master`` que gerencia os recursos.

* **Executors:** Processos especiais que são lançados nos Worker Nodes para executar as tarefas.

#### O Fluxo Detalhado:

1. **Início (Seu Código):** Você executa seu script. A primeira coisa que seu código faz é criar uma ``SparkSession``. Neste momento, nasce o Driver Program.

2. **Pedido de Recursos:** O Driver Program se conecta ao Master Node (usando o endereço ``spark://spark-master:7077``). Ele diz: "Olá, sou uma nova aplicação e preciso de X cores de CPU e Y de memória para executar meu trabalho".

3. **Alocação:** O Master, que conhece todos os Workers disponíveis, responde ao Driver alocando os recursos. Ele comanda os Worker Nodes para criarem processos Executor. Um Executor é como um "espaço de trabalho" em um Worker, com uma quantidade reservada de CPU e memória.

4. **Distribuição de Tarefas:** Agora, o Driver analisa seu código (ex: ``df.filter(...).groupBy(...)``). Ele o quebra em pequenas unidades de trabalho chamadas Tasks e envia essas tasks diretamente para os Executors nos diferentes Worker Nodes.

5. **Execução Paralela:** Cada Executor processa suas tasks em paralelo, trabalhando em uma partição diferente dos dados. É aqui que a mágica da velocidade acontece.

6. **Retorno do Resultado:** Conforme os Executors terminam suas tasks, eles podem enviar os resultados de volta para o Driver (se você usar uma ação como ``.show()`` ou ``.collect()``) ou salvar o resultado final em um sistema de arquivos (com ``.write.parquet()``).

## 🛠️ Gerenciando Recursos com ``docker-compose.yml``
Seu arquivo ``docker-compose.yml`` é o painel de controle para configurar os recursos do seu cluster local. Você pode simular máquinas mais fracas ou mais fortes alterando algumas variáveis de ambiente nos serviços dos workers.

Vamos analisar o serviço ``spark-worker`` como exemplo:

```yml
# docker-compose.yml

  spark-worker:
    build:
      context: ./spark
    container_name: spark-worker-1
    depends_on:
      - spark-master
    command: bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
    ports:
      - "8081:8081"
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      # --- LINHAS IMPORTANTES PARA GERENCIAR RECURSOS ---
      - SPARK_WORKER_MEMORY=1G   # <-- Altere aqui a memória RAM do worker
      - SPARK_WORKER_CORES=1     # <-- Altere aqui o número de CPUs do worker
      # --------------------------------------------------
    volumes:
      - ./jobs:/opt/bitnami/spark/jobs
      - ./data:/opt/bitnami/spark/data
```
#### Aumentando CPU e Memória
Digamos que você queira simular um worker mais potente. Você pode simplesmente editar essas linhas:

* ``SPARK_WORKER_CORES=2``: Agora este worker dirá ao Master que ele pode executar 2 tarefas simultaneamente.

* ``SPARK_WORKER_MEMORY=4G``: Agora este worker terá 4 Gigabytes de RAM disponíveis para seus executors.

**Exemplo de um worker "turbinado":**

```yml
  spark-worker-turbinado:
    build:
      context: ./spark
    container_name: spark-worker-3 # Novo nome
    ports:
      - "8083:8081" # Nova porta para não haver conflito
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=4G   # <-- 4GB de RAM
      - SPARK_WORKER_CORES=2     # <-- 2 núcleos de CPU
    # ... resto da configuração
```
#### Escalando o Cluster (Adicionando mais Workers)
Para aumentar o poder de processamento total, você pode adicionar mais workers. A maneira mais fácil é copiar e colar o bloco de um serviço spark-worker existente e alterar duas coisas para evitar conflitos:

1. O nome do serviço (ex: ``spark-worker-3``).

2. O ``container_name``.

3. A porta mapeada no host (ex: ``"8083:8081"``).

Lembrete Importante: Sempre que você fizer alterações no seu arquivo ``docker-compose.yml``, precisa parar e recriar os containers para que as mudanças tenham efeito:

```sh
# Parar e remover os containers antigos
docker-compose down

# Subir o ambiente com as novas configurações
docker-compose up -d
```
