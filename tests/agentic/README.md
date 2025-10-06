## 🧠 Agentic

O módulo **Agentic** do Databot utiliza a estratégia **LLM-AS-A-JUDGE** para verificar a correção das tarefas de um pedido.  

---

### Como funciona

1. **Preparação**
   - É necessário dar **pull do modelo GPT-OSS:20B** no Ollama antes de executar os agentes:
   ```bash
   ollama pull gpt-oss:20b
   ``` 
   - Cada pedido do usuário é dividido por um agente em um conjunto de **tasks**, que serão redirecionadas para os subgrafos correspondentes (por exemplo, `sql` → `analysis`).  

2. **Verificação das tasks**
   - Primeiro, o código faz uma **checagem automática** para garantir que:
     - Todas as tarefas existem.  
     - Estão na **ordem correta**.  
       - Exemplo: se o fluxo é `sql` → `analysis`, a sequência deve ser exatamente essa; caso contrário, recebe **nota 0**.  
   - Em seguida, a **LLM avalia as descrições** das tasks, atribuindo uma nota de **0 a 10** para cada execução, verificando se a descrição faz sentido.  
   - O resultado é dividido por 10 para gerar um valor entre 0 e 1.

3. **Inputs e outputs**
   - Os **inputs** (perguntas e respostas corretas) estão em `questions.json`.  
   - Os **resultados** de cada execução são salvos em `results.json`.  
   - A **acurácia** média do conjunto de tarefas é calculada e salva em `accuracy.json`.  

4. **Execuções**
   - Cada conjunto de perguntas é testado **5 vezes**, e a média das notas das execuções é utilizada para a avaliação final.
   - Verifique se o ambiente virtual está ativado e execute os testes com o seguinte comando: 
   ```bash
   python tests.py
   ```
