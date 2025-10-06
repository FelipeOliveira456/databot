## 📊 Analyst

O módulo **Analyst** do Databot é responsável por **gerar e avaliar análises de dados** a partir de arquivos CSV com base em pedidos definidos pelo usuário.  

---

### Como funciona

1. **Entrada**
   - As solicitações do usuário estão em `questions.json`.  
   - O CSV utilizado para cada análise é gerado automaticamente a partir do SQL contido em `data/sql.json`, sendo salvo em `data/csv/`.  

2. **Geração da análise**
   - O agente lê o CSV e cria um **relatório analítico** e **gráficos** conforme o pedido.  
   - As saídas geradas incluem:
     - Relatórios em **PDF** salvos em `data/pdf/`.
     - Gráficos e visualizações em **imagens** dentro de `data/img/`.

3. **Resultados**
   - Os resultados de cada execução são registrados em `results.json`, contendo:
     - A **nota de acurácia** (de **0 a 1**) atribuída **manualmente por um avaliador humano**.  
     - Uma **descrição qualitativa** do relatório, apontando **defeitos**, **qualidades**, **contradições**, presença de **informações irrelevantes** e outros aspectos da análise.  
   - Não há um arquivo `accuracy.json`, pois a avaliação é **subjetiva e interpretativa**.  

4. **Execução**
   - Para rodar os testes e gerar as análises, utilize:
   ```bash
   python tests.py
   ```
