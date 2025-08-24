#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset Builder for Logistics Routes
Сбор данных из Excel-файлов с ежедневными маршрутами для обучения нейросети
"""

import os
import re
import pandas as pd
import glob
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DatasetBuilder:
    def __init__(self):
        self.combined_data = []
        self.existing_files = set()
        self.load_existing_dataset()
    
    def load_existing_dataset(self):
        """Загружает существующий датасет для добавления новых данных"""
        csv_path = "combined_dataset.csv"
        parquet_path = "combined_dataset.parquet"
        
        if os.path.exists(csv_path):
            try:
                existing_df = pd.read_csv(csv_path)
                self.combined_data = existing_df.to_dict('records')
                print(f"Загружен существующий датасет: {len(self.combined_data)} записей")
            except Exception as e:
                print(f"Ошибка загрузки существующего датасета: {e}")
        elif os.path.exists(parquet_path):
            try:
                existing_df = pd.read_parquet(parquet_path)
                self.combined_data = existing_df.to_dict('records')
                print(f"Загружен существующий датасет: {len(self.combined_data)} записей")
            except Exception as e:
                print(f"Ошибка загрузки существующего датасета: {e}")
    
    def extract_date_from_filename(self, filename):
        """Извлекает дату из имени файла"""
        # Ищем паттерн DDMMYYYY в имени файла
        pattern = r'(\d{2})(\d{2})(\d{4})'
        match = re.search(pattern, filename)
        
        if match:
            day, month, year = match.groups()
            try:
                date_obj = datetime(int(year), int(month), int(day))
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return None
        return None
    
    def extract_temperature(self, client_name):
        """Извлекает температуру из названия клиента"""
        if client_name and isinstance(client_name, str):
            # Паттерны для поиска температуры
            temp_patterns = [
                r'\(\+(\d+)°C\)',
                r'\+(\d+)°C',
                r'(\d+)°C',
                r'(\d+)C',
            ]
            
            for pattern in temp_patterns:
                temp_match = re.search(pattern, client_name, re.IGNORECASE)
                if temp_match:
                    return f"+{temp_match.group(1)}°C"
        return "+3°C"  # По умолчанию
    
    def read_excel_sheet(self, file_path, sheet_name, password=None):
        """Читает лист Excel с возможностью ввода пароля"""
        try:
            if password:
                return pd.read_excel(file_path, sheet_name=sheet_name, password=password)
            else:
                return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            if "password" in str(e).lower():
                print(f"Лист {sheet_name} защищен паролем. Пробуем с паролем 'Test'...")
                try:
                    return pd.read_excel(file_path, sheet_name=sheet_name, password="Test")
                except Exception as e2:
                    print(f"Не удалось открыть лист {sheet_name} даже с паролем: {e2}")
                    return None
            else:
                print(f"Ошибка чтения листа {sheet_name}: {e}")
                return None
    
    def process_pallet_order_sheet(self, df, file_date):
        """Обрабатывает лист 'Pallet Order'"""
        orders = []
        
        if df is None or df.empty:
            return orders
        
        # Ищем строки с заказами (клиенты в колонке A)
        for idx, row in df.iterrows():
            client_name = row.iloc[0] if len(row) > 0 else None
            
            # Пропускаем пустые строки и заголовки
            if pd.isna(client_name) or not isinstance(client_name, str) or client_name.strip() == "":
                continue
            
            # Извлекаем температуру
            temperature = self.extract_temperature(client_name)
            
            # Обрабатываем колонки B-Z для заказов
            for col_idx in range(1, min(26, len(row))):  # B-Z (колонки 1-25)
                delivery_name = df.iloc[0, col_idx] if len(df) > 0 else None  # Заголовок колонки
                pallet_count = row.iloc[col_idx] if col_idx < len(row) else None
                
                # Пропускаем пустые заказы
                if pd.isna(pallet_count) or pallet_count == 0:
                    continue
                
                order = {
                    'Date': file_date,
                    'Client_Name': client_name,
                    'Delivery_Name': delivery_name,
                    'Pallets_Ordered': pallet_count,
                    'Temperature': temperature,
                    'Source_Sheet': 'Pallet Order'
                }
                orders.append(order)
        
        return orders
    
    def process_collection_plan_sheet(self, df, file_date):
        """Обрабатывает лист 'Collection Plan'"""
        deliveries = []
        
        if df is None or df.empty:
            return deliveries
        
        # Ищем колонки по названиям
        columns = df.columns.tolist()
        column_mapping = {}
        
        for col in columns:
            col_str = str(col).lower()
            if 'load' in col_str and 'number' in col_str:
                column_mapping['load_number'] = col
            elif 'collection' in col_str and 'site' in col_str:
                column_mapping['collection_site'] = col
            elif 'delivery' in col_str and 'destination' in col_str:
                column_mapping['delivery_destination'] = col
            elif 'pallets' in col_str and 'ordered' in col_str:
                column_mapping['pallets_ordered'] = col
            elif 'pallet' in col_str and 'type' in col_str:
                column_mapping['pallet_type'] = col
            elif 'trailer' in col_str and 'type' in col_str:
                column_mapping['trailer_type'] = col
            elif 'trailer' in col_str and 'fill' in col_str:
                column_mapping['trailer_fill'] = col
        
        # Обрабатываем каждую строку как отдельную доставку
        for idx, row in df.iterrows():
            # Пропускаем пустые строки
            if row.isna().all():
                continue
            
            delivery = {
                'Date': file_date,
                'Source_Sheet': 'Collection Plan'
            }
            
            # Заполняем данные из найденных колонок
            for field, col in column_mapping.items():
                if col in df.columns and idx < len(df):
                    delivery[field] = row[col]
            
            # Добавляем все остальные колонки
            for col in df.columns:
                if col not in column_mapping.values() and idx < len(df):
                    delivery[f'extra_{col}'] = row[col]
            
            deliveries.append(delivery)
        
        return deliveries
    
    def merge_orders_and_deliveries(self, orders, deliveries):
        """Объединяет данные из 'Pallet Order' и 'Collection Plan'"""
        merged_data = []
        
        # Создаем словарь доставок по Load Number
        delivery_dict = {}
        for delivery in deliveries:
            load_number = delivery.get('load_number')
            if load_number:
                delivery_dict[load_number] = delivery
        
        # Объединяем заказы с доставками
        for order in orders:
            # Ищем подходящую доставку (можно улучшить логику сопоставления)
            best_match = None
            for delivery in deliveries:
                # Простая логика сопоставления по количеству паллет
                if (order.get('Pallets_Ordered') == delivery.get('pallets_ordered') and
                    order.get('Delivery_Name') == delivery.get('delivery_destination')):
                    best_match = delivery
                    break
            
            if best_match:
                # Объединяем данные
                merged_record = {**order, **best_match}
                merged_data.append(merged_record)
            else:
                # Добавляем заказ без сопоставленной доставки
                merged_data.append(order)
        
        # Добавляем доставки без сопоставленных заказов
        for delivery in deliveries:
            if not any(d.get('load_number') == delivery.get('load_number') for d in merged_data):
                merged_data.append(delivery)
        
        return merged_data
    
    def process_excel_file(self, file_path):
        """Обрабатывает один Excel файл"""
        print(f"Обрабатываю файл: {os.path.basename(file_path)}")
        
        # Извлекаем дату из имени файла
        filename = os.path.basename(file_path)
        file_date = self.extract_date_from_filename(filename)
        
        if not file_date:
            print(f"Не удалось извлечь дату из имени файла: {filename}")
            return []
        
        # Читаем лист 'Pallet Order'
        pallet_order_df = self.read_excel_sheet(file_path, 'Pallet Order')
        orders = self.process_pallet_order_sheet(pallet_order_df, file_date)
        
        # Читаем лист 'Collection Plan'
        collection_plan_df = self.read_excel_sheet(file_path, 'Collection Plan')
        deliveries = self.process_collection_plan_sheet(collection_plan_df, file_date)
        
        # Объединяем данные
        merged_data = self.merge_orders_and_deliveries(orders, deliveries)
        
        print(f"Извлечено {len(orders)} заказов, {len(deliveries)} доставок, {len(merged_data)} объединенных записей")
        return merged_data
    
    def find_excel_files(self, year_folder):
        """Находит все Excel файлы с маршрутами в указанной папке"""
        patterns = [
            os.path.join(year_folder, "**", "Lyons collections*.xlsx"),
            os.path.join(year_folder, "**", "Lyons collections*.xlsm")
        ]
        
        excel_files = []
        for pattern in patterns:
            files = glob.glob(pattern, recursive=True)
            excel_files.extend(files)
        
        # Убираем дубликаты и сортируем
        excel_files = list(set(excel_files))
        excel_files.sort()
        
        return excel_files
    
    def save_dataset(self):
        """Сохраняет датасет в CSV и Parquet форматах"""
        if not self.combined_data:
            print("Нет данных для сохранения")
            return
        
        df = pd.DataFrame(self.combined_data)
        
        # Сохраняем в CSV
        csv_path = "combined_dataset.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Датасет сохранен в CSV: {csv_path}")
        
        # Сохраняем в Parquet
        parquet_path = "combined_dataset.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"Датасет сохранен в Parquet: {parquet_path}")
        
        print(f"Всего записей в датасете: {len(df)}")
        print(f"Колонки: {list(df.columns)}")
    
    def run(self):
        """Основной метод запуска"""
        print("=== Dataset Builder for Logistics Routes ===")
        print("Сбор данных из Excel-файлов с ежедневными маршрутами")
        print()
        
        # Запрашиваем путь к папке с годом
        while True:
            year_path = input("Введите путь к папке с годом (например, W:\\Customers\\Natures Way reports\\Archive\\2024): ").strip()
            
            if os.path.exists(year_path):
                break
            else:
                print(f"Папка не найдена: {year_path}")
                print("Попробуйте еще раз или нажмите Ctrl+C для выхода")
        
        # Находим Excel файлы
        excel_files = self.find_excel_files(year_path)
        
        if not excel_files:
            print(f"Excel файлы не найдены в папке: {year_path}")
            return
        
        print(f"Найдено {len(excel_files)} Excel файлов")
        
        # Обрабатываем каждый файл
        new_records = 0
        for file_path in excel_files:
            try:
                file_records = self.process_excel_file(file_path)
                self.combined_data.extend(file_records)
                new_records += len(file_records)
            except Exception as e:
                print(f"Ошибка обработки файла {file_path}: {e}")
        
        print(f"\nОбработано файлов: {len(excel_files)}")
        print(f"Добавлено новых записей: {new_records}")
        
        # Сохраняем датасет
        self.save_dataset()
        
        print("\nОбработка завершена!")

def main():
    """Точка входа в программу"""
    try:
        builder = DatasetBuilder()
        builder.run()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
