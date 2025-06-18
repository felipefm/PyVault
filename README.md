# 🔐 PyVault: Seu Gerenciador de Criptografia de Arquivos Pessoal

Bem-vindo(a) ao **PyVault**, uma ferramenta simples e eficaz para proteger seus arquivos mais importantes. Desenvolvido em Python, este aplicativo permite que você criptografe e descriptografe arquivos e pastas inteiras com facilidade, garantindo que suas informações permaneçam privadas e seguras.

## ✨ Recursos

- **Criptografia e Descriptografia Simples:** Proteja ou acesse seus arquivos com uma senha mestra.
- **Processamento Seletivo:** Escolha arquivos específicos para criptografar ou descriptografar.
- **Processamento de Pasta Completa:** Criptografe ou descriptografe todos os arquivos em uma pasta de uma só vez.
- **Seleção de Pasta Flexível:** Escolha sua pasta de trabalho via interface gráfica, inserção manual ou use a pasta atual do script.
- **Resumo das Operações:** Visualize claramente quais arquivos foram processados com sucesso e quais falharam.
- **Exclusão Opcional de Originais:** Opção de remover os arquivos originais após a criptografia/descriptografia bem-sucedida para maior segurança.

## 🚀 Como Usar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado em seu sistema. Você também precisará das seguintes bibliotecas:

```bash
pip install pycryptodome Pillow
```

### Execução

1. **Clone o Repositório:**
    ```bash
    git clone https://github.com/SeuUsuario/PyVault.git
    cd PyVault
    ```

2. **Execute o Script Principal:**
    ```bash
    python main.py
    ```

Siga as instruções no menu interativo para selecionar a pasta de trabalho e realizar as operações de criptografia ou descriptografia.

## 📁 Estrutura do Projeto

O PyVault é organizado em módulos para facilitar a manutenção e a clareza do código:

```
pasta_do_projeto/
├── main.py              # Ponto de entrada principal e menu interativo.
├── folder_manager.py    # Lógica para seleção e gerenciamento de pastas.
├── crypto_operations.py # Funções de criptografia e descriptografia de arquivos.
├── file_selector.py     # Funções para listar e selecionar arquivos.
└── requirements.txt     # Lista de dependências do projeto.
```

## ⚠️ Aviso Importante sobre Senhas

A segurança dos seus arquivos depende inteiramente da senha que você escolher. **Não há como recuperar uma senha perdida.** Certifique-se de usar uma senha forte e de guardá-la em um local seguro.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias, novas funcionalidades ou correção de bugs.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
