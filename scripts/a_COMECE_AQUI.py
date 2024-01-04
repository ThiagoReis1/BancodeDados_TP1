def obter_config_postgres():
    # Configurações o banco de dados padrao o 'postgres', ele é usado pra criar o banco de dados da função obter_config_bd()
    config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '1234',
        'host': 'localhost'
    }
    return config

def obter_config_bd():
    # Configurações o banco de dados  'bancodedados', eu crie ele pra deixar a parada mais legal
    config = {
        'dbname': 'bancodedados',
        'user': 'postgres',
        'password': '1234',
        'host': 'localhost'
    }
    return config