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

diretorioBase = Path('meu_sistema_livraria')
diretorioBackup = diretorioBase / 'backups'
diretorioDados = diretorioBase / 'dados'
diretorioInfos = diretorioBase / 'infos'

# Criação dos diretórios
for diretorio in [diretorioBase, diretorioBackup, diretorioDados, diretorioInfos]:
    diretorio.mkdir(parents=True, exist_ok=True)

# Criação do arquivo de banco de dados
import sqlite3

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
def adicionarLivro(titulo, autor, ano_publicacao, preco):
    cursor.execute('''
        insert into livros (titulo, autor, ano_publicacao, preco)
        values (?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, preco))

    conexao.commit()

# Função para exibir todos os livros
def exibirLivros():
    cursor.execute('''
        select * from livros
    ''')

    livros = cursor.fetchall()

    for livro in livros:
        print(f'{livro[1]} - {livro[2]} - {livro[3]} - R$ {livro[4]}')

# Função para atualizar o preço de um livro
def atualizarPreco(titulo, novoPreco):
    cursor.execute('''
        update livros
        set preco = ?
        where titulo = ?
    ''', (novoPreco, titulo))

    conexao.commit()

# Função para remover um livro
def removerLivro(titulo):
    cursor.execute('''
        delete from livros
        where titulo = ?
    ''', (titulo,))

    conexao.commit()

# Função para buscar livros por autor
def buscarLivrosPorAutor(autor):
    cursor.execute('''
        select * from livros
        where autor = ?
    ''', (autor,))

    livros = cursor.fetchall()

    for livro in livros:
        print(f'{livro[1]} - {livro[2]} - {livro[3]} - R$ {livro[4]}')

