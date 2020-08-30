import os
import pickle
import PySimpleGUI as sg
import pandas as pd
import sys

model_file = os.path.join(os.path.curdir,"Output","model.pickle")

if not os.path.isfile(model_file):
       sg.Popup("Can't find required binaries. Exiting")
       quit()

with open(model_file, 'rb') as f:
    analyzer = pickle.load(f)

layout = [[sg.Text("-- Disclaimer e condizioni d'uso-- ", font=(None, 23, 'bold'))],
       [sg.Text("Questa applicazione è solo a scopo informativo,", font=(None, 23, 'bold'))],
       [sg.Text("Non sostituisce il parere del medico.", font=(None, 23, 'bold'))],
       [sg.Text("ATTENZIONE:", font=(None, 0, 'bold')),
       sg.Text(" L'applicazione ha lo scopo di informare sul possibile rischio di contrarre il diabete ", font=(None, 0)),
       sg.Text("in base alle informazioni date.", font=(None,0,'underline'))],
       [sg.Text("L'applicazione è stata sviluppata con cura, utilizzando dati ufficiali,"
       " tuttavia non è possibile garantire l'assenza di errori e la correttezza delle informazioni divulgate.", font=(None, 0))],
       [sg.Text("L'applicazione ha esclusivamente scopo informativo e non ha in alcun modo né la pretesa né l'obiettivo di sostituire il parere del medico e/o specialista, di altri\n"
       "operatori sanitari o professionisti del settore che devono in ogni caso essere contattati per la formulazione di una diagnosi o l'indicazione di un eventuale terapia,\n"
       "e più in generale per il confronto sulle suddette informazioni.", font=(None, 0))],
       [sg.Text("In caso si abbia qualsiasi dubbio sulla possibilità di aver sviluppato il diabete consigliamo VIVAMENTE di contattare il proprio medico.", font=(None, 0))],
       [sg.Text("In nessun caso l'applicazione, il programmatore che l'ha sviluppata, né altre soggetti connessi alla applicazione, saranno responsabili di qualsiasi eventuale\n"
       "danno anche solo ipoteticamente collegabile all'uso dei contenuti e/o di informazioni presenti sull'applicazione.", font=(None, 0))],
       [sg.Ok("Ho compreso quanto scritto e accetto le condizioni", key='-Ok-'), sg.Exit("Non accetto, fammi uscire dall'applicazione", pad=(20,0), key='-Exit-')]]

window = sg.Window('Disclaimer', layout, element_justification='center', element_padding=(0,0), finalize=True)

event, values = window.read()
window.close()

if event in (sg.WINDOW_CLOSED, '-Exit-'):
       quit()

layout = [[sg.Text('Età:', size=(22,1), justification='right'), sg.Input(key='Age', size=(12,1), enable_events=True)],
       [sg.Text('Sesso:', size=(22,1), justification='right'), sg.Combo(['Uomo', 'Donna'], key='Gender', default_value='Uomo', size=(10,1))],
       [sg.Text('Poliuria:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Polyuria', default_value='No', size=(10,1))],
       [sg.Text('Polidipsia:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Polydipsia', default_value='No', size=(10,1))],
       [sg.Text('Improvvisa perdita di peso:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='sudden weight loss', default_value='No', size=(10,1))],
       [sg.Text('Debolezza:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='weakness', default_value='No', size=(10,1))],
       [sg.Text('Polifagia:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Polyphagia', default_value='No', size=(10,1))],
       [sg.Text('Candida genitale:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Genital thrush', default_value='No', size=(10,1))],
       [sg.Text('Appannamento della visione:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='visual blurring', default_value='No', size=(10,1))],
       [sg.Text('Prurito:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Itching', default_value='No', size=(10,1))],
       [sg.Text('Irritabilità:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Irritability', default_value='No', size=(10,1))],
       [sg.Text('Ritardo nella cicatrizzazione:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='delayed healing', default_value='No', size=(10,1))],
       [sg.Text('Paresi parziale:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='partial paresis', default_value='No', size=(10,1))],
       [sg.Text('Indolenzimento muscolare:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='muscle stiffness', default_value='No', size=(10,1))],
       [sg.Text('Alopecia:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Alopecia', default_value='No', size=(10,1))],
       [sg.Text('Obesità:', size=(22,1), justification='right'), sg.Combo(['Sì','No'], key='Obesity', default_value='No', size=(10,1))],
       [sg.Column([[sg.OK('Invia', size=(10,2), key='-Enter-'), sg.Exit('Esci', size=(10,2), key='-Exit-')]], element_justification='center', expand_x=True)]]

# Display the window and get values

window = sg.Window('Inserisci i dati', layout)

while True:
       event, values = window.read()
       if event in (sg.WIN_CLOSED, '-Exit-'):
              break
       if event in ('-Enter-',):
              if values['Age'] and int(values['Age'])>=20:
                     break
              else:
                     sg.Popup("Inserisci un età tra 20 e 99 anni.")
       # if last character in input element is invalid, remove it
       if event == 'Age' and values['Age'] and (len(values['Age'])>2 or (values['Age'][-1] not in ('0123456789'))):
              window['Age'].update(values['Age'][:-1])

window.close()

if event in (sg.WIN_CLOSED, '-Exit-'):
       quit()

df = pd.DataFrame(columns=['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss', 
       'weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
       'Itching', 'Irritability', 'delayed healing', 'partial paresis',
       'muscle stiffness', 'Alopecia', 'Obesity','class'])

df = df.append(values, ignore_index=True)
df["Age"] = round(int(df["Age"]) / 10) * 10
df.replace(to_replace={"Uomo":1,"Donna":0, "Sì":1, "No":0}, inplace=True)
df = pd.DataFrame(analyzer['scaler'].transform(df), columns=df.columns)
df = df.drop(["class"], axis=1)


layout = [[sg.Text("La rischio di sviluppare il diabete è", font=(None, 23, 'bold'))]]
if analyzer['model'].predict(df)[0] < 0.5:
       layout.append([sg.Text("BASSO", font=(None, 23, 'bold'), text_color='green')])
else:
       layout.append([sg.Text("ALTO", font=(None, 23, 'bold'), text_color='red')])

layout.append([sg.Text("Per il nostro modello la probabilità che lei sia diabetico è dello {:.2f}%".format(100 * analyzer['model'].predict_proba(df)[0][1]), font=(None, 18))])
layout.append([sg.OK(size=(20,2))])

window = sg.Window('Inserisci i dati', layout, element_justification='center')
window.read()
window.close()