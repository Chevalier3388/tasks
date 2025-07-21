import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Настройки для визуализации (обновлённые)
plt.style.use('seaborn-v0_8')  # Или другой доступный стиль
sns.set_theme(style="whitegrid")  # Современный способ установки стиля в seaborn

API_KEY = "Ваш API-ключ"  # Замените на реальный ключ с сайта openweathermap.org!
CITY = input("Введите город (например: Moscow, London, Berlin): ")
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(URL)
    data = response.json()

    # Проверка ошибок API
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}: {data.get('message', 'Неизвестная ошибка')}")
        exit()

    if 'list' not in data:
        print("Ошибка: API не вернул данные. Ответ:", data)
        exit()

    # Парсинг данных
    weather_data = []
    for forecast in data['list']:
        weather_data.append({
            'date': forecast['dt_txt'],
            'temp': forecast['main']['temp'],
            'feels_like': forecast['main']['feels_like'],
            'temp_min': forecast['main']['temp_min'],
            'temp_max': forecast['main']['temp_max'],
            'humidity': forecast['main']['humidity'],
            'pressure': forecast['main']['pressure'],
            'wind_speed': forecast['wind']['speed'],
            'wind_deg': forecast['wind']['deg'],
            'weather': forecast['weather'][0]['main'],
            'clouds': forecast['clouds']['all']
        })

    # Создание DataFrame
    df = pd.DataFrame(weather_data)
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date'].dt.time
    df['day'] = df['date'].dt.date

    # Сохранение в CSV
    df.to_csv('weather_data.csv', index=False)
    print("Данные сохранены в weather_data.csv!")

    # Визуализация
    plt.figure(figsize=(15, 10))

    # 1. График температуры
    plt.subplot(2, 2, 1)
    sns.lineplot(data=df, x='date', y='temp', label='Температура')
    sns.lineplot(data=df, x='date', y='feels_like', label='Ощущается как')
    plt.title(f'Температура в {CITY}')
    plt.xlabel('Дата и время')
    plt.ylabel('Температура (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # 2. График влажности и давления
    plt.subplot(2, 2, 2)
    ax1 = sns.lineplot(data=df, x='date', y='humidity', color='blue', label='Влажность')
    plt.ylabel('Влажность (%)', color='blue')
    ax2 = plt.twinx()
    sns.lineplot(data=df, x='date', y='pressure', color='red', ax=ax2, label='Давление')
    plt.ylabel('Давление (hPa)', color='red')
    plt.title('Влажность и давление')
    plt.xticks(rotation=45)
    plt.grid(True)

    # 3. График скорости ветра
    plt.subplot(2, 2, 3)
    sns.barplot(data=df, x='time', y='wind_speed', hue='day', palette='viridis')
    plt.title('Скорость ветра по времени суток')
    plt.xlabel('Время')
    plt.ylabel('Скорость ветра (м/с)')
    plt.xticks(rotation=45)
    plt.legend(title='День', bbox_to_anchor=(1.05, 1), loc='upper left')

    # 4. Распределение погодных условий
    plt.subplot(2, 2, 4)
    weather_counts = df['weather'].value_counts()
    plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Распределение погодных условий')

    plt.tight_layout()
    plt.savefig('weather_visualization.png')
    plt.close()

    print("Визуализация сохранена в weather_visualization.png!")

except Exception as e:
    print("Ошибка:", e)