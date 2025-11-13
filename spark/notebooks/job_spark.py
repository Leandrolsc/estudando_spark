from pyspark.sql import SparkSession

def main():
    """
    Função principal do nosso job Spark.
    """
    # 1. Criação da SparkSession - o ponto de entrada para qualquer funcionalidade Spark
    spark = SparkSession.builder \
        .appName("ProcessamentoClima") \
        .getOrCreate()

    print("Sessão Spark criada com sucesso!")

    # 2. Leitura dos Dados - Caminhos são relativos ao interior do container
    # Lendo dados do volume mapeado /opt/bitnami/spark/data/input/
    try:
        df_clima = spark.read.parquet(
            "/opt/bitnami/spark/data/input/clima_inmet_aggregated.parquet",
            header=True,
            inferSchema=True
        )
        print("Dados de clima carregados:")
        df_clima.show(5)
        df_clima.printSchema()
    except Exception as e:
        print(f"Erro ao ler o arquivo de input. Verifique se 'data/input/clima_inmet_aggregated.parquet' existe. Erro: {e}")
        spark.stop()
        return

    # 3. Transformação - A lógica de negócio
    # Agregando o total de vendas por produto e por ano
    df_agregado = df_clima

    print("Dados agregados:")
    df_agregado.show(10)

    # 4. Escrita dos Dados - Salvando o resultado
    # Salvar em formato Parquet é uma boa prática para performance e compressão
    df_agregado.write.parquet(
        "/opt/bitnami/spark/data/output/clima_agregado",
        mode="overwrite"
    )

    print("Job concluído! Resultado salvo em /data/output/clima_agregado")

    # 5. Encerramento da Sessão
    spark.stop()

if __name__ == "__main__":
    main()