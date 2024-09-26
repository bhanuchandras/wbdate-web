from flask import Flask, render_template,json,request, redirect
import pandas as pd
import wbdata
import logging, ast


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/gdppc/<country>')
@app.route('/gdppc/',defaults={'country': 'IND'})
def get_gdppc(country):
    df=wbdata.get_dataframe({ "NY.GDP.PCAP.PP.KD" : "gdppc" },country=[country],parse_dates=True)
    df['country']=country
    return df.reset_index().to_json(orient='records')

@app.route('/gdppc_comb')
def get_gdppc2():
    cntry_lst = request.args.get('country')
    cntry_data=[]
    #print(cntry_lst)
    if cntry_lst :
        #cntry_data = json.loads(cntry_lst)
        cntry_data = ast.literal_eval(cntry_lst)
    #    df=wbdata.get_dataframe({ "NY.GDP.PCAP.PP.KD" : "gdppc" },country=cntry_data,parse_dates=True)
    #else:
    #    df=wbdata.get_dataframe({ "NY.GDP.PCAP.PP.KD" : "gdppc" },country=['IND','USA'],parse_dates=True)
    #print(df)
    #print(df.T)
    #return df.reset_index().to_json(orient='records')
    start=0
    merged=pd.DataFrame()
    if len(cntry_data) > 1:
        for c in cntry_data:
            if start==0:
              df1=wbdata.get_dataframe({ "NY.GDP.PCAP.PP.KD" : "gdppc" },country=[c],parse_dates=True)
              start=1
              suff1=c
            else:
              df2=wbdata.get_dataframe({ "NY.GDP.PCAP.PP.KD" : "gdppc" },country=[c],parse_dates=True)
              merged = df1.merge(df2, on='date', suffixes=('_'+suff1, '_'+c))
            print(merged)
        df=merged
    else:
        df=wbdata.get_dataframe({ "NY.GDP.PCAP.PP.KD" : "gdppc" },country=[cntry_data[0]],parse_dates=True)
    return (df.reset_index().to_json(orient='records'))

@app.route('/cntry_list')
def fetch_countries_and_income_levels():
    try:
        countries = wbdata.get_countries()
        country_income_data = []
        #print(dir(countries))
        for country in countries:
            #print(country)
            id=country['id']
            name = country['name']
            income_level = country['incomeLevel']['value']
            capital = country['capitalCity']
            region = country['region']['value']
            country_income_data.append((id,name,capital, income_level,region))
            df = pd.DataFrame(country_income_data)
            df.columns=["id","Country","capital","income_level","region"]
        return df.to_json(orient='records')
    except json.decoder.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        return None
    except requests.exceptions.RequestException as e:
        print("RequestException:", e)
        return None
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
