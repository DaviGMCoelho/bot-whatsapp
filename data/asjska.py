operation = {
    'segunda-feira_abre': '00:00', 
    'segunda-feira_fecha': '22:22', 
    'segunda-feira_ativo': 'on', 
    'terca-feira_abre': '00:00', 
    'terca-feira_fecha': '22:22', 
    'terca-feira_ativo': 'on', 
    'quarta-feira_abre': '00:00',
    'quarta-feira_fecha': '22:22',
    'quarta-feira_ativo': 'on',
    'quinta-feira_abre': '00:00',
    'quinta-feira_fecha': '22:22',
    'quinta-feira_ativo': 'on',
    'sexta-feira_abre': '00:00',
    'sexta-feira_fecha': '22:22',
    'sexta-feira_ativo': 'on',
    'sabado_abre': '00:00',
    'sabado_fecha': '22:22',
    'sabado_ativo': 'on',
    'domingo_abre': '00:00',
    'domingo_fecha': '22:22',
    'domingo_ativo': 'on',
    'feriado_abre': '00:00',
    'feriado_fecha': '22:22',
    'feriado_ativo': 'on'
}

def _normalize_data(request: dict):
    # JSON BAGUNÇADO
    # Pega o dia
    #   - Separa por tópico
    #   - Armazena direito

    days = {}
    for key, value in request.items():
        day, topic = key.split('_', 1)

        if day not in days:
            days[day] = {
                    'day': day,
                    'open_at': None,
                    'close_at': None,
                    'active': False
            }
        if topic == 'abre':
            days[day]['open_at'] = value
        elif topic == 'fecha':
            days[day]['close_at'] = value
        elif topic == 'ativo':
            days[day]['active'] = value == 'on'
    return {'operation': list(days.values())}

data = _normalize_data(operation)
print(data)
