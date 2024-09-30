"""Desafio Completo: Sistema de Gerenciamento de Livraria com Arquivos e Banco de Dados
Você foi encarregado de criar um sistema completo de gerenciamento de uma livraria que deverá combinar vários conceitos aprendidos, incluindo:

Manipulação de Arquivos (os e pathlib): Para organizar e manter arquivos de backup da base de dados, cópias dos dados em arquivos CSV e manter um diretório organizado.
SQLite (CRUD): Para gerenciar o banco de dados principal da livraria, que inclui informações sobre livros, autores e preços.
CSV: Para exportar e importar dados da livraria (livros) em formato CSV.
Exclusão e Backup de Arquivos: Para criar cópias de segurança dos dados antes de qualquer modificação maior e limpar arquivos obsoletos.
Requisitos do Sistema:
Banco de Dados:

Deve usar SQLite para armazenar informações sobre os livros, incluindo:
id: chave primária, gerada automaticamente.
titulo: texto.
autor: texto.
ano_publicacao: inteiro.
preco: número flutuante.
Operações CRUD:

Adicionar um novo livro.
Exibir todos os livros cadastrados.
Atualizar o preço de um livro.
Remover um livro.
Buscar livros por autor.
Manipulação de Arquivos:

O sistema deve ser capaz de exportar os dados do banco de dados em formato CSV para um diretório específico.
Deve ser possível importar dados a partir de um arquivo CSV e inseri-los no banco de dados.
O sistema deve criar um backup do banco de dados sempre que novos livros forem adicionados, atualizados ou removidos.
Utilizar a biblioteca pathlib para criar, mover e verificar diretórios de backup.
Requisitos Extras:

O sistema deve criar automaticamente a estrutura de diretórios necessária (usando os.makedirs) se ela não existir.
Criar uma função que faça a limpeza de backups antigos, deixando apenas os 5 últimos arquivos de backup no diretório.

Exemplo de Execução do Sistema:
Ao executar o programa, o sistema deve exibir o seguinte menu:

1. Adicionar novo livro
2. Exibir todos os livros
3. Atualizar preço de um livro
4. Remover um livro
5. Buscar livros por autor
6. Exportar dados para CSV
7. Importar dados de CSV
8. Fazer backup do banco de dados
9. Sair

O usuário deve poder escolher uma das opções e o sistema deverá realizar a operação correspondente. Antes de cada modificação (inserção, atualização ou remoção de um livro), o sistema deve realizar um backup automático do banco de dados.

Estrutura de Arquivos e Diretórios
A estrutura de diretórios será organizada da seguinte forma:


/meu_sistema_livraria/
    /backups/
        backup_livraria_2024-01-01.db
        backup_livraria_2024-01-02.db
        ...
    /data/
        livraria.db
    /exports/
        livros_exportados.csv


Desafios Extras:
    Validação de Entradas: Adicionar validação de entradas para garantir que todos os campos, como o ano e o preço, sejam valores válidos.
    Relatórios: Adicionar a funcionalidade de gerar relatórios em diferentes formatos, como PDF ou HTML, a partir dos dados exportados.
    Esse desafio integra todos os conceitos que você aprendeu até agora sobre SQL, manipulação de arquivos, e CSV, e proporciona uma experiência prática para gerenciar dados de uma livraria."""

import os
from pathlib import Path
import sqlite3
import csv
import shutil
from datetime import datetime

diretorioBase = Path('meu_sistema_livraria')
diretorioBackup = diretorioBase / 'backups'
diretorioDados = diretorioBase / 'dados'
diretorioInfos = diretorioBase / 'infos'

# Criação dos diretórios
for diretorio in [diretorioBase, diretorioBackup, diretorioDados, diretorioInfos]:
    diretorio.mkdir(parents=True, exist_ok=True)

# Criação do arquivo de banco de dados

dbPath = diretorioDados / 'livraria.db'
conexao = sqlite3.connect(dbPath)
cursor = conexao.cursor()

# Criação da tabela de livros
cursor.execute('''
    create table if not exists livros (
        id integer primary key autoincrement,
        titulo text,
        autor text,
        ano_publicacao integer,
        preco real
    )
''')


# Função para adicionar um novo livro
def adicionar_livro(titulo, autor, ano_publicacao, preco):
    cursor.execute('''
        insert into livros (titulo, autor, ano_publicacao, preco)
        values (?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, preco))

    conexao.commit()


# Função para exibir todos os livros
def exibir_livros():
    cursor.execute('''
        select * from livros
    ''')

    livros = cursor.fetchall()

    for livro in livros:
        print(f'{livro[1]} - {livro[2]} - {livro[3]} - R$ {livro[4]}')


# Função para atualizar o preço de um livro
def atualizar_preco(titulo, novoPreco):
    cursor.execute('''
        update livros
        set preco = ?
        where titulo = ?
    ''', (novoPreco, titulo))

    conexao.commit()


# Função para remover um livro
def remover_livro(titulo):
    cursor.execute('''
        delete from livros
        where titulo = ?
    ''', (titulo,))

    conexao.commit()


# Função para buscar livros por autor
def buscar_livros_por_autor(autor):
    cursor.execute('''
        select * from livros
        where autor = ?
    ''', (autor,))

    livros = cursor.fetchall()

    for livro in livros:
        print(f'{livro[1]} - {livro[2]} - {livro[3]} - R$ {livro[4]}')


def exportar():
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()

    with open(diretorioInfos / 'livros_exportados.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)

        escritor_csv.writerow(['Id', 'Título', 'Autor', 'Ano da Publicação', 'Preço'])

        for livro in livros:
            escritor_csv.writerow(livro)

        print('Dados exportados com sucesso!')


def importar(nome_arquivo_csv):
    caminho_arquivo = diretorioInfos / nome_arquivo_csv
    if not caminho_arquivo.exists():
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return

    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)  # Ignora o cabeçalho

        for linha in leitor:
            cursor.execute('''INSERT INTO livros (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)''',
                           (linha[1], linha[2], int(linha[3]), float(linha[4])))

    conexao.commit()
    print("Dados importados com sucesso")



def backup_livros():
    data = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    backup = f"backup_livraria_{data}.db"
    shutil.copy(dbPath, diretorioBackup / backup)

    print(f'Backup criado com sucesso: {backup}')


def limpar_backups():

    backups = sorted(diretorioBackup.glob('*.db'), key=os.path.getmtime, reverse=True)

    if len(backups) > 5:
        for backup in backups[5:]:
            backup.unlink()
            print(f'backup {backup.name} foi excluido')


def menu():
    while True:
        print("\nMENU DE OPÇÕES")
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar livros por autor")
        print("6. Exportar dados para CSV")
        print("7. Importar dados de CSV")
        print("8. Fazer backup do banco de dados")
        print("9. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Título: ").lower()
            autor = input("Autor: ").lower()
            ano_publicacao = int(input("Ano de Publicação: "))
            preco = float(input("Preço: "))
            adicionar_livro(titulo, autor, ano_publicacao, preco)
            backup_livros()
            limpar_backups()
        elif opcao == '2':
            exibir_livros()
        elif opcao == '3':
            titulo = input("Título do livro a ser atualizado: ").lower()
            novoPreco = float(input("Novo preço: "))
            atualizar_preco(titulo, novoPreco)
            backup_livros()
            limpar_backups()
        elif opcao == '4':
            titulo = input("Título do livro a ser removido: ").lower()
            remover_livro(titulo)
            backup_livros()
            limpar_backups()
        elif opcao == '5':
            autor = input("Autor: ").lower()
            buscar_livros_por_autor(autor)
        elif opcao == '6':
            exportar()
        elif opcao == '7':
            arquivo_csv = input("Caminho do arquivo CSV a ser importado: ")
            importar(arquivo_csv)
        elif opcao == '8':
            backup_livros()
        elif opcao == '9':
            conexao.close()
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Executar o menu
menu()


