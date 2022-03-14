Lista de chamada
=================
Bot para discord feito utilizando Python e Heroku PostgreSQL como base de dados. A aplicação está hospedada na plataforma Heroku.

Instalar dependências
======================
  #pip install -r requirements.txt
  
Rotina de testes
=================
  #pytest tests.py

Inicializar bot
================
  #python bot.py
  
Estrutura dos serviços
=======================
#. main.py : conecta, através de um cliente, com o discord e administra as interações dos usuários com o bot;
#. process_command.py :  Irá interpretar o comando enviado pelo usuário;
#. send_message.py : Envia a mensagem correspondente ao comando recebido;
#. components.py: Retorna o componente de mensagem embutido;
#. database.py : Realiza operações no banco de dados;
#. tests.py : Testes das funções que operam no banco de dados;
#. config.py : Configurações.
