import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

opcao = input("Entre com a opção: ")
while opcao != "sair":
    match opcao:
        case "adicionar":
            titulo = input("Entre com a tarefa: ")
            descricao = input("Entre com a descrição da tarefa: ")

            request = {
                "opcao": "adicionar",
                "dados": {
                    "titulo": titulo,
                    "desc": descricao
                }
            }

            socket.send_json(request)
            reply = socket.recv_string()

            if reply == "OK": #importante, vide codigo servidor
                print("\nTarefa adicionada com sucesso")

            #if reply.split(":")[0] == "ERRO":
                #print(reply, flush=True)
            else:
                print(f"\n {reply}\n", flush = True)

        case "atualizar":
            id_para_atualizar = input("Digite o ID da tarefa que deseja atualizar: ")
            novo_titulo = input(f"Digite o NOVO título da tarefa")
            nova_desc = input(f"Digite a NOVA descrição da tarefa")

            #monta request dnv
            request = {
                "opcao":"atualizar",
                "dados": {
                    "id": id_para_atualizar,
                    "novos_dados":{
                        "titulo": novo_titulo,
                        "desc": nova_desc
                    }
                }
            }

            socket.send_json(request)

            #recebe e mostra a resposta
            reply = socket.recv_string()

            if reply == "OK":
                print(f"\nTarefa {id_para_atualizar} atualizada com sucesso!\n")
            else:
                print(f"\n{reply}\n", flush=True)
        case "deletar":
            # pergunta qual tarefa quer remover
            id_pra_remover = input("Digite o ID da tarefa que quer remover:")
            #monta a requisição com o ID
            request = {
                "opcao":"deletar",
                "dados":{
                    "id":id_pra_remover
                }
            }

            socket.send_json(request)

            # recebe e mostra a resposta
            reply = socket.recv_string()

            if reply == "OK":
                print(f"\nTarefa com ID {id_pra_remover} removida com sucesso!\n")
            else:
                print(f"\n{reply}\n", flush = True)
            
        case "listar":
        #montando requisicao, dados vazios por consistencia
            request = {
                "opcao":"listar",
                "dados":{}
            }
            print("\nBuscando tarefas no servidor")
            socket.send_json(request)

            #recebe tarefa
            lista_de_tarefas = socket.recv_json()

            #exibe as respostas
            print("---Lista de Tarefas---")
            if not lista_de_tarefas:
                print("Nenhuma tarefa encontrada.")
            else:
                for id, tarefa in lista_de_tarefas.items():
                    print(f" ID: {id}")
                    print(f" Titulo: {tarefa['titulo']}")
                    print(f" Descricao: {tarefa['desc']}")
                    print("-"*20)
                print("--------------------\n")
        case "buscar":
            pass
        case _:
            print("Opção não encontrada")

    opcao = input("Entre com a opção: ")
