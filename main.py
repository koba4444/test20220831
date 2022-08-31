# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

import pandas as pd
import pydeck as pdk
import streamlit as st

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    import streamlit as st
    st.title('My first app  111')
    st.write("""
                #My app
                Hello *world!*/n
                ##l;skjgirnigs
            """)

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

    df = pd.DataFrame(
        np.random.randn(100, 2) / [0.5, 0.5] + [55.5, 37.33],
        columns=['lat', 'lon'])
    st.map(df)

    #======================================


    st.title('Маршруты мусороуборочных машин в городе Остин')
    # Цвета для маршрутов по дням недели
    colors = {
        'Monday': [229, 42, 42],
        'Thursday': [98, 42, 229],
        'Wednesday': [42, 229, 61],
        'Tuesday': [221, 235, 23],
        'Friday': [144, 108, 26]
    }

    # Функция которая приводит столбец с геопозицией в необходимую форму
    def from_data_file(a):
        res = pd.DataFrame(columns=['latlng1', 'latlng2'])
        for i in a:
            route = i.split(', ')
            for j in range(len(route) - 1):
                res = res.append(pd.DataFrame(data=[[route[j], route[j + 1]]], columns=res.columns))
        res['lon'] = res['latlng1'].apply(lambda x: float(x.split(' ')[0]))
        res['lat'] = res['latlng1'].apply(lambda x: float(x.split(' ')[1]))
        res['lon2'] = res['latlng2'].apply(lambda x: float(x.split(' ')[0]))
        res['lat2'] = res['latlng2'].apply(lambda x: float(x.split(' ')[1]))
        res['inbound'] = 100
        res['outbound'] = 100
        res = res.drop(['latlng1', 'latlng2'], 1)
        res = res.reset_index(drop=True)
        return res

    data = pd.read_csv('garbage-routes-1.csv')
    # Удаляем ненужные символы из столбца с геопозициями
    data['the_geom'] = data['the_geom'].apply(
        lambda x: x.replace(')', '').replace('(', '').replace('MULTIPOLYGON ', ''))
    data = data.set_index('SERVICE_DAY')
    days = data.index.unique()
    ALL_LAYERS = {}
    # Добавляем слои на карту по дням недели
    for i in days:
        ALL_LAYERS[i] = pdk.Layer(
            "ArcLayer",
            data=from_data_file(data['the_geom'][i]),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=colors[i],
            get_target_color=colors[i],
            auto_highlight=True,
            width_scale=0.001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    st.sidebar.markdown('### Map Layers')
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state={"latitude": 30.367,
                                "longitude": -97.6, "zoom": 11, "pitch": 50},
            layers=selected_layers,
        ))
    else:
        st.error("Please choose at least one layer above.")
    #==========================================



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
