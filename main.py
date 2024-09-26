import os
import sqlite3
import pandas

root = "meu_sistema_livraria"
data = "/data"
export = "/exports"
backup = "/backup"

if not os.path.isdir(root):
    os.makedirs(root)

if not os.path.isdir(f"{root}{export}"):
    os.makedirs(f"{root}{export}")

if not os.path.isdir(f"{root}{backup}"):
    os.makedirs(f"{root}{backup}")

if not os.path.isdir(f"{root}{data}"):
    os.makedirs(f"{root}{data}")

conexao = sqlite3.connect(f"{root}{data}/livraria.db")

cursor = conexao.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicado INTEGER NOT NULL,
        preco FLOAT NOT NULL
    )
''')


def adicionarlivro():

    new_livro = (
        input("Digite o titulo do livro: "),
        input("Digite o nome do autor do livro: "),
        int(input("Digite o ano em que foi publicado: ")),
        float(input("Digite o preço do livro: ")),
    )

    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicado, preco) VALUES (?, ?, ?, ?)
    ''', new_livro)


def listarlivros():
    resposta = pandas.read_sql_query("SELECT * FROM livros", conexao)

    print(resposta, "\n\n")

    while True:
        v_menu = input("Deseja voltar ao menu? [s/n]")

        if v_menu == "s":
            print("\n\n")
            break


def exportcsv():

    tabela = pandas.read_sql_query("SELECT * FROM livros", conexao)

    tabela.to_csv(f"{root}{export}/livros_exportados.csv", index=False, encoding="utf-8")


def backupdb():
    pass


while True:
    print("[1] Adicionar novo livro")
    print("[2] Listar livros")
    print("[3] Atualizar preço do livro")
    print("[4] Remover um livro")
    print("[5] Buscar livros de um autor")
    print("[6] Exportar dados para CSV")
    print("[7] Importar dados para CSV")
    print("[8] Fazer backup do Banco de Dados")
    print("[9] Sair")
    print("<--------------------------------->")
    escolha = int(input("Digite uma das opções acima: "))

    match escolha:
        case 1:
            adicionarlivro()

        case 2:
            listarlivros()

        case 6:
            exportcsv()

        case 9:
            break

    conexao.commit()

conexao.close()
