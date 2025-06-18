"""
Módulo para seleção de arquivos para processamento.
"""
import os


def select_files_to_process(file_list, operation_type):
    """
    Permite ao usuário selecionar quais arquivos processar por índice(s).
    operation_type: 'criptografar' ou 'descriptografar'
    """
    if not file_list:
        print(f"Nenhum arquivo encontrado para {operation_type}.")
        return []

    while True:
        print(f"\n==== Seleção de Arquivos para {operation_type.upper()} ====")
        print(f"Arquivos disponíveis:")
        print("=" * 60)
        
        # Exibe lista numerada dos arquivos
        for i, file_path in enumerate(file_list, 1):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # Tamanho em KB
            print(f"{i:2d}. {file_name} ({file_size:.1f} KB)")
        
        print("=" * 60)
        print("Digite os NÚMEROS dos arquivos que deseja processar, separados por vírgula (ex: 1,3,5).")
        print("Você também pode digitar um intervalo (ex: 1-5 para 1, 2, 3, 4, 5).")
        print("- 'todos': Para selecionar todos os arquivos exibidos.")
        print("- 'cancelar': Para voltar ao menu principal.")
        print("======================================================")
        
        user_input = input(f"Sua seleção para {operation_type}: ").strip().lower()

        if user_input == 'cancelar':
            return []
        
        if user_input == 'todos':
            print(f"Selecionados todos os {len(file_list)} arquivos para {operation_type}.")
            return file_list

        selected_indices = set()  # Usar um set para evitar duplicatas

        # Processa entradas do tipo 1,3,5 ou 1-5
        parts = user_input.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start > end:
                        start, end = end, start  # Permite intervalo invertido (5-1)
                    for i in range(start, end + 1):
                        selected_indices.add(i)
                except ValueError:
                    print(f"Formato de intervalo inválido: '{part}'.")
                    selected_indices.clear()  # Limpa tudo se houver erro
                    break
            else:
                try:
                    selected_indices.add(int(part))
                except ValueError:
                    print(f"Entrada inválida: '{part}'. Por favor, use números, vírgulas, ou intervalos (ex: 1,3, 5-8).")
                    selected_indices.clear()  # Limpa tudo se houver erro
                    break
        
        if not selected_indices:  # Se houve erro na entrada ou nada foi selecionado
            continue  # Volta para o início do loop

        final_selected_files = []
        for index in sorted(list(selected_indices)):  # Garante ordem crescente e remove duplicatas
            if 1 <= index <= len(file_list):
                final_selected_files.append(file_list[index - 1])
            else:
                print(f"Aviso: O índice {index} está fora do intervalo válido (1 a {len(file_list)}). Será ignorado.")
        
        if final_selected_files:
            print(f"\nConfirme os arquivos selecionados para {operation_type}:")
            for file_path in final_selected_files:
                print(f"  - {os.path.basename(file_path)}")
            
            confirm = input(f"\nConfirma a seleção de {len(final_selected_files)} arquivo(s)? (s/N): ").lower()
            if confirm == 's':
                return final_selected_files
            else:
                print("Seleção cancelada. Escolha novamente.")
        else:
            print("Nenhum arquivo válido selecionado com base na sua entrada. Tente novamente.")


def get_files_for_encryption(path_folder):
    """
    Retorna lista de arquivos disponíveis para criptografia.
    """
    available_files = []
    for root, _, files in os.walk(path_folder):
        for file in files:
            full_path = os.path.join(root, file)
            if not full_path.endswith('.enc') and not full_path.endswith('.py') and not file.startswith('.'):
                available_files.append(full_path)
    return available_files


def get_files_for_decryption(path_folder):
    """
    Retorna lista de arquivos disponíveis para descriptografia.
    """
    available_files = []
    for root, _, files in os.walk(path_folder):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path.endswith('.enc'):
                available_files.append(full_path)
    return available_files