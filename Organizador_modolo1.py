import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Dicionário com extensões e categorias
EXTENSOES = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Músicas": [".mp3", ".wav"],
    "Vídeos": [".mp4", ".mkv", ".avi"],
}

"""Aqui criamos um dicionário onde a chave é a categoria ("Imagens", "Documentos"...).
O valor é uma lista de extensões que pertencem a essa categoria.
Exemplo: Se o arquivo for .jpg, cai em "Imagens"."""

def organizar_pasta(caminho_pasta):
    if not caminho_pasta:
        return

    """Essa função recebe o caminho da pasta escolhida.
        Se não foi escolhida nenhuma, ele apenas sai (return)."""

    for arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        ''' os.listdir(caminho_pasta) → pega todos os nomes de arquivos/pastas dentro da pasta.
            os.path.join() → junta o caminho da pasta + nome do arquivo 
        (evita erro de “barra invertida” no Windows).'''

        # Ignora pastas
        if os.path.isdir(caminho_arquivo):
            continue

        '''Se for uma pasta e não um arquivo, a gente pula (continue).
          Assim, só organizamos arquivos normais.'''
            
        _, extensao = os.path.splitext(arquivo)
        movido = False
        '''os.path.splitext(arquivo) → separa o nome e a extensão.
        Exemplo: "foto.jpg" → ("foto", ".jpg")
        movido = False → variável para controlar se o arquivo foi colocado em alguma categoria.'''


        for categoria, lista_ext in EXTENSOES.items():
            if extensao.lower() in lista_ext:
                pasta_destino = os.path.join(caminho_pasta, categoria)
                os.makedirs(pasta_destino, exist_ok=True)
                shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
                movido = True
                break
            '''Aqui percorremos o dicionário EXTENSOES.

            Se a extensão do arquivo está na lista → achamos a categoria.
            Criamos a pasta da categoria (caso não exista ainda).
            shutil.move() → move o arquivo para dentro da pasta correta.
            movido = True → marcamos que o arquivo já foi organizado.
            break → saímos do loop porque já encontramos o destino.'''


        if not movido:  # Caso a extensão não esteja no dicionário
            pasta_outros = os.path.join(caminho_pasta, "Outros")
            os.makedirs(pasta_outros, exist_ok=True)
            shutil.move(caminho_arquivo, os.path.join(pasta_outros, arquivo))
            messagebox.showinfo("Sucesso", "Arquivos organizados com sucesso!")
            #Se o arquivo não se encaixa em nenhuma categoria, ele vai para uma pasta chamada “Outros”.

# Interface gráfica
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        organizar_pasta(pasta)

janela = tk.Tk()
janela.title("Organizador de Arquivos")
janela.geometry("400x200")

"""Criamos a janela principal.
Definimos título e tamanho."""

label = tk.Label(janela, text="Clique no botão para escolher uma pasta:", font=("Arial", 12))
label.pack(pady=20)
'''Criamos um rótulo de texto.
pack(pady=20) → organiza o componente e adiciona espaçamento vertical.'''
botao = tk.Button(janela, text="Selecionar Pasta", command=escolher_pasta, font=("Arial", 12), bg="lightblue")
botao.pack(pady=10)
'''Criamos um botão.
command=escolher_pasta → quando clicar, chama a função escolher_pasta.'''
janela.mainloop()
'''Mantém a janela aberta até o usuário fechar.
É o “loop principal” do Tkinter.'''