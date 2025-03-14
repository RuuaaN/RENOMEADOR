import os
import re
import argparse
from datetime import datetime

def get_image_files(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'))]

def get_file_info(directory, file):
    file_path = os.path.join(directory, file)
    stat = os.stat(file_path)
    return {
        'name': file,
        'path': file_path,
        'size': stat.st_size,
        'ctime': stat.st_ctime
    }

def sort_files(files, order_by, descending):
    return sorted(files, key=lambda x: x[order_by], reverse=descending)

def rename_files(directory, method, order_by, descending):
    files = get_image_files(directory)
    if not files:
        print("Nenhuma imagem encontrada na pasta.")
        return
    
    files_info = [get_file_info(directory, file) for file in files]
    sorted_files = sort_files(files_info, order_by, descending)
    
    existing_names = set()
    
    for index, file_info in enumerate(sorted_files, start=1):
        ext = os.path.splitext(file_info['name'])[1]
        
        if method == "sequential":
            new_name = f"{index}{ext}"
        elif method == "date":
            date_str = datetime.fromtimestamp(file_info['ctime']).strftime("%d-%m-%Y")
            new_name = f"{date_str}{ext}"
        else:
            print("Método inválido.")
            return
        
        new_name = ensure_unique_name(directory, new_name, existing_names)
        new_path = os.path.join(directory, new_name)
        
        os.rename(file_info['path'], new_path)
        print(f"{file_info['name']} -> {new_name}")

def ensure_unique_name(directory, name, existing_names):
    base, ext = os.path.splitext(name)
    counter = 1
    new_name = name
    
    while new_name in existing_names or os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base}({counter}){ext}"
        counter += 1
    
    existing_names.add(new_name)
    return new_name

def user_input(prompt, choices):
    while True:
        print(prompt)
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        selection = input("Escolha uma opção: ")
        if selection.isdigit() and 1 <= int(selection) <= len(choices):
            return choices[int(selection) - 1]
        print("Opção inválida, tente novamente.")

def main():
    print("Bem-vindo ao Renomeador de Imagens!")
    method = user_input("Escolha o método de renomeação:", ["sequential", "date"])
    order_by = user_input("Escolha o critério de ordenação:", ["size", "ctime", "name"])
    descending = user_input("Ordenação crescente ou decrescente?", ["Crescente", "Decrescente"]) == "Decrescente"
    
    directory = os.path.dirname(os.path.abspath(__file__))  # Usa a pasta onde o script está salvo
    rename_files(directory, method, order_by, descending)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    
    print("\nPressione Enter para sair...")
    input()
