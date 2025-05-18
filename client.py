import rpyc
from constRPYC import SERVER_IP, SERVER_PORT

try:
    print(f"Conectando ao servidor em {SERVER_IP}:{SERVER_PORT}...")
    conn = rpyc.connect(SERVER_IP, SERVER_PORT, config={'sync_request_timeout': 30})
    print("Conectado com sucesso!\n")


    print(f"Valor inicial da lista: {conn.root.value()}")
    conn.root.append("Maçã")
    conn.root.append("Banana")
    conn.root.append("Laranja")
    print(f"Após appends: {conn.root.value()}")
    conn.root.insert(1, "Uva")
    print(f"Após insert(1, 'Uva'): {conn.root.value()}") 
    print("-" * 30)


    print(f"Tamanho da lista (length): {conn.root.length()}") 
    print("-" * 30)


    try:
        print(f"Elemento no índice 0 (get(0)): {conn.root.get(0)}")
        print(f"Elemento no índice 2 (get(2)): {conn.root.get(2)}") 
        print("Tentando get(10) (esperado erro de índice):")
        conn.root.get(10)
    except IndexError as e:
        print(f"  ERRO PEGO (get): {e}")
    except Exception as e:
        print(f"  ERRO INESPERADO (get): {e}")
    print("-" * 30)

    try:
        item_removido = conn.root.pop_item(2) 
        print(f"Item removido com pop_item(2): '{item_removido}'. Lista agora: {conn.root.value()}") 
        item_removido_ultimo = conn.root.pop_item() 
        print(f"Item removido com pop_item(): '{item_removido_ultimo}'. Lista agora: {conn.root.value()}") 
        print("Tentando pop_item(5) (esperado erro de índice):")
        conn.root.pop_item(5)
    except IndexError as e:
        print(f"  ERRO PEGO (pop_item): {e}")
    except Exception as e:
        print(f"  ERRO INESPERADO (pop_item): {e}")
    print("-" * 30)


    conn.root.append("Morango")
    conn.root.append("Uva") 
    print(f"Lista antes de remove_item: {conn.root.value()}") 
    try:
        print(f"Resultado de remove_item('Uva'): {conn.root.remove_item('Uva')}") 
        print(f"Lista após remove_item('Uva'): {conn.root.value()}") 
        print("Tentando remove_item('Pera') (esperado erro de valor):")
        conn.root.remove_item("Pera") 
    except ValueError as e:
        print(f"  ERRO PEGO (remove_item): {e}")
    except Exception as e:
        print(f"  ERRO INESPERADO (remove_item): {e}")
    print("-" * 30)


    print(f"Lista antes de clear_all: {conn.root.value()}")
    print(f"Resultado de clear_all(): {conn.root.clear_all()}")
    print(f"Lista após clear_all: {conn.root.value()}") 
    print(f"Tamanho da lista após clear_all: {conn.root.length()}") 
    print("-" * 30)

    print("Testes concluídos.")

except ConnectionRefusedError:
    print(f"ERRO: Conexão recusada. O servidor em {SERVER_IP}:{SERVER_PORT} está rodando e acessível?")
except rpyc.core.protocol.PingError: 
    print(f"ERRO de Ping: A conexão com o servidor em {SERVER_IP}:{SERVER_PORT} pode ter sido perdida ou o servidor não está respondendo a tempo.")
except Exception as e:
    print(f"UM ERRO INESPERADO OCORREU: {e}")
finally:
    if 'conn' in locals() and conn and not conn.closed:
        conn.close()
        print("\nConexão fechada.")