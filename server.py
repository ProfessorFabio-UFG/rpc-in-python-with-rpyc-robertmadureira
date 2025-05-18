import rpyc
from rpyc.utils.server import ThreadedServer
from constRPYC import SERVER_PORT 

class MyList(rpyc.Service):
    def __init__(self):
        super().__init__()
        self.my_list = []
        print("Serviço MyList inicializado.")

    def on_connect(self, conn):
        print(f"Cliente conectado: {conn}")

    def on_disconnect(self, conn):
        print(f"Cliente desconectado: {conn}")

    def exposed_value(self):
        print(f"RPC: value() -> {self.my_list}")
        return self.my_list

    def exposed_append(self, data):
        self.my_list.append(data)
        print(f"RPC: append({data}) -> {self.my_list}")
        return self.my_list 

    def exposed_insert(self, index, data):
         self.my_list.insert(index,data)
         print(f"RPC: insert({index}, {data}) -> {self.my_list}")
         return self.my_list 

    def exposed_get(self, index):
        try:
            value = self.my_list[index]
            print(f"RPC: get({index}) -> {value}")
            return value
        except IndexError:
            msg = f"Índice {index} fora dos limites para lista de tamanho {len(self.my_list)}."
            print(f"RPC: get({index}) -> Error: {msg}")
            raise IndexError(msg)
        except Exception as e:
            print(f"RPC: get({index}) -> Error: {e}")
            raise e

    def exposed_remove_item(self, value_to_remove):
        try:
            self.my_list.remove(value_to_remove)
            print(f"RPC: remove_item({value_to_remove}) -> {self.my_list}")
            return f"Removida primeira ocorrência de: {value_to_remove}"
        except ValueError:
            msg = f"Valor '{value_to_remove}' não encontrado na lista."
            print(f"RPC: remove_item({value_to_remove}) -> Error: {msg}")
            raise ValueError(msg)
        except Exception as e:
            print(f"RPC: remove_item({value_to_remove}) -> Error: {e}")
            raise e

    def exposed_pop_item(self, index=-1):
        try:
            value = self.my_list.pop(index)
            print(f"RPC: pop_item({index}) -> Removed '{value}'. Lista: {self.my_list}")
            return value
        except IndexError:
            msg = f"Índice de pop {index} fora dos limites para lista de tamanho {len(self.my_list)}."
            print(f"RPC: pop_item({index}) -> Error: {msg}")
            raise IndexError(msg)
        except Exception as e:
            print(f"RPC: pop_item({index}) -> Error: {e}")
            raise e

    def exposed_length(self):
        length = len(self.my_list)
        print(f"RPC: length() -> {length}")
        return length

    def exposed_clear_all(self):
        self.my_list.clear()
        print(f"RPC: clear_all() -> Lista esvaziada.")
        return "Lista esvaziada com sucesso."

if __name__ == "__main__":
    print(f"Iniciando servidor RPyC na porta {SERVER_PORT}...")
    server = ThreadedServer(MyList, port=SERVER_PORT,
                            protocol_config={'allow_public_attrs': False})
    server.start()