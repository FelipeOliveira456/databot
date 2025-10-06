## 🔁 Complete

O módulo **Complete** do Databot realiza o **processamento completo (fim a fim)**, integrando todas as etapas dos subgrafos — **Agentic**, **SQL** e **Analyst** — em uma única execução.  

---

### Como funciona

1. **Fluxo integrado**
   - A partir de um **único pedido do usuário**, o sistema:
     1. **Verifica e estrutura** as tarefas com o módulo **Agentic**.  
     2. **Executa as consultas SQL** correspondentes e gera os **dados em CSV**.  
     3. **Analisa os dados e produz relatórios** visuais e textuais com o módulo **Analyst**.  

2. **Saídas**
   - Os resultados finais são armazenados nos seguintes diretórios:
     - `data/csv/` — arquivos de dados gerados pelas queries SQL.  
     - `data/img/` — gráficos e visualizações produzidos pelo analista.  
     - `data/pdf/` — relatórios analíticos completos em formato PDF.  

3. **Entradas**  
   - As solicitações estão definidas em `questions.json` e foram elaboradas com base no artigo acadêmico da **FUCAPE Business School**, que apresenta modelos de análise de faturamento para pequenas e médias empresas. Esse material serviu como referência conceitual para a formulação dos pedidos:  
   [Como foram suas vendas? 20 modelos para análises de faturamento das PMEs do comércio (FUCAPE, 2022)](https://fucape.br/wp-content/uploads/2022/11/724-COMO-FORAM-SUAS-VENDAS-20-MODELOS-PARA-ANALISES-DE.pdf)


4. **Resultados**
   - Este módulo **não possui arquivos `results.json` nem `accuracy.json`**, pois os resultados **serão discutidos e relatados em um artigo acadêmico (em desenvolvimento)**.  

5. **Execução**
   - Para rodar o fluxo completo:
   ```bash
   python tests.py
   ```
