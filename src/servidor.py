#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Echo - Exemplo de Socket TCP
Devolve qualquer mensagem que recebe (echo).
Pode processar múltiplas conexões sequencialmente.
"""

import socket
import threading

def handle_client(conexao, endereco):
    import time 
    time.sleep(3)
    print(f'[THREAD] Atendendo cliente {endereco}')
    try:
        while True:
            dados = conexao.recv(1024)

            if not dados:
                print(f'[THREAD] Cliente {endereco} desconectou')
                break

            mensagem = dados.decode('utf-8')
            print(f'[THREAD {endereco}] Recebido: {mensagem}')

            resposta = f'Echo: {mensagem}'
            conexao.send(resposta.encode('utf-8'))

    except Exception as e:
        print(f'[ERRO] Cliente {endereco}: {e}')

    finally:
        conexao.close()
        print(f'[THREAD] Encerrada conexão com {endereco}')





servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('localhost', 5000))
servidor.listen(1)
print('Servidor Echo escutando em localhost:5000')

while True:
    print('\nAguardando conexão...')
    conexao, endereco = servidor.accept()
    print(f'Conexão aceita de {endereco}')

    # Criar thread para esse cliente
    thread = threading.Thread(target=handle_client, args=(conexao, endereco))
    thread.daemon = True     # opcional (encerra junto com o programa)
    thread.start()

    print(f'Thread iniciada para {endereco}')