# Projeto-de-Redes

O projeto foi desenvolvido para a disciplina de Rede 1, é um programa que realiza transferências de arquivos (Peer-to-peer). Cada usuário que cadastrar no programa terá a possibilidade de salvar arquivos, fazer download e deletar arquivos que não quer mais do servidor. 
Cada usuário terá uma pasta no servidor para identificação de seus próprios arquivos não interferindo nos demais. Ao fazer download de qualquer arquivo, será criado uma pasta no mesmo local onde o programa foi salvo e nela será salvo todos os arquivos que forem feito o download. Foi utilizado Sqlite3 para armazenamento dos usuários e dos dirétorios dos arquivos salvos no servidor.

## Desenvolvimento

O programa foi desenvolvido utilizando a versão do Python: 3.6.9

## Funcionalidades

* Login
* Registro
* Upload de arquivos para o servidor
* Download de arquivos que estão no servidor
* Deletar arquivos que estão no servidor

## Instalação

É necessário a versão do Python: 3.6.9 que pode ser encontrado no link abaixo:

[Instalar Python](https://www.python.org/downloads/)

Se necessário, instalar o Sqlite3:

[Instalar Sqlite no Linux/MacOS/Windows](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm)

## Como usar

Fazer a clonagem do repositório, entrar na pasta do programa executando as seguintes instruções:

```
    git clone https://github.com/gacl97/Projeto-de-Redes.git
    cd Projeto-de-redes
```

Após a clonagem executar o programa do servidor, colocando o seguinte comando:

```
    python3 server.py
```
Informe a Porta que será a mesma para usar ao conectar os clientes.

Agora executar o cliente com o seguinte comando:

```
    python3 client.py
```

Informe o Endereço IP e a Porta que foi usado pra executar o servidor. Uma vez que o servidor foi executado, poderá conectar vários clientes utilizando a aplicação ao mesmo tempo.

Sendo o primeiro acesso, o usuário deve se registrar criando um login que será único e uma senha.
Ao se registrar no programa, o usuário pode fazer upload de arquivos, download dos arquivos que foram feitos uploads e deletar arquivos do servidor.