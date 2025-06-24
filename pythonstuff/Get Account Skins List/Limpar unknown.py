# Abrir o arquivo original para leitura e criar um novo arquivo limpo para escrita
with open('skin_names.txt', 'r', encoding='utf-8') as original_file, \
     open('skin_names_cleaned.txt', 'w', encoding='utf-8') as cleaned_file:
    
    for line in original_file:
        # Se a linha não contém "Unknown", escreva no novo arquivo
        if "Unknown" not in line:
            cleaned_file.write(line)
