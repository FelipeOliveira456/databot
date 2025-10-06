## 🗄️ SQL

O módulo **SQL** do Databot verifica a **correção das consultas SQL** utilizando o mesmo conjunto de arquivos de testes (`questions.json`, `results.json`) e script (`tests.py`), mas com uma lógica focada na **execução das queries**.

---

### Como funciona

1. **Verificação das consultas**
   - Cada execução compara o **resultado retornado pela query do Databot** com o **resultado esperado**.  
   - Para evitar problemas de ordem nos dados, as listas e tuplas retornadas são **convertidas em conjuntos** antes da comparação.  
   - Se o resultado for equivalente ao esperado, considera-se correto; caso contrário, incorreto.
   - Divide-se as perguntas em fáceis, médias e difíceis e calcula a acurácia delas separadamente.

2. **Inputs e outputs**
   - Os **inputs** (perguntas e respostas corretas) estão em `questions.json`.  
   - Os **resultados** de cada execução são salvos em `results.json`.  
   - A **acurácia** média do conjunto de tarefas é calculada e salva em `accuracy.json`. 

3. **Executando os testes**
   - Cada conjunto de perguntas é testado **10 vezes**, e a média das notas das execuções é utilizada para a avaliação final.
   - Certifique-se de que o ambiente virtual está ativado.  
   - Execute os testes com:
   ```bash
   python tests.py
   ```