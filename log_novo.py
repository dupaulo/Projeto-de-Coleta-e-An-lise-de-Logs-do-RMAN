import os
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Função para calcular a diferença em horas, minutos e segundos entre duas datas no formato especificado
def calculate_time_difference(start_str, end_str):
    date_format = "%a %b %d %H:%M:%S %z %Y"
    # Normalizar a string de data para corresponder ao formato esperado
    start_str = normalize_date_format(start_str)
    end_str = normalize_date_format(end_str)
    start_time = datetime.strptime(start_str, date_format)
    end_time = datetime.strptime(end_str, date_format)
    difference = end_time - start_time
    return str(timedelta(seconds=difference.total_seconds()))

# Função para normalizar o formato da data
def normalize_date_format(date_str):
    parts = date_str.split()
    if len(parts[2]) == 1:  # Se o dia tiver um dígito, adicionar um zero à esquerda
        parts[2] = '0' + parts[2]
    # Ajustar o fuso horário para o formato esperado
    if len(parts[-2]) == 3:  # Se o fuso horário tiver 3 caracteres, adicionar "00" no final
        parts[-2] = parts[-2] + "00"
    return ' '.join(parts)

# Diretório onde os arquivos .log estão localizados
log_directory = Path(r"E:\\log")

# Verificando se o diretório existe
if not log_directory.exists():
    raise FileNotFoundError(f"O diretório {log_directory} não foi encontrado.")

# Conectando ao banco de dados (ou criando-o)
conn = sqlite3.connect('E:\\db_pyton\\backup_logs.db')
cursor = conn.cursor()

# Criando a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS log_files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    host TEXT,
    data_bkp TEXT,
    instance TEXT,
    tipo_bkp TEXT,
    start_time TEXT,
    end_time TEXT,
    time_difference TEXT,
    status TEXT
)
''')

# Adicionando colunas novas, se necessário
cursor.execute('PRAGMA table_info(log_files)')
columns = [column[1] for column in cursor.fetchall()]

if 'time_difference' not in columns:
    cursor.execute('ALTER TABLE log_files ADD COLUMN time_difference TEXT')
if 'status' not in columns:
    cursor.execute('ALTER TABLE log_files ADD COLUMN status TEXT')

# Exemplo de padrões regex para capturar informações específicas de um arquivo de log
host_pattern = re.compile(r'Host:\s+(\S+)')
instance_pattern = re.compile(r'Instância:\s+(\S+)')
type_pattern = re.compile(r'Tipo:\s+(\S+)')
date_pattern = re.compile(r'Data:\s+(.+)')
backup_start_pattern = re.compile(r'Backup iniciou em:\s+(.+)')
backup_end_pattern = re.compile(r'Terminou em:\s+(.+)')
status_pattern = re.compile(r'Backup efetuado com sucesso')

# Percorrendo os arquivos no diretório
for filepath in log_directory.glob("*.log"):
    # Ignorar arquivos já processados
    if "completed" in filepath.stem:
        continue
    
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Removendo as strings especificadas
    tipo_bkp_match = type_pattern.search(content)

    host_match = host_pattern.sub('',content)
    instance_match = instance_pattern.sub('',content) 

    content = host_pattern.sub('', content)
    content = instance_pattern.sub('', content)
    content = type_pattern.sub('', content)
    content = date_pattern.sub('', content)
    
    # Extraindo tempos de início e fim do backup
    start_match = backup_start_pattern.search(content)
    end_match = backup_end_pattern.search(content)
    status_match = status_pattern.search(content)

    if start_match and end_match and status_match:
        instance = tipo_bkp_match.group(1)
        parts = instance.split('_')
        instance = parts[2]
        
        host = 'Exadata'
        
        tipo_bkp = tipo_bkp_match.group(1)
        parts = tipo_bkp.split('_')
        tipo_bkp = parts[1]
        
        start_time = start_match.group(1)
        end_time = end_match.group(1)
        time_difference = calculate_time_difference(start_time, end_time)
        status = "Backup efetuado com sucesso"
        
        pega_data = filepath.name.split('.')
        data = pega_data[1]
        data = data[:8]
        ano = data[:4]
        mes = data[4:6]
        dia = data[6:8]
        data_format = f"{dia}/{mes}/{ano}"

        # Inserindo os dados no banco de dados
        cursor.execute('''
        INSERT INTO log_files (filename, tipo_bkp,host,data_bkp,instance,start_time, end_time, time_difference, status) 
        VALUES (?, ?, ?, ?, ?,?,?,?,?)
        ''', (filepath.name, tipo_bkp ,host,data_format,instance,start_time, end_time, time_difference, status))
        
        conn.commit()
        
        # Renomeando o arquivo para marcar como "completed"
        completed_filename = filepath.with_name(filepath.stem + "_completed.log")
        filepath.rename(completed_filename)

# Fechando a conexão com o banco de dados
conn.close()
