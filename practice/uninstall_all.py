import subprocess

def uninstall_package(package):
    try:
        result = subprocess.run(['pip', 'uninstall', '-y', package])
        print(f"Удален пакет: {package}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при удалении пакета {package}: {e}")

def main():
    # Получаем список всех установленных пакетов
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    
    # Обрабатываем вывод команды
    lines = result.stdout.strip().split('\n')
    packages = [line.split()[0] for line in lines[2:] if len(line) > 0]
    
    # Удаляем каждый пакет
    for package in packages:
        uninstall_package(package)

if __name__ == "__main__":
    main()


