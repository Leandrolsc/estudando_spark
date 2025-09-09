# Guia Prático: Análise de Dados com Spark no JupyterLab

Parabéns! Seu ambiente interativo está no ar.  
Este notebook é um guia de ponta a ponta sobre como usar o Spark para carregar, transformar e consultar dados.

---

## Passo 1: A Fundação - A SparkSession

Tudo no Spark começa com a **SparkSession**.  
Ela é o seu ponto de entrada para se conectar ao cluster Spark, configurar o ambiente e começar a trabalhar.  

Execute esta célula primeiro. Ela prepara tudo para nós.

```python
# Importa a biblioteca necessária
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, desc, year

# 1. Cria e configura a SparkSession
spark = SparkSession.builder \
    .appName("AnaliseInterativaClima") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.warehouse.dir", "/opt/bitnami/spark/spark-warehouse") \
    .enableHiveSupport() \
    .getOrCreate()

# O que cada linha faz:
# .appName("..."): Dá um nome para sua aplicação, que aparecerá na UI do Spark (localhost:8080).
# .master("..."): Aponta para o nosso cluster Spark no Docker. É aqui que a mágica da conexão acontece.
# .config("..."): Informa ao Spark onde ele deve guardar os dados das tabelas que criarmos.
# .enableHiveSupport(): Ativa o catálogo de tabelas, permitindo usar SQL de forma mais poderosa.

print("SparkSession criada com sucesso!")
print("Pode começar a análise. Use a variável 'spark' para todas as operações.")
print("Acesse a UI do Spark para ver sua aplicação rodando: http://localhost:8080")
```

## Passo 2: Carregando Dados

Vamos carregar um arquivo parquet para dentro de um DataFrame.
Pense em um DataFrame como uma tabela do Excel ou de um banco de dados, mas distribuída em um cluster e com superpoderes.

📌 Obs: Utilize o arquivo parquet que está em data/input/clima_inmet_aggregated.parquet.


Carregando o parquet:

```python
# O caminho é o mesmo que está dentro do container
caminho_arquivo = "data/input/clima_inmet_aggregated.parquet"

# Lendo o arquivo parquet e criando um DataFrame
df_clima = spark.read.parquet(
            "data/input/clima_inmet_aggregated.parquet",
            header=True,
            inferSchema=True
        )

# Vamos inspecionar os dados para ver se carregou corretamente
print("Esquema do DataFrame (tipos de dados das colunas):")
df_clima.printSchema()

print("\nAmostra dos dados (primeiras 5 linhas):")
df_clima.show(5)

```

## Passo 3: Fazendo Consultas - 2 Maneiras Principais

Existem duas formas populares de fazer consultas no Spark:

* API de DataFrames (programática)

* Spark SQL (SQL puro)

### Método 1: API de DataFrames

Pergunta de negócio:
"Quais as cidades brasileiras e seus respectivos estados com maior temperatura média, ordene do maior para o menor?"

```python
# Usando a API de DataFrames para responder à pergunta
med_cidades = df_clima.groupBy("Cidade", "UF") \
    .agg(round(avg("Med_Temperatura"), 2).alias("Temperatura_Média")) \
    .orderBy(desc("Temperatura_Média"))

print("Cidades Brasileiras Temperaturas médias nos ultimos 15 anos:")
med_cidades.show()
```


### Método 2: Spark SQL

Se você vem de um mundo de bancos de dados, vai se sentir em casa.
Para usar SQL, primeiro precisamos registrar o DataFrame como uma view temporária.

Mesma pergunta de negócio:
"Quais as cidades brasileiras e seus respectivos estados com maior temperatura média, ordene do maior para o menor?"

```python
# 1. Registra o DataFrame como uma view temporária
df_clima.createOrReplaceTempView("clima_view")

# 2. Agora, execute uma consulta SQL pura!
sql_query = """
    SELECT
        Cidade,
        UF,
        AVG(Med_Temperatura) AS Temperatura_Média
    FROM
        clima_view
    GROUP BY
        Cidade,
        UF,
    ORDER BY
        Temperatura_Média DESC
"""

clima_medio_df = spark.sql(sql_query)

print("Resultado da consulta com Spark SQL:")
clima_medio_df.show()
```


## Passo 4: Criando Tabelas Permanentes

Views são temporárias e só existem na sessão atual.
Se você quiser que suas tabelas persistam mesmo após reiniciar o notebook, pode salvá-las no warehouse.

```python
# Salvando o DataFrame original como uma tabela gerenciada pelo Spark
df_clima.write.mode("overwrite").saveAsTable("tabela_clima_permanente")

# 'mode("overwrite")' significa que se a tabela já existir, ela será substituída.

print("Tabela criada com sucesso!")

# Agora vamos provar que ela existe no catálogo do Spark
spark.sql("SHOW TABLES").show()
```

Agora, em qualquer outro notebook (ou no mesmo, depois de reiniciar), você pode pular o passo de ler o parquet e consultar a tabela diretamente:

```python
# Lendo diretamente da tabela que acabamos de criar
df_direto_da_tabela = spark.sql("SELECT * FROM tabela_clima_permanente WHERE cidade = 'Belo Horizonte'")

df_direto_da_tabela.show()
```

## Passo 5: Salvando os Resultados

Após sua análise, você provavelmente vai querer salvar o resultado em um arquivo.
O formato Parquet é altamente recomendado por ser otimizado para performance e compressão.

```python
# Vamos salvar o resultado da nossa agregação (Clima de Belo Horizonte)
caminho_saida = "/opt/bitnami/spark/data/output/clima_agregado"

df_direto_da_tabela.write.mode("overwrite").parquet(caminho_saida)

print(f"Resultado salvo com sucesso em '{caminho_saida}' na sua pasta 'data/output'!")
```


---

## 📌 Boas Práticas com Spark

1. Use Particionamento ao Salvar Dados

Sempre que possível, utilize .partitionBy("coluna") ao salvar datasets grandes. Isso melhora a leitura e filtragem posterior.

```python
df_clima.write.partitionBy("Cidade").parquet(caminho_saida)
```

2. Aproveite o Cache para Consultas Repetidas

Se você vai reutilizar um DataFrame várias vezes em consultas diferentes, use .cache() ou .persist().

```python
df_clima.cache()
```

3. Evite collect() em grandes datasets

O método collect() traz todos os dados para o driver. Prefira show() ou operações agregadas.

4. Leia o Plano de Execução

Use .explain() para entender como o Spark vai processar sua query e identificar gargalos.

```python
df_clima.explain()
```

5. Prefira Formatos Otimizados (Parquet/Delta)

Parquet ou Delta são mais rápidos, comprimidos e otimizados para análises.

6. Monitore na UI do Spark

Sempre acompanhe o processamento pelo painel em http://localhost:8080. Ele ajuda a identificar stages lentos ou mal otimizados.
