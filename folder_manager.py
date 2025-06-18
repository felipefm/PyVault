"""
Módulo para gerenciamento de pastas e seleção de diretórios.
"""
import os
import tkinter as tk
from tkinter import filedialog


def select_folder():
    """
    Abre uma janela de diálogo para o usuário selecionar uma pasta.
    Retorna o caminho da pasta selecionada ou None se cancelado.
    """
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do tkinter
    
    print("Abrindo janela de seleção de pasta...")
    
    folder_path = filedialog.askdirectory(
        title="Selecione a pasta para criptografia/descriptografia",
        initialdir=os.path.expanduser("~")
    )
    
    root.destroy()
    
    if folder_path:
        print(f"Pasta selecionada: {folder_path}")
        return folder_path
    else:
        print("Nenhuma pasta foi selecionada.")
        return None


def manual_folder_input():
    """
    Permite ao usuário digitar manualmente o caminho da pasta.
    Retorna o caminho da pasta ou None se inválido/cancelado.
    """
    while True:
        print("\nDigite o caminho completo da pasta:")
        print("(ou digite 'cancelar' para voltar ao menu)")
        folder_path = input("Caminho da pasta: ").strip()
        
        if folder_path.lower() == 'cancelar':
            return None
        
        folder_path = os.path.expanduser(folder_path)
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            print(f"Pasta válida: {folder_path}")
            return folder_path
        else:
            print("❌ Caminho inválido ou pasta não encontrada. Tente novamente.")


def choose_working_folder():
    """
    Permite ao usuário escolher a pasta de trabalho de diferentes formas.
    Retorna o caminho da pasta selecionada ou None se cancelado.
    """
    while True:
        print("\n" + "="*50)
        print("     SELEÇÃO DE PASTA DE TRABALHO")
        print("="*50)
        print("Como você deseja selecionar a pasta?")
        print("1. Usar janela de seleção (GUI)")
        print("2. Digitar caminho manualmente")
        print("3. Usar pasta atual do script")
        print("4. Cancelar")
        print("="*50)
        
        choice = input("Digite sua escolha (1-4): ").strip()
        
        if choice == '1':
            try:
                folder_path = select_folder()
                if folder_path:
                    return folder_path
                else:
                    print("Seleção cancelada.")
                    continue
            except Exception as e:
                print(f"❌ Erro ao abrir janela de seleção: {e}")
                print("Tentando método manual...")
                folder_path = manual_folder_input()
                if folder_path:
                    return folder_path
                
        elif choice == '2':
            folder_path = manual_folder_input()
            if folder_path:
                return folder_path
                
        elif choice == '3':
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Usando pasta atual do script: {current_dir}")
            return current_dir
            
        elif choice == '4':
            print("Seleção de pasta cancelada.")
            return None
            
        else:
            print("❌ Opção inválida. Digite 1, 2, 3 ou 4.")


def show_folder_info(folder_path):
    """
    Mostra informações sobre a pasta selecionada.
    """
    try:
        total_files = 0
        enc_files = 0
        regular_files = 0
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.startswith('.') and not file.endswith('.py'):
                    total_files += 1
                    if file.endswith('.enc'):
                        enc_files += 1
                    else:
                        regular_files += 1
        
        print(f"\n📁 Informações da pasta: {os.path.basename(folder_path)}")
        print(f"   Caminho completo: {folder_path}")
        print(f"   Total de arquivos: {total_files}")
        print(f"   Arquivos não criptografados: {regular_files}")
        print(f"   Arquivos criptografados (.enc): {enc_files}")
        
    except Exception as e:
        print(f"❌ Erro ao analisar pasta: {e}")