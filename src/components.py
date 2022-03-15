from random import choice
from config import Config
from discord import Embed

# Cores
RED     = 0xf83629
YELLOW  = 0xe7f337
BLUE    = 0x538fdf
GREEN   = 0x6dc22c


def update_subscription_msg(embed, user):
    embed_dict = embed.to_dict()
    edited_text = embed_dict['fields'][0]['value']
    if edited_text == "-":
        edited_text = ""
    edited_text += f"\n{user}"
    embed_dict['fields'][0]['value'] = edited_text
    return Embed.from_dict(embed_dict)

##### static messages #####

help = Embed.from_dict({
    "color": BLUE,
    "title": "Comandos",
    "footer": {
        "text": "CRISPY CORPORATIONS (#8453)",
        "icon_url": Config.icon_url
    },
    "fields": [
        {
            "name": "Cadastrar um novo evento",
            "value": f"```{Config.prefix}criar <nome do evento>```",
            "inline": False
        },
        {
            "name": "Renomear evento",
            "value": f"```{Config.prefix}renomear <nome> - <novo nome>```",
            "inline": False
        },
        {
            "name": "Excluir um evento",
            "value": f"```{Config.prefix}excluir```",
            "inline": False
        },
        {
            "name": "Listar os eventos cadastrados",
            "value": f"```{Config.prefix}eventos```",
            "inline": False
        },
        {
            "name": "Listar os inscritos de um evento",
            "value": f"```{Config.prefix}info```",
            "inline": False
        },
        {
            "name": "Realizar chamada de um evento",
            "value": f"```{Config.prefix}chamada```",
            "inline": False
        },
        {
            "name": "Reabrir inscrições de um evento",
            "value": f"```{Config.prefix}inscrever```",
            "inline": False
        },
        {
            "name": "Cancelar inscrição em um evento",
            "value": f"```{Config.prefix}sair```",
            "inline": False
        },
        {
            "name": "Código do bot",
            "value": f"```{Config.prefix}source```",
            "inline": False
        },
    ]
})

event_already_subscribed = Embed.from_dict({
    "color": RED,
    "title": "Aviso",
    "description": "Este evento já está cadastrado."
})

list_root = Embed.from_dict({
    "title": "Acesso negado", 
    "description": "Seu usuário não possui permissão para uso deste comando.", 
    "color": RED
})

no_events = Embed.from_dict({
    "title": "Eventos cadastrados", 
    "description": "- Não há eventos cadastrados -",
    "color": YELLOW
})

no_separator = Embed.from_dict({
    "title": "Aviso",
    "description": "Por favor, separe o nome e o novo nome com o caráctere **-** (hífen)",
    "color": RED
})

event_invalid_name = Embed.from_dict({
    "title": "Aviso",
    "description": "Novo nome de evento inválido.",
    "color": RED
})

rename_perm_error = Embed.from_dict({
    "title": "Aviso",
    "description": "Não foi possível renomear o evento. Não se esqueça" \
        " que apenas o criador do evento possui permissão para renomeá-lo.",
    "color": RED
})

rename_success = Embed.from_dict({
    "title": f"Renomear evento {Config.check}",
    "description": "Evento renomeado com sucesso.",
    "color": GREEN
})

remove_event_error = Embed.from_dict({
    "title": "Aviso",
    "description": "Não foi possível remover o evento",
    "color": RED
})

remove_event_success = Embed.from_dict({
    "title": f"Excluir evento {Config.check}",
    "description": "Evento removido com sucesso",
    "color": GREEN
})

inexistent_event = Embed.from_dict({
    "title": "Aviso",
    "description": "Este evento não está cadastrado",
    "color": RED
})

event_not_typed_error = Embed.from_dict({
    "title": "Aviso",
    "description": "Por favor, digite o nome do evento após o comando",
    "color": RED
})

source = Embed.from_dict({
    "color": BLUE,
    "title": "Código do bot",
    "description": "O conhecimento serve para ser compartilhado.\n" \
        "O código do Bot de Lista de Chamada é aberto a todos.\n" \
        "Clique no ícone de url para ser redirecionado.",
    "footer": [
        {
            "text": "Beijos de tio Crispim",
            "icon_url": Config.icon_url
        },  
    ]
})

##### update and return #####

def ping(): 
    pongs = ['tô aqui consagrado', 'diga campeão', 'ô amigo', 'opa', 'Êêê boi', 
        'fala corno', 'diga gay', 'oba', 'tô aqui', 'digaí boe', 'cu', 'Éééé gata',
        'bem-te-vi']
    return Embed.from_dict({
        "title": "pong",
        "description": choice(pongs),
        "color": BLUE
    })

def list_events(events):
    return Embed.from_dict({
        "title": "Eventos cadastrados", 
        "description": events,
        "color": YELLOW
    })

def already_subscribed(user, event):
    return Embed.from_dict({
        "color": RED,
        "title": "Aviso",
        "description": f"**{user}** já possui inscrição em **{event}**"
    })

def subscribe_event(event):
    return Embed.from_dict({
        "color": YELLOW,
        "title": "Inscrição",
        "description": f"Interaja aqui para se inscrever na lista de **{event}**",
        "fields": [
            {
                "name": "Inscritos",
                "value": "-",
                "inline": False
            },  
        ]
    })

def no_subscribers(event):
    return Embed.from_dict({
        "title": event,
        "description": "- Não há inscritos -",
        "color": YELLOW
    })

def list_event_users(event, users, creator):
    return Embed.from_dict({
        "title": event,
        "description": users,
        "color": YELLOW,
        "fields": [
            {
                "name": "Criado por: ",
                "value": creator,
                "inline": False
            }
        ]
    })

def call_users(event, users):
    return Embed.from_dict({
        "title": f"Chamada {event}",
        "description": users,
        "color": YELLOW
    })

def remove_subscription(event): 
    return Embed.from_dict({
        "title": "Remover inscrição",
        "description": f"Interaja aqui para retirar seu nome da lista de **{event}**",
        "color": YELLOW
    })

def not_subscribed(event, user):
    return Embed.from_dict({
        "color": RED,
        "title": "Aviso",
        "description": f"**{user}** não possui inscrição em **{event}**"
    })

def unsubscribed(event, user):
    return Embed.from_dict({
        "color": RED,
        "title": "Aviso",
        "description": f"**{user}** foi removido de **{event}**"
    })

def remove_event(event):
    return Embed.from_dict({
        "color": YELLOW,
        "title": "Excluir evento",
        "description": f"{Config.warn}Atenção{Config.warn}\nAo confirmar, **{event}** será deletado.\n\n" \
        "**Não se esqueça que apenas quem criou o evento possui permissão para excluí-lo.**"
    })