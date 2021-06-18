from pathlib import Path

import requests
import streamlit as st


data_freqs = {
    'Daily': 'D',
    'Weekly': 'W',
    'Monthly': 'M',
    'Quarterly': 'Q',
    'Yearly': 'Y',
}

st.write('[Create user](https://forms.gle/DCKc6WVTSBLMJ3VK7)')
token = st.text_input('Token', type='password')
input_path = Path(st.text_input('Training path'))
input_freq = st.selectbox('Data frequency', list(data_freqs.keys()))
horizon = st.number_input('Forecast horizon', value=7)
backtest_windows = st.number_input('Backtest windows', value=0)

if st.button('Run forecast'):
    data_prefix = input_path.parent
    data_input = input_path.name
    data_format = input_path.suffix.replace('.', '')

    url = st.secrets['API_URL']
    header = {'x-api-key': token}
    body = dict(
        data={
            'prefix': str(data_prefix),
            'input': data_input,
            'format': data_format,
        },
        features={
            'freq': data_freqs[input_freq],
        },
        backtest={
            'n_windows': str(backtest_windows),
        },
        forecast={
            'horizon': str(horizon),
        }
    )
    resp = requests.post(url, json=body, headers=header)
    st.text(requests.status_codes._codes[resp.status_code][0].capitalize())
