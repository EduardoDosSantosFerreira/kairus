```markdown
# 🔐 KAIRUS - Secure Note Taking Application

<div align="center">
  <strong>🔒 Military-grade encryption • 📁 Password-protected folders • 💾 Auto-save • 🚀 Lightweight</strong>
</div>

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-6.6.0-green.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/AES-256-red.svg" alt="AES-256">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

## 📋 Sobre o Projeto

**KAIRUS** é um aplicativo desktop de anotações seguro, rápido e minimalista, desenvolvido com **Python** e **PySide6**. O aplicativo oferece criptografia AES-256 para todas as notas, suporte a pastas com senha, salvamento automático confiável e uma interface escura moderna.

### ✨ Características Principais

- 🔐 **Criptografia Militar**: AES-256-CBC com PBKDF2 para todas as notas
- 🔑 **Autenticação Segura**: Hash de senha com PBKDF2 (100.000 iterações)
- 📁 **Pastas Protegidas**: Crie pastas com senha para organizar notas sensíveis
- 💾 **Auto-save Inteligente**: Debounce de 1.5s e salvamento periódico a cada 30s
- 🚀 **Vault Automático**: Pasta especial que armazena rascunhos e fallbacks
- 📄 **Exportação Múltipla**: Exporte notas para PDF (Desktop/Documents/Custom) ou TXT
- ⌨️ **Atalhos Globais**: Ctrl+Insert para Quick Note de qualquer lugar
- 🎨 **Interface Dark Moderna**: Design minimalista com paleta de cores profissional

## 🎨 Paleta de Cores

| Elemento | Cor |
|----------|-----|
| Fundo principal | `#0D0D0D` |
| Superfícies (inputs, botões, cards) | `#1C2422` |
| Cor principal (accent) | `#244235` |
| Texto principal | `#F3F8F4` |
| Texto secundário | `#8A9A95` |
| Bordas | `#1A2422` |
| Erro | `#ff6b6b` |
| Sucesso | `#6bc46d` |

## 📁 Estrutura do Projeto

```
kairus/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt       # Dependências do projeto
├── reset_db.py            # Script de reset do banco de dados
│
├── core/                  # Módulos centrais
│   ├── __init__.py
│   ├── note_manager.py    # Gerenciamento de notas
│   ├── folder_manager.py  # Gerenciamento de pastas
│   ├── vault.py           # Gerenciamento do Vault
│   ├── autosave.py        # Sistema de auto-save
│   └── pdf_exporter.py    # Exportação para PDF
│
├── ui/                    # Interface gráfica
│   ├── __init__.py
│   ├── login.py           # Tela de login
│   ├── register.py        # Tela de registro
│   ├── main_window.py     # Dashboard principal
│   ├── dialogs.py         # Diálogos (Folder, Move, Password)
│   └── quick_note_dialog.py # Diálogo de nota rápida
│
├── security/              # Módulos de segurança
│   ├── __init__.py
│   └── crypto.py          # Criptografia AES-256
│
├── storage/               # Armazenamento
│   ├── __init__.py
│   └── file_manager.py    # Gerenciamento de arquivos
│
├── utils/                 # Utilitários
│   ├── __init__.py
│   └── helpers.py         # Funções auxiliares
│
└── data/                  # Dados do usuário (criado automaticamente)
    └── [username]/
        ├── user.json      # Dados do usuário
        ├── vault/         # Pasta Vault
        └── folders/       # Pastas criadas pelo usuário
            └── [folder_name]/
                ├── meta.json      # Metadados da pasta
                └── [note_id].json # Notas criptografadas
```

## 🚀 Funcionalidades

### 1. Autenticação
- **Tela de Cadastro**: Criação de conta com validação de senha (mín. 6 caracteres)
- **Tela de Login**: Autenticação segura com hash de senha
- **Vault Automático**: Criado automaticamente ao registrar usuário

### 2. Gerenciamento de Pastas
- **Criar pastas** com ou sem senha
- **Proteção por senha**: Pastas protegidas exigem senha para acesso
- **Desbloqueio em sessão**: Pastas permanecem desbloqueadas durante o uso
- **Travar pastas**: Opção de travar manualmente
- **Renomear e excluir** pastas (exceto Vault)

### 3. Gerenciamento de Notas
- **Criar, editar, renomear e excluir** notas
- **Auto-save**: Salva automaticamente após 1.5s sem digitar
- **Fallback para Vault**: Conteúdo não salvo vai para o Vault
- **Mover notas** entre pastas (com re-criptografia)
- **Atalho global**: Ctrl+Insert para Quick Note

### 4. Exportação
- **PDF - Desktop**: Salva diretamente na área de trabalho
- **PDF - Documents**: Salva na pasta Documentos
- **PDF - Escolher local**: Diálogo para selecionar destino
- **TXT File**: Exportação em texto puro

### 5. Segurança
- **AES-256-CBC** para criptografia de notas
- **PBKDF2** com 100.000 iterações para derivação de chave
- **Salt único** por criptografia (armazenado junto ao ciphertext)
- **PKCS7 padding** para alinhamento de bloco
- **Verificação de senha** resistente a timing attacks

## ⌨️ Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+S` | Salvar nota atual |
| `Ctrl+N` | Nova nota |
| `Ctrl+Shift+N` | Nova pasta |
| `Ctrl+Insert` | Quick Note (global) |
| `Ctrl+F` | Focar na árvore de pastas |
| `F5` | Atualizar tudo |
| `Ctrl+W` | Limpar editor |
| `Delete` | Excluir item selecionado |

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Windows 10/11 (outros SOs suportados mas sem hotkey global)

### Passos

1. **Clone ou extraia o projeto**

```bash
git clone https://github.com/yourusername/kairus.git
cd kairus
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**

```bash
python main.py
```

### Dependências

```txt
PySide6==6.6.0          # Interface gráfica
cryptography==41.0.7    # Criptografia AES
bcrypt==4.1.2           # Hash de senha
reportlab==4.0.4        # Exportação PDF
```

## 🔧 Configuração

### Reset do Banco de Dados

Para resetar completamente o sistema (apagar todos os usuários, pastas e notas):

```bash
python reset_db.py
```

Digite `DELETE ALL` para confirmar.

### Hotkey Global (Windows)

O atalho global `Ctrl+Insert` requer permissões de administrador no Windows. Execute o programa como administrador para habilitar esta funcionalidade.

## 🖥️ Uso

### Primeiro Acesso

1. Ao iniciar pela primeira vez, a tela de **cadastro** será exibida
2. Crie um usuário com nome (mín. 3 caracteres) e senha (mín. 6 caracteres)
3. O **Vault** será criado automaticamente

### Criando uma Nota

1. Selecione uma pasta na sidebar
2. Escreva o conteúdo no editor
3. Clique em **📄 + New Note** ou pressione `Ctrl+N`
4. Digite um título e confirme

### Criando uma Pasta com Senha

1. Clique em **📁 + New Folder**
2. Digite o nome da pasta
3. Marque **"Protect with password"**
4. Digite e confirme a senha
5. Clique em **Create**

### Acessando uma Pasta com Senha

1. Clique na pasta com ícone 🔒
2. Digite a senha quando solicitado
3. A pasta será desbloqueada para toda a sessão

### Exportando uma Nota

1. Clique com o botão direito na nota
2. Vá em **📄 Export** > escolha o formato:
   - **PDF - Desktop** (salva na área de trabalho)
   - **PDF - Documents** (salva em Documentos)
   - **PDF - Choose location...** (escolher local)
   - **TXT File** (salva como texto)

### Quick Note

- Pressione `Ctrl+Insert` de qualquer lugar (até fora do app)
- Uma janela popup será aberta para escrita rápida
- A nota será salva automaticamente no Vault

## 🏗️ Arquitetura

### Fluxo de Criptografia

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Usuário   │────▶│   Senha     │────▶│   PBKDF2    │
└─────────────┘     └─────────────┘     │ (100k iters)│
                                        └──────┬──────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Nota      │────▶│   AES-256   │◀────│   Chave     │
│  (texto)    │     │    CBC      │     │   32 bytes  │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Salt +    │
                    │   IV +      │
                    │  Ciphertext │
                    └─────────────┘
```

### Fluxo de Auto-save

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Digitação │────▶│  Debounce   │────▶│  1.5s sem   │
│             │     │  (1.5s)     │     │  digitar    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Salvar    │◀────│   Trigger   │◀────│   Auto-     │
│   Nota      │     │   Auto-save │     │   save      │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 🔒 Segurança

- ✅ As senhas nunca são armazenadas em texto puro
- ✅ Cada nota é criptografada individualmente
- ✅ Pastas protegidas usam chave derivada da senha da pasta
- ✅ O Vault usa a senha mestre do usuário
- ✅ Todos os dados são armazenados localmente (offline)
- ✅ Verificação de integridade na descriptografia

## 🐛 Troubleshooting

### "Invalid padding bytes" ao abrir nota
- **Causa**: Nota foi criada com uma versão anterior do código
- **Solução**: Execute `python reset_db.py` e recrie seus dados

### Global hotkey (Ctrl+Insert) não funciona
- **Causa**: Permissões de administrador necessárias no Windows
- **Solução**: Execute o programa como administrador

### A pasta com senha não desbloqueia
- **Causa**: Senha incorreta ou metadata corrompida
- **Solução**: Verifique a senha ou delete a pasta (se vazia)

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para máxima segurança e usabilidade.

---

<div align="center">
  <strong>KAIRUS - Suas anotações, sua privacidade, seu controle.</strong>
</div>
```