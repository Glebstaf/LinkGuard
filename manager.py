"""
🛡️ LinkGuard Manager v2.0 - Управление программой
"""
import os
import subprocess
import sys
import json

# --- Конфигурация ---
ARCHIVE_FILE = "whitelist_archive.json"

def add_to_whitelist():
    """Добавляет домен в белый список"""
    domain = input("Введите домен для добавления (например, example.com): ").strip()
    if not domain:
        print("❌ Домен не может быть пустым.")
        return
    
    with open("whitelist.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{domain}")
    print(f"✅ Домен '{domain}' добавлен в whitelist.txt")

def restart_guard():
    """Перезапускает LinkGuard"""
    print("🔄 Перезапускаю LinkGuard...")
    try:
        with open("stop.flag", "w") as f:
            pass
        import time
        time.sleep(2)
        subprocess.Popen(["link_guard.exe"])
        print("✅ LinkGuard перезапущен.")
    except Exception as e:
        print(f"❌ Ошибка перезапуска: {e}")

def stop_guard():
    """Останавливает LinkGuard"""
    print("🛑 Останавливаю LinkGuard...")
    try:
        with open("stop.flag", "w") as f:
            pass
        print("✅ Команда на остановку отправлена. LinkGuard скоро закроется.")
    except Exception as e:
        print(f"❌ Ошибка остановки: {e}")

def check_status():
    """Проверяет статус работы"""
    try:
        if os.path.exists("stop.flag"):
            print("⚠️ Флаг остановки найден. LinkGuard может быть остановлен.")
        else:
            print("✅ Флаг остановки не найден. LinkGuard, вероятно, работает.")
        print("💡 Проверьте Диспетчер задач (Ctrl+Shift+Esc) для точного статуса.")
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")

def uninstall_program():
    """Полностью удаляет программу"""
    print("⚠️ ВНИМАНИЕ! Это удалит LinkGuard и все файлы.")
    confirm = input("Подтвердите удаление? (да/нет): ").lower()
    
    if confirm != 'да':
        print("❌ Отмена удаления.")
        return
    
    try:
        files_to_remove = ["link_guard.exe", "manager.exe", "whitelist.txt", "stop.flag"]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
        
        if os.path.exists(ARCHIVE_FILE):
            os.remove(ARCHIVE_FILE)
        
        print("✅ LinkGuard успешно удален.")
    except Exception as e:
        print(f"❌ Ошибка удаления: {e}")

def delete_whitelist():
    """Удаляет только белый список"""
    print("⚠️ ВНИМАНИЕ! Это удалит whitelist.txt.")
    confirm = input("Подтвердите удаление? (да/нет): ").lower()
    
    if confirm != 'да':
        print("❌ Отмена удаления.")
        return
    
    try:
        if os.path.exists("whitelist.txt"):
            os.remove("whitelist.txt")
            print("✅ Белый список удален.")
        else:
            print("ℹ️ Файл whitelist.txt не найден.")
    except Exception as e:
        print(f"❌ Ошибка удаления: {e}")

def export_whitelist():
    """Экспортирует белый список в архив"""
    try:
        if not os.path.exists("whitelist.txt"):
            print("❌ Файл whitelist.txt не найден.")
            return
        
        whitelist = []
        with open("whitelist.txt", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    whitelist.append(line)
        
        with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(whitelist, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Белый список экспортирован в {ARCHIVE_FILE}")
    except Exception as e:
        print(f"❌ Ошибка экспорта: {e}")

def import_whitelist():
    """Импортирует белый список из архива"""
    try:
        if not os.path.exists(ARCHIVE_FILE):
            print(f"❌ Файл {ARCHIVE_FILE} не найден.")
            return
        
        with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
            whitelist = json.load(f)
        
        with open("whitelist.txt", 'w', encoding='utf-8') as f:
            for domain in whitelist:
                f.write(f"{domain}\n")
        
        print(f"✅ Белый список импортирован из {ARCHIVE_FILE}")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")

if __name__ == "__main__":
    import time
    while True:
        print("\n" + "="*45)
        print("  🛡️ LinkGuard Manager v2.0")
        print("="*45)
        print("1. Добавить домен в белый список")
        print("2. Перезапустить LinkGuard")
        print("3. Выключить LinkGuard")
        print("4. Проверить статус работы")
        print("5. Удалить программу")
        print("6. Удалить только белый список")
        print("7. Экспорт белого списка")
        print("8. Импорт белого списка")
        print("9. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            add_to_whitelist()
        elif choice == '2':
            restart_guard()
        elif choice == '3':
            stop_guard()
        elif choice == '4':
            check_status()
        elif choice == '5':
            uninstall_program()
        elif choice == '6':
            delete_whitelist()
        elif choice == '7':
            export_whitelist()
        elif choice == '8':
            import_whitelist()
        elif choice == '9':
            print("👋 Выход из менеджера.")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")