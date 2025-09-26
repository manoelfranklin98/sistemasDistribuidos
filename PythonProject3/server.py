from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from model import Contato
import threading

class ContatoService:
    def __init__(self):
        self._store = {}
        self._next_id = 1
        self._lock = threading.Lock()
        # seed inicial
        self.create({'id': 0, 'nome': 'Alice', 'telefone': '(11)1111-1111', 'email': 'alice@example.com'})
        self.create({'id': 0, 'nome': 'Bob', 'telefone': '(22)2222-2222', 'email': 'bob@example.com'})

    def create(self, contato_dict):
        with self._lock:
            cid = self._next_id
            self._next_id += 1
            contato = Contato(cid, contato_dict.get('nome', ''), contato_dict.get('telefone', ''), contato_dict.get('email', ''))
            self._store[cid] = contato
            return contato.to_dict()

    def read(self, cid):
        c = self._store.get(int(cid))
        return c.to_dict() if c else None

    def list(self):
        return [c.to_dict() for c in self._store.values()]

    def update(self, contato_dict):
        cid = int(contato_dict.get('id'))
        with self._lock:
            if cid not in self._store:
                return None
            c = self._store[cid]
            if 'nome' in contato_dict and contato_dict['nome']:
                c.nome = contato_dict['nome']
            if 'telefone' in contato_dict and contato_dict['telefone']:
                c.telefone = contato_dict['telefone']
            if 'email' in contato_dict and contato_dict['email']:
                c.email = contato_dict['email']
            self._store[cid] = c
            return c.to_dict()

    def delete(self, cid):
        cid = int(cid)
        with self._lock:
            return self._store.pop(cid, None) is not None

if __name__ == '__main__':
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    server = SimpleXMLRPCServer(('0.0.0.0', 8000), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()

    service = ContatoService()
    server.register_function(service.create, 'create')
    server.register_function(service.read, 'read')
    server.register_function(service.list, 'list')
    server.register_function(service.update, 'update')
    server.register_function(service.delete, 'delete')

    print('Servidor XML-RPC rodando em http://0.0.0.0:8000/RPC2')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor finalizado')
