import streamlit as st
import tiktoken
import os
from dotenv import load_dotenv
import requests
import time

def time_execution(function, *args):
    start_time = time.time()  # record the start time (in seconds)
    result = function(*args)  # execute the function
    end_time = time.time()  # record the end time (in seconds)
    duration = end_time - start_time  # calculate the duration
    return result, duration

enc_3= tiktoken.encoding_for_model('gpt-3.5-turbo')
enc_4= tiktoken.encoding_for_model('gpt-4')


models = {'GPT-4 (až 32 tisíc tokenů)':{
                    'name':'gpt-4',
                    'encoder': enc_4,
                    'input': 0.06,
                    'output': 0.12
                    },
        'chatGPT-3.5 (až 16 tisíc tokenů)':{    
                    'name':'gpt-3.5-turbo',
                    'encoder': enc_3,
                    'input' : 0.003,
                    'output': 0.004,
                    }
        }

load_dotenv()
CURR_API_KEY = os.getenv("CURR_API_KEY")

def get_currency():
    try:
        cr_url = f'https://v6.exchangerate-api.com/v6/{CURR_API_KEY}/latest/USD'
        cr_json = requests.get(cr_url).json()
        cr = cr_json["conversion_rates"]['CZK']
        currency = 'Kč'

    except:
        st.toast('Problém s nahráním měnového kurzu, cena bude spočítána v $.' , icon="🚨")
        cr = 1
        currency = '$'

    return cr, currency


cr, currency = get_currency()
# st.write(f'Loaded encoder in {time_enc_3:.8f}, Loaded encoder in {time_enc_4:.8f}, Loaded currency in {time_cr:.3f}')


def write_response(response_input,enc):
    resp_len_box.markdown('___')
    if response_input:
        resp_len_box.markdown('**Spotřeba tokenů na Odpověď**')
        resp_enc = enc.encode(response_input)
        resp_enc_box.text_area(label='Tokeny v Odpovědi', value=str(resp_enc),height=200 )
        resp_len = len(resp_enc)
        re_cena = resp_len * cr * models[select_model]['output'] / 1000
        resp_len_box.markdown(f'**{resp_len} tokenů.**')
        resp_cena_box.subheader(f'**{re_cena:.8f} {currency}**')
        return re_cena

def write_prompt(prompt_input,enc):
    prompt_len_box.markdown('___')
    if prompt_input:
        prompt_len_box.markdown('**Spotřeba tokenů na Prompt**')
        prompt_enc = enc.encode(prompt_input)
        prompt_enc_box.text_area(label='Tokeny v Promptu', value=str(prompt_enc),height=200 )
        prompt_len = len(prompt_enc)
        pro_cena = prompt_len * cr * models[select_model]['input'] / 1000
        prompt_len_box.markdown(f'**{prompt_len} tokenů.**')
        prompt_cena_box.subheader(f'**{pro_cena:.8f} {currency}**')
        prompt_cena_box.markdown('___')
        return pro_cena

def write_cena(pro_cena,re_cena):
    cena_celkem = pro_cena + re_cena
    cena_celkem_box.markdown('___')
    cena_celkem_box.markdown('**Celková cena**')
    cena_celkem_box.subheader(f'**{cena_celkem:.8f} {currency}**')
    cena_celkem_box.markdown('___')

hide_streamlit_style = """
<style>
  #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
  header {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.subheader('Vložte znění vašeho promptu')
prompt_input = st.text_area('Vložte Prompt',
                              height=150,
                              label_visibility="collapsed")

st.subheader('Vložte znění odpovědi chatGPT')
response_input = st.text_area('Vložte Odpověď modelu',
                              height=150,
                              label_visibility="collapsed")

select_model = st.selectbox('Vyberte model', ('GPT-4 (až 32 tisíc tokenů)', 'chatGPT-3.5 (až 16 tisíc tokenů)'),index = None, placeholder="Vyberte model")

convert_button = st.button('Spočítat tokeny')



prmpt1, prmpt2 = st.columns([1,1])

with prmpt1:
    prompt_len_box = st.container()
    prompt_cena_box = st.container()

with prmpt2:
    resp_len_box = st.container()
    resp_cena_box = st.container()
    cena_celkem_box = st.container()


resp1, resp2 = st.columns([1,1])
with resp1:
    prompt_enc_box = st.empty()
with resp2:
    resp_enc_box = st.empty()

if convert_button:
    if select_model:
        enc = models[select_model]['encoder']       
        pro_cena = write_prompt(prompt_input,enc)
        re_cena = write_response(response_input,enc)
        if pro_cena and re_cena:
            write_cena(pro_cena,re_cena)
    else:
        st.error('Vyberte model', icon="🚨")

        
