# Lista de chamada 
Bot para discord feito utilizando Python e Heroku PostgreSQL como base de dados. A aplicação está hospedada na plataforma Heroku.

## Instalar dependências
  - pip install -r requirements.txt
  
## Rotina de testes
  - pytest

## Inicializar bot
  - python main.py

# Fluxograma de operação
```mermaid
stateDiagram-v2
    [*] --> main.py
    main.py --> process_command.py
    components.py --> send_message.py
    process_command.py --> send_message.py
    database.py --> send_message.py
    send_message.py --> [*]
```           
