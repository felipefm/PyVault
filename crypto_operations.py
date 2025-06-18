"""
Módulo para operações de criptografia e descriptografia.
"""
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from getpass import getpass

from file_selector import get_files_for_encryption, get_files_for_decryption, select_files_to_process

# Separador para metadados
SEP = b'---\n\n'


def encrypt_file(file_path, password, salt, key_size=32):
    """
    Função auxiliar para criptografar um único arquivo.
    """
    try:
        with open(file_path, 'rb') as f:
            everything = f.read()
    except FileNotFoundError:
        print(f"  ❌ Erro: Arquivo '{file_path}' não encontrado. Pulando.")
        return False
    except Exception as e:
        print(f"  ❌ Erro ao ler o arquivo '{file_path}': {e}. Pulando.")
        return False

    key = PBKDF2(password.encode('utf-8'), salt, dkLen=key_size, count=10000000)

    # Procura por metadados apenas se o separador existir
    try:
        if SEP in everything:
            metadata_end_index = everything.index(SEP) + len(SEP)
            metadata = everything[:metadata_end_index]
            data = everything[metadata_end_index:]
        else:
            metadata = b''
            data = everything
    except ValueError:
        metadata = b''
        data = everything

    try:
        cipher = AES.new(key, AES.MODE_CTR)
        ct = cipher.encrypt(data)
        nonce = cipher.nonce
    except ValueError as e:
        print(f"  ❌ Erro ao criar cifrador AES para '{file_path}': {e}.")
        return False
    except Exception as e:
        print(f"  ❌ Erro durante a criptografia de '{file_path}': {e}. Pulando.")
        return False

    encrypted_file_path = f"{file_path}.enc"

    try:
        with open(encrypted_file_path, 'wb') as f:
            f.write(b'ENC_FILE_V2\n')
            f.write(len(metadata).to_bytes(4, byteorder='big'))
            f.write(metadata)
            f.write(salt)
            f.write(len(nonce).to_bytes(1, byteorder='big'))
            f.write(nonce)
            f.write(ct)
        print(f"  ✅ Criptografado: '{os.path.basename(file_path)}' -> '{os.path.basename(encrypted_file_path)}'")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao escrever o arquivo criptografado '{encrypted_file_path}': {e}. Pulando.")
        if os.path.exists(encrypted_file_path):
            os.remove(encrypted_file_path)
        return False


def decrypt_file_old_format(content, password, key_size=32):
    """
    Descriptografia para arquivos no formato antigo (sem cabeçalho).
    """
    metadata = b''
    start_crypto_data = 0
    
    if SEP in content:
        try:
            metadata_end_index = content.index(SEP) + len(SEP)
            metadata = content[:metadata_end_index]
            start_crypto_data = metadata_end_index
        except ValueError:
            pass
    
    remaining_content = content[start_crypto_data:]
    
    if len(remaining_content) < 32:
        if len(remaining_content) >= 16 + 8:
            for nonce_size_alt in [8, 12]:
                if len(remaining_content) >= 16 + nonce_size_alt:
                    extracted_salt_alt = remaining_content[:16]
                    extracted_nonce_alt = remaining_content[16:16+nonce_size_alt]
                    ct_alt = remaining_content[16+nonce_size_alt:]
                    try:
                        key_alt = PBKDF2(password.encode('utf-8'), extracted_salt_alt, dkLen=key_size, count=10000000)
                        cipher_alt = AES.new(key_alt, AES.MODE_CTR, nonce=extracted_nonce_alt)
                        plaintext_data_alt = cipher_alt.decrypt(ct_alt)
                        if any(char.isprintable() for char in plaintext_data_alt[:100].decode('utf-8', errors='ignore')):
                            return metadata, plaintext_data_alt
                    except Exception:
                        pass
        return None, None

    extracted_salt = remaining_content[:16]
    extracted_nonce = remaining_content[16:32]
    ct = remaining_content[32:]
        
    try:
        key = PBKDF2(password.encode('utf-8'), extracted_salt, dkLen=key_size, count=10000000)
        cipher = AES.new(key, AES.MODE_CTR, nonce=extracted_nonce)
        plaintext_data = cipher.decrypt(ct)
        return metadata, plaintext_data
    except Exception as e:
        print(f"  Depuração: Erro ao tentar formato antigo padrão (salt 16, nonce 16): {e}")
        return None, None


def decrypt_file_new_format(content, password, key_size=32):
    """
    Descriptografia para arquivos no formato novo (com cabeçalho V2).
    """
    offset = len(b'ENC_FILE_V2\n')
    
    if len(content) < offset + 4:
        return None, None

    metadata_size = int.from_bytes(content[offset:offset+4], byteorder='big')
    offset += 4

    if len(content) < offset + metadata_size + 16 + 1:
        return None, None

    metadata = content[offset:offset+metadata_size]
    offset += metadata_size

    extracted_salt = content[offset:offset+16]
    offset += 16

    nonce_size = int.from_bytes(content[offset:offset+1], byteorder='big')
    offset += 1

    if len(content) < offset + nonce_size:
        return None, None

    extracted_nonce = content[offset:offset+nonce_size]
    offset += nonce_size

    ct = content[offset:]

    try:
        key = PBKDF2(password.encode('utf-8'), extracted_salt, dkLen=key_size, count=10000000)
        cipher = AES.new(key, AES.MODE_CTR, nonce=extracted_nonce)
        plaintext_data = cipher.decrypt(ct)
        return metadata, plaintext_data
    except Exception as e:
        print(f"  Depuração: Erro ao tentar formato V2: {e}")
        return None, None


def decrypt_file(file_path, password, key_size=32):
    """
    Função auxiliar para descriptografar um único arquivo.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  ❌ Erro: Arquivo '{file_path}' não encontrado. Pulando.")
        return False
    except Exception as e:
        print(f"  ❌ Erro ao ler o arquivo '{file_path}': {e}. Pulando.")
        return False

    metadata = None
    plaintext_data = None

    if content.startswith(b'ENC_FILE_V2\n'):
        print(f"  📄 Detectado formato V2 para '{os.path.basename(file_path)}'")
        metadata, plaintext_data = decrypt_file_new_format(content, password, key_size)
    
    if metadata is None or plaintext_data is None:
        print(f"  📄 Tentando formato antigo para '{os.path.basename(file_path)}'")
        metadata, plaintext_data = decrypt_file_old_format(content, password, key_size)

    if metadata is None or plaintext_data is None:
        print(f"  ❌ Erro de descriptografia para '{file_path}': Senha incorreta ou arquivo corrompido.")
        return False

    decrypted_file_path = file_path
    if decrypted_file_path.endswith('.enc'):
        decrypted_file_path = decrypted_file_path[:-len('.enc')]
        if decrypted_file_path.endswith('.new'):
            decrypted_file_path = decrypted_file_path[:-len('.new')]
    else:
        decrypted_file_path = file_path + ".decrypted"

    try:
        with open(decrypted_file_path, 'wb') as f:
            f.write(metadata)
            f.write(plaintext_data)
                
        print(f"  ✅ Descriptografado: '{os.path.basename(file_path)}' -> '{os.path.basename(decrypted_file_path)}'")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao escrever o arquivo descriptografado '{decrypted_file_path}': {e}. Pulando.")
        if os.path.exists(decrypted_file_path):
            os.remove(decrypted_file_path)
        return False


def process_files(file_list, operation, password, salt=None):
    """
    Processa uma lista de arquivos com a operação especificada.
    """
    successful_operations = []
    failed_operations = []

    for file_path in file_list:
        print(f"Processando ({operation}): {os.path.basename(file_path)}")
        
        if operation == "Criptografando":
            success = encrypt_file(file_path, password, salt)
        else:  # Descriptografando
            success = decrypt_file(file_path, password)
            
        if success:
            successful_operations.append(file_path)
        else:
            failed_operations.append(file_path)

    return successful_operations, failed_operations


def show_operation_summary(operation, successful, failed):
    """
    Mostra resumo da operação realizada.
    """
    print(f"\n--- Resumo da {operation} ---")
    print(f"Arquivos processados com sucesso: {len(successful)}")
    for f in successful:
        print(f"  - {os.path.basename(f)}")

    if failed:
        print(f"Arquivos que falharam: {len(failed)}")
        for f in failed:
            print(f"  - {os.path.basename(f)}")


def ask_delete_originals(successful_operations, operation):
    """
    Pergunta se deve deletar arquivos originais após operação bem-sucedida.
    """
    if not successful_operations:
        return
        
    if operation == "Criptografia":
        message = "\nDeseja remover os arquivos originais após a criptografia bem-sucedida? (s/N): "
        file_type = "original"
    else:
        message = "\nDeseja remover os arquivos criptografados (.enc) após a descriptografia bem-sucedida? (s/N): "
        file_type = "criptografado"
    
    delete_originals = input(message).lower()
    if delete_originals == 's':
        for file_path in successful_operations:
            try:
                os.remove(file_path)
                print(f"  Removido {file_type}: '{os.path.basename(file_path)}'")
            except Exception as e:
                print(f"  ❌ Erro ao remover o arquivo {file_type} '{os.path.basename(file_path)}': {e}")
    else:
        print(f"Arquivos {file_type}s não serão removidos.")


# Funções principais para serem chamadas pelo main.py
def encrypt_selected_files(path_folder):
    """Criptografia seletiva de arquivos."""
    print(f"Criptografia seletiva na pasta: '{path_folder}'")
    
    available_files = get_files_for_encryption(path_folder)
    selected_files = select_files_to_process(available_files, 'criptografar')
    
    if not selected_files:
        print("Nenhum arquivo selecionado para criptografia.")
        return
    
    password = getpass("Digite a senha de criptografia para os arquivos selecionados: ")
    if not password:
        print("Senha não pode ser vazia. Criptografia abortada.")
        return

    session_salt = get_random_bytes(16)
    print("\n⚠️ IMPORTANTE: Guarde bem a senha que você digitou. Sem ela, seus arquivos NÃO poderão ser recuperados.")
    
    print(f"Iniciando criptografia de {len(selected_files)} arquivo(s)...\n")
    
    successful, failed = process_files(selected_files, "Criptografando", password, session_salt)
    show_operation_summary("Criptografia", successful, failed)
    ask_delete_originals(successful, "Criptografia")
    
    print("\nCriptografia seletiva concluída.")


def decrypt_selected_files(path_folder):
    """Descriptografia seletiva de arquivos."""
    print(f"Descriptografia seletiva na pasta: '{path_folder}'")
    
    available_files = get_files_for_decryption(path_folder)
    selected_files = select_files_to_process(available_files, 'descriptografar')
    
    if not selected_files:
        print("Nenhum arquivo selecionado para descriptografia.")
        return

    password = getpass("Digite a senha de descriptografia para os arquivos selecionados: ")
    if not password:
        print("Senha não pode ser vazia. Descriptografia abortada.")
        return

    print(f"Iniciando descriptografia de {len(selected_files)} arquivo(s)...\n")
    
    successful, failed = process_files(selected_files, "Descriptografando", password)
    show_operation_summary("Descriptografia", successful, failed)
    ask_delete_originals(successful, "Descriptografia")
    
    print("\nDescriptografia seletiva concluída.")


def encrypt_folder(path_folder):
    """Criptografia de todos os arquivos da pasta."""
    print(f"Iniciando criptografia da pasta: '{path_folder}'")

    password = getpass("Digite a senha de criptografia para todos os arquivos: ")
    if not password:
        print("Senha não pode ser vazia. Criptografia abortada.")
        return

    session_salt = get_random_bytes(16)
    print("\n⚠️ IMPORTANTE: Guarde bem a senha que você digitou. Sem ela, seus arquivos NÃO poderão ser recuperados.")

    files_to_process = get_files_for_encryption(path_folder)

    if not files_to_process:
        print("Nenhum arquivo encontrado para criptografar na pasta.")
        return

    print(f"Encontrados {len(files_to_process)} arquivos para criptografar.")

    successful, failed = process_files(files_to_process, "Criptografando", password, session_salt)
    show_operation_summary("Criptografia", successful, failed)
    ask_delete_originals(successful, "Criptografia")

    print("\nCriptografia de pasta concluída.")


def decrypt_folder(path_folder):
    """Descriptografia de todos os arquivos .enc da pasta."""
    print(f"Iniciando descriptografia da pasta: '{path_folder}'")

    password = getpass("Digite a senha de descriptografia para todos os arquivos: ")
    if not password:
        print("Senha não pode ser vazia. Descriptografia abortada.")
        return

    files_to_process = get_files_for_decryption(path_folder)

    if not files_to_process:
        print("Nenhum arquivo .enc encontrado para descriptografar na pasta.")
        return

    print(f"Encontrados {len(files_to_process)} arquivos .enc para descriptografar.")

    successful, failed = process_files(files_to_process, "Descriptografando", password)
    show_operation_summary("Descriptografia", successful, failed)
    ask_delete_originals(successful, "Descriptografia")

    print("\nDescriptografia de pasta concluída.")