# RDD (Resilient Distributed Dataset)

## O que é um RDD

O **RDD (Resilient Distributed Dataset)** é a **estrutura de dados fundamental do Apache Spark**, criada para permitir o **processamento paralelo, distribuído e tolerante a falhas** de grandes volumes de dados.  
Em termos simples, um RDD é uma **coleção imutável de objetos distribuídos** pelo cluster, que pode ser processada de forma **paralela e eficiente**.

Cada RDD é dividido em **partições**, que são distribuídas entre os nós do cluster. Isso permite ao Spark executar operações em larga escala de forma distribuída, garantindo **alta performance e tolerância a falhas**.

---

## Principais Características

1. **Imutabilidade:**  
   Um RDD, uma vez criado, não pode ser modificado. Todas as transformações geram novos RDDs.

2. **Distribuição:**  
   Os dados de um RDD são automaticamente distribuídos (particionados) entre os nós do cluster.

3. **Tolerância a falhas:**  
   Caso alguma partição seja perdida, o Spark consegue **reconstruí-la automaticamente** com base no **lineage** (histórico de transformações aplicadas).

4. **Avaliação preguiçosa (Lazy Evaluation):**  
   As transformações em RDDs são avaliadas de forma preguiçosa, ou seja, o Spark só executa as operações quando uma **ação** (como `collect()` ou `count()`) é chamada.

5. **Dois tipos de operações:**
   - **Transformações:** Geram novos RDDs (ex.: `map()`, `filter()`, `flatMap()`, `reduceByKey()`).
   - **Ações:** Executam cálculos e retornam resultados (ex.: `collect()`, `count()`, `saveAsTextFile()`).

---

## Usos Comuns do RDD

O RDD é ideal para cenários onde é necessário **controle detalhado sobre o processamento dos dados** ou quando os dados **não possuem um esquema definido**.  
Alguns casos de uso típicos incluem:

- **ETL distribuído:**  
  Leitura de grandes volumes de dados de fontes diversas, aplicação de transformações e gravação em destinos distribuídos.

- **Processamento de dados não estruturados:**  
  Ideal para logs, arquivos de texto e dados sem esquema fixo.

- **Operações de baixo nível:**  
  Quando se deseja aplicar transformações personalizadas sobre partições específicas.

- **Processamento em memória de alto desempenho:**  
  Utilizando **cache** e **persistência** de RDDs para acelerar operações iterativas.

---

## Limitações do RDD — O Que Não Dá Para Fazer Facilmente

Apesar de ser uma base poderosa do Spark, o uso direto de RDDs apresenta **limitações** em comparação com APIs de nível mais alto, como **DataFrame** e **Dataset**:

1. ❌ **Falta de otimização automática:**  
   O RDD não utiliza o **Catalyst Optimizer**, o que significa que o desempenho depende inteiramente da lógica implementada pelo desenvolvedor.

2. ❌ **Ausência de esquema (schema):**  
   Diferente de DataFrames, o RDD não possui um esquema tabular. Isso impossibilita a execução direta de consultas SQL.

3. ❌ **Integração limitada com SQL:**  
   Não é possível executar queries SQL sobre RDDs. Para isso, é necessário converter o RDD em um DataFrame.

4. ❌ **Código mais verboso e complexo:**  
   Operações simples podem demandar várias linhas de código funcional, dificultando a manutenção e legibilidade.

5. ❌ **Menor eficiência em operações analíticas:**  
   Em tarefas como agregações, joins e filtros complexos, os DataFrames e Datasets são muito mais rápidos, pois se beneficiam da otimização interna do Spark.

---

## Exemplo de Uso (Scala)

```scala
# Criação de um RDD a partir de um arquivo de texto
rdd = spark.sparkContext.textFile("hdfs://caminho/arquivo.txt")

# Transformações: separa palavras e cria pares (palavra, 1)
palavras = rdd.flatMap(lambda linha: linha.split(" "))
pares = palavras.map(lambda palavra: (palavra, 1))

# Redução: conta as ocorrências de cada palavra
contagem = pares.reduceByKey(lambda a, b: a + b)

# Ação: exibe o resultado no console
for palavra, qtd in contagem.collect():
    print(f"{palavra}: {qtd}")
```

---

### Conclusão

O RDD é a base da computação distribuída no Apache Spark, oferecendo flexibilidade, paralelismo e tolerância a falhas.
No entanto, ele é mais adequado para operações de baixo nível ou cenários onde se requer controle detalhado do processamento.
Para tarefas analíticas e manipulação de dados estruturados, recomenda-se o uso de DataFrames ou Datasets, que oferecem melhor desempenho e otimização automática.