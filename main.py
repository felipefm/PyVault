#!/usr/bin/env python3
"""
Aplicação Principal de Criptografia de Arquivos
Permite criptografar e descriptografar arquivos com seleção de pastas via GUI
"""

import sys
import os
from pathlib import Path

# Importar os módulos do sistema
try:
    import crypto_operations
    import file_selector
    import folder_manager
    print("✅ Todos os módulos carregados com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)

# Variável global para armazenar a pasta de trabalho
WORKING_FOLDER = None

def main():
    """Função principal da aplicação"""
    global WORKING_FOLDER
    
    print("=" * 60)
    print("🔐 SISTEMA DE CRIPTOGRAFIA DE ARQUIVOS")
    print("=" * 60)
    
    while True:
        # Mostrar status da pasta de trabalho
        if WORKING_FOLDER:
            print(f"\n✅ Pasta de trabalho: {os.path.basename(WORKING_FOLDER)}")
        else:
            print(f"\n⚠️  Pasta de trabalho não definida")
        
        print("\nEscolha uma opção:")
        print("1. 🔒 Criptografar arquivos")
        print("2. 🔓 Descriptografar arquivos")
        print("3. 🔑 Processar arquivos (modo avançado)")
        print("4. 📁 Gerenciar pastas")
        print("5. ❌ Sair")
        
        choice = input("\nDigite sua escolha (1-5): ").strip()
        
        if choice == "1":
            encrypt_files()
        elif choice == "2":
            decrypt_files()
        elif choice == "3":
            process_files()
        elif choice == "4":
            manage_folders()
        elif choice == "5":
            print("\n👋 Encerrando aplicação...")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

def ensure_working_folder():
    """Garante que uma pasta de trabalho esteja definida"""
    global WORKING_FOLDER
    
    if not WORKING_FOLDER:
        print("\n⚠️  Pasta de trabalho não definida!")
        print("📁 Definindo pasta de trabalho...")
        WORKING_FOLDER = folder_manager.choose_working_folder()
        
        if not WORKING_FOLDER:
            print("❌ Nenhuma pasta foi selecionada.")
            return False
            
        folder_manager.show_folder_info(WORKING_FOLDER)
    
    return True

def encrypt_files():
    """Função para criptografar arquivos"""
    print("\n" + "=" * 40)
    print("🔒 CRIPTOGRAFAR ARQUIVOS")
    print("=" * 40)
    
    # Garantir que temos uma pasta de trabalho
    if not ensure_working_folder():
        return
    
    try:
        print("\nEscolha o tipo de criptografia:")
        print("1. 🔒 Criptografar arquivos selecionados")
        print("2. 📁 Criptografar toda a pasta")
        print("3. ↩️  Voltar ao menu principal")
        
        encrypt_choice = input("\nDigite sua escolha (1-3): ").strip()
        
        if encrypt_choice == "1":
            crypto_operations.encrypt_selected_files(WORKING_FOLDER)
        elif encrypt_choice == "2":
            crypto_operations.encrypt_folder(WORKING_FOLDER)
        elif encrypt_choice == "3":
            return
        else:
            print("❌ Opção inválida!")
            
    except Exception as e:
        print(f"❌ Erro durante a criptografia: {e}")

def decrypt_files():
    """Função para descriptografar arquivos"""
    print("\n" + "=" * 40)
    print("🔓 DESCRIPTOGRAFAR ARQUIVOS")
    print("=" * 40)
    
    # Garantir que temos uma pasta de trabalho
    if not ensure_working_folder():
        return
    
    try:
        print("\nEscolha o tipo de descriptografia:")
        print("1. 🔓 Descriptografar arquivos selecionados")
        print("2. 📁 Descriptografar toda a pasta")
        print("3. ↩️  Voltar ao menu principal")
        
        decrypt_choice = input("\nDigite sua escolha (1-3): ").strip()
        
        if decrypt_choice == "1":
            crypto_operations.decrypt_selected_files(WORKING_FOLDER)
        elif decrypt_choice == "2":
            crypto_operations.decrypt_folder(WORKING_FOLDER)
        elif decrypt_choice == "3":
            return
        else:
            print("❌ Opção inválida!")
            
    except Exception as e:
        print(f"❌ Erro durante a descriptografia: {e}")

def process_files():
    """Função para processamento avançado de arquivos"""
    print("\n" + "=" * 40)
    print("🔧 PROCESSAMENTO AVANÇADO")
    print("=" * 40)
    
    # Garantir que temos uma pasta de trabalho
    if not ensure_working_folder():
        return
    
    try:
        print("\nModo avançado - Escolha a operação:")
        print("1. 🔒 Criptografia seletiva")
        print("2. 🔓 Descriptografia seletiva")
        print("3. 📁 Criptografia completa da pasta")
        print("4. 📁 Descriptografia completa da pasta")
        print("5. ↩️  Voltar ao menu principal")
        
        process_choice = input("\nDigite sua escolha (1-5): ").strip()
        
        if process_choice == "1":
            crypto_operations.encrypt_selected_files(WORKING_FOLDER)
        elif process_choice == "2":
            crypto_operations.decrypt_selected_files(WORKING_FOLDER)
        elif process_choice == "3":
            crypto_operations.encrypt_folder(WORKING_FOLDER)
        elif process_choice == "4":
            crypto_operations.decrypt_folder(WORKING_FOLDER)
        elif process_choice == "5":
            return
        else:
            print("❌ Opção inválida!")
            
    except Exception as e:
        print(f"❌ Erro durante o processamento: {e}")

def manage_folders():
    """Função para gerenciar pastas"""
    global WORKING_FOLDER
    
    print("\n" + "=" * 40)
    print("📁 GERENCIAR PASTAS")
    print("=" * 40)
    
    while True:
        if WORKING_FOLDER:
            print(f"\n📁 Pasta atual: {WORKING_FOLDER}")
        else:
            print("\n📁 Nenhuma pasta definida")
            
        print("\nOpções de gerenciamento:")
        print("1. 📂 Escolher nova pasta de trabalho")
        print("2. 📋 Mostrar informações da pasta atual")
        print("3. 🔄 Redefinir pasta de trabalho")
        print("4. ↩️  Voltar ao menu principal")
        
        folder_choice = input("\nDigite sua escolha (1-4): ").strip()
        
        try:
            if folder_choice == "1":
                new_folder = folder_manager.choose_working_folder()
                if new_folder:
                    WORKING_FOLDER = new_folder
                    print("✅ Pasta de trabalho atualizada!")
                    folder_manager.show_folder_info(WORKING_FOLDER)
                else:
                    print("❌ Nenhuma pasta foi selecionada.")
                    
            elif folder_choice == "2":
                if WORKING_FOLDER:
                    folder_manager.show_folder_info(WORKING_FOLDER)
                else:
                    print("❌ Nenhuma pasta de trabalho definida.")
                    
            elif folder_choice == "3":
                WORKING_FOLDER = None
                print("🔄 Pasta de trabalho resetada!")
                
            elif folder_choice == "4":
                break
            else:
                print("❌ Opção inválida!")
                
        except Exception as e:
            print(f"❌ Erro no gerenciamento de pastas: {e}")

def show_system_info():
    """Mostra informações do sistema"""
    print("\n" + "=" * 40)
    print("ℹ️  INFORMAÇÕES DO SISTEMA")
    print("=" * 40)
    
    print("📦 Módulos carregados:")
    print("   • crypto_operations - Operações de criptografia")
    print("   • file_selector - Seleção de arquivos") 
    print("   • folder_manager - Gerenciamento de pastas")
    
    print("\n🔧 Funcionalidades disponíveis:")
    print("   • Criptografia de arquivos selecionados")
    print("   • Criptografia de pasta completa")
    print("   • Descriptografia de arquivos selecionados")
    print("   • Descriptografia de pasta completa")
    print("   • Seleção de pasta via GUI ou manual")
    print("   • Informações detalhadas de pastas")

if __name__ == "__main__":
    try:
        # Mostrar informações iniciais
        show_system_info()
        
        # Executar aplicação principal
        main()
        
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔐 Sistema de criptografia encerrado.")
        print("📝 Obrigado por usar o sistema!")