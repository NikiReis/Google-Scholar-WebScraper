def etl_process():
    import pandas as pd

    filter_year = int(input('Deseja artigos a partir de que ano ? '))

    df = pd.read_csv('rawdata\\dadosraiz.csv', sep=',', encoding='utf-8', na_values= '****')

    year_less_2000 = df['Year'] < filter_year
    df.drop(df[year_less_2000].index, inplace=True)

    df['Year'] = df['Year'].astype('str')
    df.fillna('Dados não disponíveis', inplace=True)

    df.to_csv('arquivos\\dados.csv', index=False)
