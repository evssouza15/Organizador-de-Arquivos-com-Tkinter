import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Dicionário com extensões e categorias
EXTENSOES = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Músicas": [".mp3", ".wav"],
    "Vídeos": [".mp4", ".mkv", ".avi"],
}

def organizar_pasta(caminho_pasta, barra, janela):
    if not caminho_pasta:
        return

    arquivos = [a for a in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, a))]
    total = len(arquivos)

    if total == 0:
        messagebox.showinfo("Aviso", "Nenhum arquivo encontrado na pasta.")
        return

    contador = {cat: 0 for cat in EXTENSOES.keys()}
    contador["Outros"] = 0

    for i, arquivo in enumerate(arquivos, start=1):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        _, extensao = os.path.splitext(arquivo)
        movido = False

        for categoria, lista_ext in EXTENSOES.items():
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

        # Atualiza a barra de progresso
        barra["value"] = (i / total) * 100
        janela.update_idletasks()

    # Monta relatório final
    relatorio = "\n".join([f"{cat}: {qtd}" for cat, qtd in contador.items()])
    messagebox.showinfo("Relatório", f"Arquivos organizados com sucesso!\n\n{relatorio}")

# Interface gráfica
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        organizar_pasta(pasta, barra, janela)

janela = tk.Tk()
janela.title("Organizador de Arquivos v2")
janela.geometry("450x250")

label = tk.Label(janela, text="Clique no botão para escolher uma pasta:", font=("Arial", 12))
label.pack(pady=20)

botao = tk.Button(janela, text="Selecionar Pasta", command=escolher_pasta, font=("Arial", 12), bg="lightblue")
botao.pack(pady=10)

# Barra de progresso
barra = ttk.Progressbar(janela, length=300, mode="determinate")
barra.pack(pady=20)

janela.mainloop()
