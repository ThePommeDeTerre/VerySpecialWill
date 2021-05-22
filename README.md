# VerySpecialWill
Computer Systems Security Project

Projeto de Segurança de Sistemas Informáticos 

## Engenharia de _Software_
### Arquitetura Geral do Sistema
![](https://i.imgur.com/HeGHyzb.png)

## Instalação

### Dependências Servidor 
- Docker; e
- docker-compose.
### Dependências Cliente
- Python 3.8;
- Flask 1.1.2;
- Pyotp;
- flask_wtfe;
- flask_qrcode;
- Pycharm ou Visual Studio Code (não obrigatório).

### Obter o sistema
Para obter o sistema, o seguinte comando pode ser utilizado:
```bash
git clone https://github.com/ThePommeDeTerre/VerySpecialWill.git
```

## Utilização
### Servidor
No terminal, dentro do projeto, executar o seguinte comando:
```bash
docker-compose up
```

### Cliente
No Pycharm basta executar o projeto presente em Cliente, com as configurações correspondentes para excecutar um servidor Flask.
Alternativamente, no terminal na pasta do Cliente:
```bash
python3 app.py
```
Depois apenas é necessário abrir o seguinte _link_ num _browser_: https://127.0.0.1:32182/.

## Imagens da Execução do Sistema
### Página Inicial
![](https://i.imgur.com/io8EiXN.png)
### Autenticação 2FA
![](https://i.imgur.com/EQ8NVem.png)
### Página Utilizador
![](https://i.imgur.com/FA7i7zJ.png)
### Criar Testamento
![](https://i.imgur.com/DrmHYcx.png)
### Testamento Criado com Sucesso
![](https://i.imgur.com/HiawrrR.png)
### Testamento Decifrado com Sucesso
![](https://i.imgur.com/YRHYXNf.png)
### Testamento sem Partes Suficientes para Decifrar
![](https://i.imgur.com/3xYxVgy.png)

### Tentar Decifrar Testamento no Dia Errado
![](https://i.imgur.com/7nrjGu0.jpg)