from xmlrpc.client import ServerProxy
from pprint import pprint
import sys

SERVER = 'http://localhost:8000'

def menu():
    print('\n--- CRUD RPC - Contatos (Python XML-RPC) ---')
    print('1) Listar')
    print('2) Criar')
    print('3) Ler por id')
    print('4) Atualizar')
    print('5) Deletar')
    print('0) Sair')

def main():
    proxy = ServerProxy(SERVER, allow_none=True)
    while True:
        menu()
        opt = input('Escolha: ').strip()
        if opt == '1':
            allc = proxy.list()
            pprint(allc)
        elif opt == '2':
            nome = input('Nome: ')
            tel = input('Telefone: ')
            email = input('Email: ')
            criado = proxy.create({'id': 0, 'nome': nome, 'telefone': tel, 'email': email})
            print('Criado:')
            pprint(criado)
        elif opt == '3':
            cid = input('Id: ')
            found = proxy.read(int(cid))
            pprint(found)
        elif opt == '4':
            cid = input('Id a atualizar: ')
            nome = input('Novo nome (enter para manter): ')
            tel = input('Novo telefone (enter para manter): ')
            email = input('Novo email (enter para manter): ')
            upd = {'id': int(cid)}
            if nome: upd['nome'] = nome
            if tel: upd['telefone'] = tel
            if email: upd['email'] = email
            res = proxy.update(upd)
            pprint(res)
        elif opt == '5':
            cid = input('Id a deletar: ')
            ok = proxy.delete(int(cid))
            print('Deletado' if ok else 'Não encontrado')
        elif opt == '0':
            print('Saindo')
            sys.exit(0)
        else:
            print('Opção inválida')

if __name__ == '__main__':
    main()
