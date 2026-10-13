# SMART PASS — Sistema de Controle de Saídas Escolares

## 1. Sobre o projeto

O SMART PASS é um sistema web desenvolvido em Python com Django para gerenciar alunos e registrar saídas escolares.

## 2. O que precisa instalar antes

Antes de executar o projeto, instale os seguintes programas:

- **Python 3.13:** necessário para executar o projeto Python.
- **Visual Studio Code (VS Code):** editor para abrir e modificar o código.
- **Git:** necessário para baixar o projeto do repositório, caso ele ainda não esteja no computador.
- **Google Chrome ou outro navegador:** para acessar o site.

O projeto utiliza Django e outras bibliotecas Python, instaladas pelo arquivo `requirements.txt`.

## 3. Como baixar o projeto

Se o projeto ainda não estiver no computador, abra o terminal e execute:

```powershell
git clone URL_DO_REPOSITORIO
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório Git.

Depois, entre na pasta:

```powershell
cd Sistema_saida2.0
```

Se o projeto já estiver no computador, abra a pasta existente no VS Code e não execute o `git clone` novamente.

## 4. Como preparar o ambiente

Abra o terminal do VS Code em **Terminal → Novo Terminal**.

Entre na pasta do projeto:

```powershell
cd C:\Users\Cliente\Documents\Sistema_saida2.0
```

Crie o ambiente virtual, caso ainda não exista:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Atualize o instalador de pacotes:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências do projeto:

```powershell
python -m pip install -r requirements.txt
```

**Importante:** execute a instalação das dependências depois de ativar o ambiente virtual.

## 5. Como executar o site

Com o ambiente virtual ativado, execute:

```powershell
python manage.py check
```

Se não houver erros de configuração, inicie o servidor:

```powershell
python manage.py runserver 8001
```

Abra o navegador e acesse:

**http://127.0.0.1:8001/**

Mantenha o terminal aberto enquanto utilizar o sistema.

Para encerrar o servidor, pressione `Ctrl + C` no terminal.

## 6. Páginas do sistema

- **Painel:** http://127.0.0.1:8001/
- **Registrar saída:** http://127.0.0.1:8001/saida/
- **Histórico:** http://127.0.0.1:8001/historico/
- **Alunos:** http://127.0.0.1:8001/alunos/
- **Diagnóstico:** http://127.0.0.1:8001/diagnostico/

## 7. Banco de dados

O projeto utiliza o banco de dados SQLite no arquivo `db.sqlite3`.

Esse arquivo contém os dados armazenados localmente, como os cadastros de alunos e os registros de saídas.

- Não exclua o arquivo `db.sqlite3`.
- Faça uma cópia de segurança antes de realizar alterações importantes.
- Ao transferir o projeto para outro computador, confira se o banco de dados correto também foi transferido.

Se o projeto estiver usando um banco de dados diferente em produção, siga as configurações específicas desse ambiente.

## 8. Arquivos importantes

- `manage.py`: comandos de gerenciamento do Django.
- `requirements.txt`: bibliotecas necessárias para executar o projeto.
- `db.sqlite3`: banco de dados local.
- `escola/`: configurações principais do projeto Django.
- `saidas/`: aplicação responsável pelas funcionalidades do sistema.
- `saidas/templates/saidas/`: páginas HTML.
- `saidas/static/saidas/style.css`: arquivo de estilos visuais.

## 9. Solução de problemas

### O comando `python` não funciona

Verifique se o Python está instalado e disponível no PATH do Windows.

### O comando `pip` não funciona

Com o ambiente virtual ativado, execute:

```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### O site não abre

Verifique se o servidor está em execução e se o endereço utilizado é `http://127.0.0.1:8001/`.

### Aparece erro de dependência

Confirme que o ambiente virtual está ativado e execute:

```powershell
python -m pip install -r requirements.txt
```

### O CSS ou as cores não aparecem

Atualize o navegador com `Ctrl + F5`. Se o problema continuar, verifique se o arquivo `saidas/static/saidas/style.css` existe e se a configuração de arquivos estáticos do Django está correta.

## 10. Observações finais

Este procedimento descreve a execução local do SMART PASS no Windows. A publicação na internet exige configuração adicional do servidor de hospedagem, variáveis de ambiente, arquivos estáticos e banco de dados de produção.

**Projeto:** SMART PASS  
**Tecnologia principal:** Python e Django  
**Banco local:** SQLite  
**Porta local:** 8001
