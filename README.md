# 🚀 Laboratório de Estudos Spark com Docker

Este projeto oferece um ambiente de desenvolvimento Apache Spark completo e pronto para usar, totalmente containerizado com Docker. O objetivo é simular um cluster real, permitindo que você estude, desenvolva e teste jobs de Big Data de forma isolada e prática no seu próprio computador.

## ✨ Principais Funcionalidades

* Ambiente Realista: Simula a arquitetura distribuída de um cluster real (Master/Workers), permitindo desenvolver código que é diretamente portável para ambientes de produção como YARN ou Kubernetes.

* Desenvolvimento Interativo: Inclui um container com Jupyter Lab pré-configurado para se conectar ao cluster, ideal para análise de dados e prototipação.

* Simplicidade: Com apenas um comando (docker-compose up), todo o ambiente é provisionado e fica pronto para uso.

* Isolado e Portátil: Evita a necessidade de instalar Java, Spark ou Python diretamente na sua máquina.


## 🏗️ Estrutura do Projeto

Para uma melhor organização, o projeto segue a estrutura abaixo.

```code
.
├── 🐳 docker-compose.yml   # Orquestra todos os containers do ambiente.
├── 📂 jobs/                 # (Crie esta pasta) Onde seus scripts (.py) e notebooks (.ipynb) devem ficar.
├── 📂 spark/                # (Crie esta pasta) Local para armazenar notebooks e imagem docker do spark.
└── 📜 README.md             # Este arquivo de documentação.
```

## 🛠️ Como Executar o Ambiente

1. **Pré-requisitos**
   - [Docker](https://www.docker.com/get-started) instalado
   - [Docker Compose](https://docs.docker.com/compose/) instalado

2. **Clone o repositório**
   ```sh
   git clone https://github.com/leandrolsc/estudando_spark.git
   cd estudando_spark
   ```

3. **Inicie o Ambiente**

Execute o comando abaixo na raiz do projeto. O ``--build`` é necessário apenas na primeira vez ou quando houver alterações nos arquivos de configuração.

```sh
docker-compose up --build -d
```

O ``-d`` (detached) executa os containers em segundo plano.

4. **Acesse os serviços**

Após a inicialização, os seguintes serviços estarão disponíveis no seu navegador:

* Spark Master UI: http://localhost:8080 (Para monitorar o cluster e os workers)

* Jupyter Lab: http://localhost:8888 (Para desenvolver de forma interativa)


## Observações

* O ambiente Spark está configurado para não exigir autenticação, facilitando o uso local.
---

Sinta-se à vontade para adaptar o ambiente conforme suas necessidades de estudo ou desenvolvimento!