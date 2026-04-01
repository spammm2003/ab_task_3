import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title='Аналіз Telegram-каналу', page_icon='📈', layout='wide')

st.title('📈 Аналіз активності Telegram-каналу')

# --- 1. Завантаження даних ---
@st.cache_data
def load_data():
    df = pd.read_csv('telegram_data.csv')
    # Перетворюємо колонку Дата_Час у формат datetime для зручної роботи з часом
    df['Дата_Час'] = pd.to_datetime(df['Дата_Час'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Файл 'telegram_data.csv' не знайдено. Будь ласка, створіть його за зразком.")
    st.stop()

# --- 2. Обчислення коефіцієнта залучення (ER - Engagement Rate) ---
# Формула: (Реакції / Перегляди) * 100
df['ER (%)'] = (df['Реакції'] / df['Перегляди']) * 100
df['ER (%)'] = df['ER (%)'].round(2) # Округлюємо до 2 знаків

st.subheader('📋 Дані постів та Коефіцієнт залучення (ER)')
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# --- 3. Графік активності ---
st.subheader('📊 Графік активності (Перегляди та Реакції)')
st.write("Динаміка переглядів та реакцій з часом.")

# Встановлюємо час як індекс для правильного відображення на осі X
chart_data = df.set_index('Дата_Час')[['Перегляди', 'Реакції']]
st.line_chart(chart_data)

st.divider()

# --- 4. Визначення найефективнішого часу для публікацій ---
st.subheader('⏰ Найефективніший час для публікацій')

# Витягуємо годину публікації з дати
df['Година'] = df['Дата_Час'].dt.hour

# Групуємо дані за годиною і рахуємо середні показники
hourly_stats = df.groupby('Година')[['Перегляди', 'ER (%)']].mean().reset_index()

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Середня кількість переглядів за годинами**")
    st.bar_chart(hourly_stats.set_index('Година')['Перегляди'])

with col2:
    st.markdown("**Середній рівень залучення (ER %) за годинами**")
    st.bar_chart(hourly_stats.set_index('Година')['ER (%)'])

# Аналітичний висновок
best_hour_views = hourly_stats.loc[hourly_stats['Перегляди'].idxmax()]['Година']
best_hour_er = hourly_stats.loc[hourly_stats['ER (%)'].idxmax()]['Година']

st.info(f"""
💡 **Аналітичні висновки:**
* Найбільше **переглядів** у середньому збирають пости, опубліковані о **{int(best_hour_views)}:00**.
* Найвища **активність аудиторії (реакції, ER)** спостерігається у постах, опублікованих о **{int(best_hour_er)}:00**.

Рекомендація: Плануйте найважливіші пости ближче до {int(best_hour_er)}:00 для максимального залучення аудиторії.
""")
