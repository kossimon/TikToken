import streamlit as st
import tiktoken
import os
from dotenv import load_dotenv
import requests


models = {'GPT-4 (až 32 tisíc tokenů)':{
                    'name':'gpt-4',
                    'input': 0.06,
                    'output': 0.12
                    },
        'chatGPT-3.5 (až 16 tisíc tokenů)':{    
                    'name':'gpt-3.5-turbo',
                    'input' : 0.003,
                    'output': 0.004,
                    }
        }

load_dotenv()
CURR_API_KEY = os.getenv("CURR_API_KEY")

cr_url = f'https://v6.exchangerate-api.com/v6/{CURR_API_KEY}/latest/USD'
cr_json = requests.get(cr_url).json()
cr = cr_json["conversion_rates"]['CZK']


def write_response(response_input,enc):
    resp_len_box.markdown('**Spotřeba tokenů na Odpověď**')

    report = []
    if response_input:
        resp_enc = enc.encode(response_input)
        for i in resp_enc:
            report.append([i])
            resp_enc_box.text_area(label='Tokeny v Odpovědi', value=report,height=200 )
        resp_len = len(resp_enc)
        re_cena = resp_len * cr * models[select_model]['output'] / 1000
        resp_len_box.markdown(f'**{resp_len} tokenů.**')
        resp_cena_box.subheader(f'**{re_cena:.8f} KČ.**')
        return re_cena

def write_prompt(prompt_input,enc):
     prompt_len_box.markdown('**Spotřeba tokenů na Prompt**')
     report = []
     if prompt_input:
        prompt_enc = enc.encode(prompt_input)
        for i in prompt_enc:
            report.append([i])
            prompt_enc_box.markdown('**Tokeny v Promptu**')
            prompt_enc_box.text_area(label='Tokeny v Promptu', value=report,height=200 )
        prompt_len = len(prompt_enc)
        pro_cena = prompt_len * cr * models[select_model]['input'] / 1000
        prompt_len_box.markdown(f'**{prompt_len} tokenů.**')
        prompt_cena_box.subheader(f'**{pro_cena:.8f} KČ.**')
        return pro_cena

def write_cena(pro_cena,re_cena):
    cena_celkem = pro_cena + re_cena
    cena_celkem_box.markdown('___')
    cena_celkem_box.markdown('**Celková cena**')
    cena_celkem_box.subheader(f'**{cena_celkem:.8f} Kč**')
    cena_celkem_box.markdown('___')

hide_streamlit_style = """
<style>
  #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 1rem;}
  header {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Step 3: Create UI elements
prompt_input = st.text_area('Vložte Prompt',
                              height=150,
                              label_visibility="collapsed")
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
        enc = tiktoken.encoding_for_model(models[select_model]['name'])
        pro_cena = write_prompt(prompt_input,enc)
        re_cena = write_response(response_input,enc)
        if pro_cena and re_cena:
            write_cena(pro_cena,re_cena)
    else:
        st.error('Vyberte model', icon="🚨")

        