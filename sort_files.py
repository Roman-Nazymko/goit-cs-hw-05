import os
import asyncio
from pathlib import Path
import shutil
import logging
from colorama import Fore, Style, init
import textwrap
import argparse

# Ініціалізуємо colorama
init(autoreset=True)

# Налаштування логування
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")

# Копіювання файлів за їх розширенням
async def process_file(file_path, destination_dir):
    try:
        extension = file_path.suffix[1:].lower() if file_path.suffix else "unknown"
        target_dir = Path(destination_dir, extension)
        target_dir.mkdir(parents=True, exist_ok=True)
        destination = target_dir / file_path.name

        # Асинхронне копіювання
        await asyncio.to_thread(shutil.copy2, file_path, destination)
        print(Fore.GREEN + f"Копіювання: {file_path} -> {destination}" + Style.RESET_ALL)
    except Exception as e:
        error_message = textwrap.fill(
            f"Помилка копіювання файлу {file_path}: {e}",
            width=100
        )
        logging.error(error_message)
        print(Fore.RED + error_message + Style.RESET_ALL)

# Читання папки і обробка файлів
async def process_directory(source_dir, destination_dir):
    try:
        tasks = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root, file)
                tasks.append(process_file(file_path, destination_dir))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка при обробці папки {source_dir}: {e}")
        print(Fore.RED + f"Помилка при обробці папки {source_dir}: {e}" + Style.RESET_ALL)

def parse_args():
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням.")
    parser.add_argument("source_dir", help="Шлях до папки з файлами для сортування")
    parser.add_argument("destination_dir", help="Шлях до папки для збереження файлів")
    return parser.parse_args()

def main():
    args = parse_args()

    source_dir = args.source_dir 
    destination_dir = args.destination_dir


    if not Path(source_dir).is_dir():
        print(Fore.RED + "Помилка: Вказана папка не існує або це не папка." + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Розпочинається процес сортування..." + Style.RESET_ALL)
    asyncio.run(process_directory(source_dir, destination_dir))
    print(Fore.CYAN + "Сортування завершено." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
