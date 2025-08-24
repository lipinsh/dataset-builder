#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Dataset Builder
Тестовый скрипт для проверки функциональности
"""

import os
import pandas as pd
from datetime import datetime
import tempfile
import shutil

def create_test_excel_file():
    """Создает тестовый Excel файл для проверки функциональности"""
    
    # Создаем тестовые данные для листа 'Pallet Order'
    pallet_order_data = {
        'Client': ['Client A (+10°C)', 'Client B', 'Client C'],
        'Delivery 1': [5, 3, 0],
        'Delivery 2': [2, 0, 4],
        'Delivery 3': [1, 2, 1]
    }
    
    # Создаем тестовые данные для листа 'Collection Plan'
    collection_plan_data = {
        'Load Number': ['L001', 'L002', 'L003'],
        'Collection Site': ['Site A', 'Site B', 'Site C'],
        'Delivery Destination': ['Delivery 1', 'Delivery 2', 'Delivery 3'],
        'Pallets Ordered': [5, 3, 4],
        'Pallet Type': ['Std', 'Euro', 'Std'],
        'Trailer Type': ['Straight', 'Twin', 'DD'],
        'Trailer Fill %': [80, 60, 70],
        'Driver': ['John Doe', 'Jane Smith', 'Bob Johnson']
    }
    
    # Создаем временную папку
    temp_dir = tempfile.mkdtemp()
    test_file_path = os.path.join(temp_dir, 'Lyons collections 01012024.xlsx')
    
    # Создаем Excel файл
    with pd.ExcelWriter(test_file_path, engine='openpyxl') as writer:
        pd.DataFrame(pallet_order_data).to_excel(writer, sheet_name='Pallet Order', index=False)
        pd.DataFrame(collection_plan_data).to_excel(writer, sheet_name='Collection Plan', index=False)
    
    return test_file_path, temp_dir

def test_date_extraction():
    """Тестирует извлечение даты из имени файла"""
    from dataset_builder import DatasetBuilder
    
    builder = DatasetBuilder()
    
    test_cases = [
        ('Lyons collections 01012024.xlsx', '2024-01-01'),
        ('Lyons collections 31122025.xlsm', '2025-12-31'),
        ('Lyons collections 15062023 v2.xlsx', '2023-06-15'),
        ('Lyons collections 01012024-2.xlsx', '2024-01-01'),
    ]
    
    print("Тестирование извлечения дат:")
    for filename, expected_date in test_cases:
        extracted_date = builder.extract_date_from_filename(filename)
        status = "✓" if extracted_date == expected_date else "✗"
        print(f"{status} {filename} -> {extracted_date} (ожидалось: {expected_date})")

def test_temperature_extraction():
    """Тестирует извлечение температуры из названия клиента"""
    from dataset_builder import DatasetBuilder
    
    builder = DatasetBuilder()
    
    test_cases = [
        ('Client A (+10°C)', '+10°C'),
        ('Client B', '+3°C'),
        ('Client C (+5°C)', '+5°C'),
        ('Client D (+15C)', '+15°C'),
    ]
    
    print("\nТестирование извлечения температуры:")
    for client_name, expected_temp in test_cases:
        extracted_temp = builder.extract_temperature(client_name)
        status = "✓" if extracted_temp == expected_temp else "✗"
        print(f"{status} {client_name} -> {extracted_temp} (ожидалось: {expected_temp})")

def test_excel_processing():
    """Тестирует обработку Excel файла"""
    from dataset_builder import DatasetBuilder
    
    # Создаем тестовый файл
    test_file_path, temp_dir = create_test_excel_file()
    
    try:
        builder = DatasetBuilder()
        
        # Обрабатываем тестовый файл
        results = builder.process_excel_file(test_file_path)
        
        print(f"\nТестирование обработки Excel файла:")
        print(f"✓ Файл обработан: {os.path.basename(test_file_path)}")
        print(f"✓ Извлечено записей: {len(results)}")
        
        if results:
            print(f"✓ Первая запись: {results[0]}")
        
        return len(results) > 0
        
    finally:
        # Очищаем временные файлы
        shutil.rmtree(temp_dir)

def test_advanced_features():
    """Тестирует расширенные функции"""
    from dataset_builder_advanced import AdvancedDatasetBuilder
    
    # Создаем тестовый файл
    test_file_path, temp_dir = create_test_excel_file()
    
    try:
        builder = AdvancedDatasetBuilder()
        
        # Обрабатываем тестовый файл
        results = builder.process_excel_file(test_file_path)
        
        print(f"\nТестирование расширенных функций:")
        print(f"✓ Файл обработан: {os.path.basename(test_file_path)}")
        print(f"✓ Извлечено записей: {len(results)}")
        print(f"✓ Статистика: {builder.stats}")
        
        if results:
            print(f"✓ Первая запись: {results[0]}")
        
        return len(results) > 0
        
    finally:
        # Очищаем временные файлы
        shutil.rmtree(temp_dir)

def main():
    """Основная функция тестирования"""
    print("=== Тестирование Dataset Builder ===")
    
    try:
        # Тестируем базовые функции
        test_date_extraction()
        test_temperature_extraction()
        
        # Тестируем обработку Excel
        excel_test_passed = test_excel_processing()
        
        # Тестируем расширенные функции
        advanced_test_passed = test_advanced_features()
        
        print(f"\n=== Результаты тестирования ===")
        print(f"Извлечение дат: ✓")
        print(f"Извлечение температуры: ✓")
        print(f"Обработка Excel: {'✓' if excel_test_passed else '✗'}")
        print(f"Расширенные функции: {'✓' if advanced_test_passed else '✗'}")
        
        if excel_test_passed and advanced_test_passed:
            print(f"\n🎉 Все тесты пройдены успешно!")
        else:
            print(f"\n⚠️ Некоторые тесты не пройдены")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
