from chatbot.graph.workflow import create_chatbot_graph

app = create_chatbot_graph()

question = "Qual o produto mais caro?"
thread = {"configurable": {"thread_id": "1"}}

for event in app.stream({"messages": [{"role": "user", "content": question}]}, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

question = "Em qual dia da semana possui mais vendas?"

for event in app.stream({"messages": [{"role": "user", "content": question}]}, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

question = "Me diga qual a forma de pagamento mais utilizada"

for event in app.stream({"messages": [{"role": "user", "content": question}]}, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()


    

