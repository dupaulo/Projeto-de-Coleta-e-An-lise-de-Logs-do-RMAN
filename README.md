# Projeto-de-Coleta-e-An-lise-de-Logs-do-RMAN
Este projeto foi desenvolvido como parte de um estudo em engenharia de dados, com o objetivo de coletar, armazenar e analisar informações de logs do RMAN. Utilizando Python, SQLite e Tableau, o projeto visa melhorar o gerenciamento de backups, facilitando a verificação, tomada de decisão e análise de tempo de execução de cada tipo de backup.

 Funcionalidades

- **Leitura dos Logs:** O programa lê os logs do RMAN e extrai as informações relevantes.
- **Armazenamento dos Dados:** As informações extraídas são armazenadas em um banco de dados SQLite de forma estruturada e eficiente.
- **Marcação de Logs:** Após a leitura e armazenamento, os logs são marcados como "completed" para evitar leituras duplicadas.
- **Expurgo de Diretórios:** Opcionalmente, após a leitura e armazenamento, os diretórios de logs podem ser expurgados para liberar espaço de armazenamento.

 Ferramentas Utilizadas

- **Python:** Utilizado para a coleta automatizada e processamento dos logs do RMAN.
- **SQLite:** Banco de dados leve para armazenamento eficiente dos dados coletados.
- **Tableau:** Ferramenta de visualização para criar dashboards interativos e informativos.

 Benefícios

- **Agilidade na Verificação:** Reduz o tempo gasto na verificação dos backups realizados.
- **Melhoria na Tomada de Decisão:** Visualizações interativas ajudam na identificação rápida de problemas e tendências.
- **Análise de Tempo de Execução:** Permite identificar áreas que podem ser otimizadas, melhorando a eficiência do processo de backup.
- **Liberação de Espaço:** Expurgo opcional dos diretórios de logs para garantir a disponibilidade de espaço de armazenamento.

 Como Utilizar

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
