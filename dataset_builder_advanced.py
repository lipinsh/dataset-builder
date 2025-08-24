#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Dataset Builder for Logistics Routes
Улучшенная версия скрипта для сбора данных из Excel-файлов с ежедневными маршрутами
"""

import os
import re
import pandas as pd
import glob
from datetime import datetime
from pathlib import Path
import warnings
import logging
from typing import List, Dict, Any, Optional
warnings.filterwarnings('ignore')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataset_builder.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AdvancedDatasetBuilder:
    def __init__(self):
        self.combined_data = []
        self.processed_files = set()
        self.load_existing_dataset()
        
        # Статистика
        self.stats = {
            'files_processed': 0,
            'files_skipped': 0,
            'orders_extracted': 0,
            'deliveries_extracted': 0,
            'errors': 0
        }
    
    def load_existing_dataset(self):
        """Загружает существующий датасет для добавления новых данных"""
        csv_path = "combined_dataset.csv"
        parquet_path = "combined_dataset.parquet"
        
        if os.path.exists(csv_path):
            try:
                existing_df = pd.read_csv(csv_path)
                self.combined_data = existing_df.to_dict('records')
                logging.info(f"Загружен существующий датасет: {len(self.combined_data)} записей")
                
                # Загружаем список уже обработанных файлов
                if 'Source_File' in existing_df.columns:
                    self.processed_files = set(existing_df['Source_File'].unique())
                    
            except Exception as e:
                logging.error(f"Ошибка загрузки существующего датасета: {e}")
        elif os.path.exists(parquet_path):
            try:
                existing_df = pd.read_parquet(parquet_path)
                self.combined_data = existing_df.to_dict('records')
                logging.info(f"Загружен существующий датасет: {len(self.combined_data)} записей")
                
                if 'Source_File' in existing_df.columns:
                    self.processed_files = set(existing_df['Source_File'].unique())
                    
            except Exception as e:
                logging.error(f"Ошибка загрузки существующего датасета: {e}")
    
    def extract_date_from_filename(self, filename: str) -> Optional[str]:
        """Извлекает дату из имени файла с улучшенной логикой"""
        # Паттерны для поиска даты
        patterns = [
            r'(\d{2})(\d{2})(\d{4})',  # DDMMYYYY
            r'(\d{2})(\d{2})(\d{2})',  # DDMMYY
            r'(\d{1,2})[-_](\d{1,2})[-_](\d{2,4})',  # DD-MM-YY или DD_MM_YY
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                groups = match.groups()
                
                if len(groups) == 3:
                    if len(groups[2]) == 2:  # YY
                        day, month, year = groups
                        # Предполагаем, что год 20xx
                        full_year = f"20{year}"
                    elif len(groups[2]) == 4:  # YYYY
                        day, month, year = groups
                        full_year = year
                    else:
                        continue
                    
                    try:
                        date_obj = datetime(int(full_year), int(month), int(day))
                        return date_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
        
        return None
    
    def extract_temperature(self, client_name: str) -> str:
        """Извлекает температуру из названия клиента"""
        if not client_name or not isinstance(client_name, str):
            return "+3°C"
        
        # Паттерны для поиска температуры
        temp_patterns = [
            r'\(\+(\d+)°C\)',
            r'\+(\d+)°C',
            r'(\d+)°C',
            r'(\d+)C',
        ]
        
        for pattern in temp_patterns:
            match = re.search(pattern, client_name, re.IGNORECASE)
            if match:
                temp_value = match.group(1)
                return f"+{temp_value}°C"
        
        return "+3°C"  # По умолчанию
    
    def read_excel_sheet(self, file_path: str, sheet_name: str, password: str = None) -> Optional[pd.DataFrame]:
        """Читает лист Excel с улучшенной обработкой ошибок"""
        try:
            if password:
                return pd.read_excel(file_path, sheet_name=sheet_name, password=password)
            else:
                return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            error_msg = str(e).lower()
            
            if "password" in error_msg:
                logging.info(f"Лист {sheet_name} защищен паролем. Пробуем с паролем 'Test'...")
                try:
                    return pd.read_excel(file_path, sheet_name=sheet_name, password="Test")
                except Exception as e2:
                    logging.warning(f"Не удалось открыть лист {sheet_name} даже с паролем: {e2}")
                    return None
            elif "sheet" in error_msg and "not found" in error_msg:
                logging.warning(f"Лист '{sheet_name}' не найден в файле {os.path.basename(file_path)}")
                return None
            else:
                logging.error(f"Ошибка чтения листа {sheet_name}: {e}")
                return None
    
    def find_header_row(self, df: pd.DataFrame) -> int:
        """Находит строку с заголовками в таблице"""
        if df is None or df.empty:
            return 0
        
        # Ищем строку с заголовками (содержит ключевые слова)
        header_keywords = ['client', 'customer', 'delivery', 'pallet', 'load', 'collection']
        
        for idx, row in df.iterrows():
            row_str = ' '.join(str(cell).lower() for cell in row if pd.notna(cell))
            if any(keyword in row_str for keyword in header_keywords):
                return idx
        
        return 0
    
    def process_pallet_order_sheet(self, df: pd.DataFrame, file_date: str, filename: str) -> List[Dict[str, Any]]:
        """Обрабатывает лист 'Pallet Order' с улучшенной логикой"""
        orders = []
        
        if df is None or df.empty:
            return orders
        
        # Находим строку с заголовками
        header_row = self.find_header_row(df)
        
        # Получаем заголовки доставок (колонки B-Z)
        delivery_headers = []
        for col_idx in range(1, min(26, len(df.columns))):
            if header_row < len(df):
                header_value = df.iloc[header_row, col_idx]
                if pd.notna(header_value) and str(header_value).strip():
                    delivery_headers.append((col_idx, str(header_value).strip()))
        
        # Обрабатываем строки с заказами
        for idx, row in df.iterrows():
            if idx <= header_row:  # Пропускаем заголовки
                continue
            
            client_name = row.iloc[0] if len(row) > 0 else None
            
            # Пропускаем пустые строки
            if pd.isna(client_name) or not isinstance(client_name, str) or client_name.strip() == "":
                continue
            
            # Извлекаем температуру
            temperature = self.extract_temperature(client_name)
            
            # Обрабатываем заказы по колонкам
            for col_idx, delivery_name in delivery_headers:
                if col_idx < len(row):
                    pallet_count = row.iloc[col_idx]
                    
                    # Пропускаем пустые заказы
                    if pd.isna(pallet_count) or pallet_count == 0:
                        continue
                    
                    order = {
                        'Date': file_date,
                        'Client_Name': client_name.strip(),
                        'Delivery_Name': delivery_name,
                        'Pallets_Ordered': float(pallet_count),
                        'Temperature': temperature,
                        'Source_Sheet': 'Pallet Order',
                        'Source_File': filename
                    }
                    orders.append(order)
        
        return orders
    
    def process_collection_plan_sheet(self, df: pd.DataFrame, file_date: str, filename: str) -> List[Dict[str, Any]]:
        """Обрабатывает лист 'Collection Plan' с улучшенной логикой"""
        deliveries = []
        
        if df is None or df.empty:
            return deliveries
        
        # Находим строку с заголовками
        header_row = self.find_header_row(df)
        
        # Создаем DataFrame с правильными заголовками
        if header_row > 0:
            df_clean = df.iloc[header_row:].reset_index(drop=True)
            df_clean.columns = df.iloc[header_row]
        else:
            df_clean = df
        
        # Ищем колонки по названиям
        columns = df_clean.columns.tolist()
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
            elif 'driver' in col_str:
                column_mapping['driver'] = col
            elif 'vehicle' in col_str:
                column_mapping['vehicle'] = col
            elif 'route' in col_str:
                column_mapping['route'] = col
        
        # Обрабатываем каждую строку как отдельную доставку
        for idx, row in df_clean.iterrows():
            # Пропускаем пустые строки
            if row.isna().all():
                continue
            
            delivery = {
                'Date': file_date,
                'Source_Sheet': 'Collection Plan',
                'Source_File': filename
            }
            
            # Заполняем данные из найденных колонок
            for field, col in column_mapping.items():
                if col in df_clean.columns and idx < len(df_clean):
                    value = row[col]
                    if pd.notna(value):
                        delivery[field] = value
            
            # Добавляем все остальные колонки
            for col in df_clean.columns:
                if col not in column_mapping.values() and idx < len(df_clean):
                    value = row[col]
                    if pd.notna(value):
                        delivery[f'extra_{col}'] = value
            
            deliveries.append(delivery)
        
        return deliveries
    
    def merge_orders_and_deliveries(self, orders: List[Dict], deliveries: List[Dict]) -> List[Dict]:
        """Объединяет данные из 'Pallet Order' и 'Collection Plan' с улучшенной логикой"""
        merged_data = []
        
        # Создаем словарь доставок по ключевым признакам
        delivery_dict = {}
        for delivery in deliveries:
            key = (
                delivery.get('delivery_destination'),
                delivery.get('pallets_ordered'),
                delivery.get('collection_site')
            )
            if key[0] and key[1]:  # Есть место доставки и количество паллет
                delivery_dict[key] = delivery
        
        # Объединяем заказы с доставками
        for order in orders:
            key = (
                order.get('Delivery_Name'),
                order.get('Pallets_Ordered'),
                None  # collection_site из заказа не доступен
            )
            
            best_match = None
            if key in delivery_dict:
                best_match = delivery_dict[key]
            else:
                # Ищем частичное совпадение
                for delivery in deliveries:
                    if (order.get('Delivery_Name') == delivery.get('delivery_destination') and
                        order.get('Pallets_Ordered') == delivery.get('pallets_ordered')):
                        best_match = delivery
                        break
            
            if best_match:
                # Объединяем данные, избегая дублирования
                merged_record = {**order}
                for k, v in best_match.items():
                    if k not in merged_record or pd.isna(merged_record[k]):
                        merged_record[k] = v
                merged_data.append(merged_record)
            else:
                # Добавляем заказ без сопоставленной доставки
                merged_data.append(order)
        
        # Добавляем доставки без сопоставленных заказов
        for delivery in deliveries:
            if not any(d.get('load_number') == delivery.get('load_number') for d in merged_data):
                merged_data.append(delivery)
        
        return merged_data
    
    def process_excel_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Обрабатывает один Excel файл"""
        filename = os.path.basename(file_path)
        logging.info(f"Обрабатываю файл: {filename}")
        
        # Проверяем, не обрабатывали ли мы уже этот файл
        if filename in self.processed_files:
            logging.info(f"Файл {filename} уже обработан, пропускаем")
            self.stats['files_skipped'] += 1
            return []
        
        # Извлекаем дату из имени файла
        file_date = self.extract_date_from_filename(filename)
        
        if not file_date:
            logging.warning(f"Не удалось извлечь дату из имени файла: {filename}")
            self.stats['errors'] += 1
            return []
        
        try:
            # Читаем лист 'Pallet Order'
            pallet_order_df = self.read_excel_sheet(file_path, 'Pallet Order')
            orders = self.process_pallet_order_sheet(pallet_order_df, file_date, filename)
            
            # Читаем лист 'Collection Plan'
            collection_plan_df = self.read_excel_sheet(file_path, 'Collection Plan')
            deliveries = self.process_collection_plan_sheet(collection_plan_df, file_date, filename)
            
            # Объединяем данные
            merged_data = self.merge_orders_and_deliveries(orders, deliveries)
            
            # Обновляем статистику
            self.stats['orders_extracted'] += len(orders)
            self.stats['deliveries_extracted'] += len(deliveries)
            self.stats['files_processed'] += 1
            
            logging.info(f"Извлечено {len(orders)} заказов, {len(deliveries)} доставок, {len(merged_data)} объединенных записей")
            
            return merged_data
            
        except Exception as e:
            logging.error(f"Ошибка обработки файла {filename}: {e}")
            self.stats['errors'] += 1
            return []
    
    def find_excel_files(self, year_folder: str) -> List[str]:
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
            logging.warning("Нет данных для сохранения")
            return
        
        df = pd.DataFrame(self.combined_data)
        
        # Очищаем данные
        df = df.replace('', pd.NA)
        df = df.dropna(how='all')  # Удаляем полностью пустые строки
        
        # Сохраняем в CSV
        csv_path = "combined_dataset.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        logging.info(f"Датасет сохранен в CSV: {csv_path}")
        
        # Сохраняем в Parquet
        parquet_path = "combined_dataset.parquet"
        df.to_parquet(parquet_path, index=False)
        logging.info(f"Датасет сохранен в Parquet: {parquet_path}")
        
        logging.info(f"Всего записей в датасете: {len(df)}")
        logging.info(f"Колонки: {list(df.columns)}")
        
        # Сохраняем статистику
        self.save_statistics()
    
    def save_statistics(self):
        """Сохраняет статистику обработки"""
        stats_df = pd.DataFrame([self.stats])
        stats_df.to_csv("processing_statistics.csv", index=False)
        logging.info("Статистика сохранена в processing_statistics.csv")
    
    def run(self):
        """Основной метод запуска"""
        print("=== Advanced Dataset Builder for Logistics Routes ===")
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
            logging.warning(f"Excel файлы не найдены в папке: {year_path}")
            return
        
        logging.info(f"Найдено {len(excel_files)} Excel файлов")
        
        # Обрабатываем каждый файл
        new_records = 0
        for file_path in excel_files:
            try:
                file_records = self.process_excel_file(file_path)
                self.combined_data.extend(file_records)
                new_records += len(file_records)
            except Exception as e:
                logging.error(f"Критическая ошибка обработки файла {file_path}: {e}")
                self.stats['errors'] += 1
        
        logging.info(f"\nОбработано файлов: {self.stats['files_processed']}")
        logging.info(f"Пропущено файлов: {self.stats['files_skipped']}")
        logging.info(f"Ошибок: {self.stats['errors']}")
        logging.info(f"Извлечено заказов: {self.stats['orders_extracted']}")
        logging.info(f"Извлечено доставок: {self.stats['deliveries_extracted']}")
        logging.info(f"Добавлено новых записей: {new_records}")
        
        # Сохраняем датасет
        self.save_dataset()
        
        print("\nОбработка завершена!")
        print(f"Результат сохранен в файлы:")
        print("- combined_dataset.csv")
        print("- combined_dataset.parquet")
        print("- processing_statistics.csv")
        print("- dataset_builder.log")

def main():
    """Точка входа в программу"""
    try:
        builder = AdvancedDatasetBuilder()
        builder.run()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        logging.info("Программа прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        logging.error(f"Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
