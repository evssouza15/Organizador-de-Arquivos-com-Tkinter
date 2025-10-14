import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog

# Dicionário padrão de extensões
EXTENSOES = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Músicas": [".mp3", ".wav"],
    "Vídeos": [".mp4", ".mkv", ".avi"],
}

def organizar_pasta(caminho_pasta, barra, janela, categorias):
    if not caminho_pasta:
        return

    arquivos = [a for a in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, a))]
    total = len(arquivos)

    if total == 0:
        messagebox.showinfo("Aviso", "Nenhum arquivo encontrado na pasta.")
        return

    contador = {cat: 0 for cat in categorias.keys()}
    contador["Outros"] = 0

    for i, arquivo in enumerate(arquivos, start=1):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        _, extensao = os.path.splitext(arquivo)
        movido = False

        for categoria, lista_ext in categorias.items():
            if extensao.lower() in lista_ext:
                pasta_destino = os.path.join(caminho_pasta, categoria)
                os.makedirs(pasta_destino, exist_ok=True)
                shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
                contador[categoria] += 1
                movido = True
                break

        if not movido:
            pasta_outros = os.path.join(caminho_pasta, "Outros")
            os.makedirs(pasta_outros, exist_ok=True)
            shutil.move(caminho_arquivo, os.path.join(pasta_outros, arquivo))
            contador["Outros"] += 1

        barra["value"] = (i / total) * 100
        janela.update_idletasks()

    relatorio = "\n".join([f"{cat}: {qtd}" for cat, qtd in contador.items()])
    messagebox.showinfo("Relatório", f"Arquivos organizados com sucesso!\n\n{relatorio}")

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        organizar_pasta(pasta, barra, janela, EXTENSOES)

def editar_categorias():
    global EXTENSOES
    categoria = simpledialog.askstring("Nova Categoria", "Digite o nome da categoria:")
    if categoria:
        ext = simpledialog.askstring("Extensões", "Digite as extensões separadas por vírgula (ex: .zip,.rar):")
        if ext:
            EXTENSOES[categoria] = [e.strip() for e in ext.split(",")]
            messagebox.showinfo("Sucesso", f"Categoria '{categoria}' adicionada com extensões {EXTENSOES[categoria]}.")

# Interface gráfica
janela = tk.Tk()
janela.title("Organizador de Arquivos v3")
janela.geometry("500x300")

label = tk.Label(janela, text="Clique no botão para escolher uma pasta:", font=("Arial", 12))
label.pack(pady=20)

botao = tk.Button(janela, text="Selecionar Pasta", command=escolher_pasta, font=("Arial", 12), bg="lightblue")
botao.pack(pady=10)

botao_categorias = tk.Button(janela, text="Editar Categorias", command=editar_categorias, font=("Arial", 12), bg="lightgreen")
botao_categorias.pack(pady=10)

barra = ttk.Progressbar(janela, length=350, mode="determinate")
barra.pack(pady=20)

janela.mainloop()
