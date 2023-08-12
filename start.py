from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from typing import List
import os

from config import directory_path, main_file, output_file
from tech import file_search

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Allow requests from any origin
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
    allow_credentials=True  # Allow sending cookies
)

#Main section
@app.get("/")
async def main_Banner_Hello_Page():
    """Главная страница"""
    return {"Разработано":"Иорин Д.А Богданов Д.А"}


@app.get("/main")
async def main_Print_File_Reestr_Function():
    """Метод возвращает Реестр операций.xlsm"""
    df = pd.read_excel(output_file)
    res = df.to_json(force_ascii=False, orient='columns')
    return [res]


@app.get("/main_download")
async def main_download_Function():
    """Метод загружает пользователю Реестр операций.xlsm"""
    return FileResponse(path=output_file, filename=output_file, media_type="application/vnd.ms-excel")


@app.get("/list_files")
async def list_files_Function():
    """Метод возвращает спискок файлов .xlsm"""
    arr_list = []
    file_list = os.listdir(directory_path)
    for item in range(len(file_list)):
        file_list_vlojenie = os.listdir(f"{directory_path}/{file_list[item]}")
        for file in file_list_vlojenie:
            arr_list.append(f"{file}")
    return arr_list


@app.get("/get_current_files/{item_str}")
async def get_current_Function(item_str: str):
    '''Отправляет файл по запросу'''
    res = file_search.search_file(item_str, directory_path)
    if res:
        return FileResponse(path=res, filename=res, media_type="application/vnd.ms-excel")
    else:
        return {"error": 'no such file'}


@app.get("/analytics")
async def main_analytics_Function():
    """Метод возвращает аналитику по Реестр операций.xlsm"""
    df = pd.read_excel(output_file)
    unique_categories = df['Участок'].unique()
    anal = []
    for uu in unique_categories:
        filtered_df = df[df['Участок'] == uu]
        hours_total = filtered_df['Время всего'].sum()
        filtered_df_againt = filtered_df[filtered_df['Дата изготовления'].notna()]
        fact_time = filtered_df_againt['Время всего'].sum()
        print([uu, hours_total, fact_time])
        anal.append(str([uu, hours_total, fact_time]))
    return anal

@app.get("/avaliable_surnames")
async def avaliable_surnames_Function():
    """Метод возвращает фамилии Реестр операций.xlsm"""
    df = pd.read_excel(output_file)
    unique_categories = df['Фамилия исполнителя'].dropna().unique()
    unique_categories = list(unique_categories)
    print(unique_categories)
    return unique_categories

@app.get("/filter_analytics/{surname}")
async def main_filter_analytics_Function(surname: str):
    """Метод возвращает аналитику c фильтрами по фамилии Реестр операций.xlsm"""
    df = pd.read_excel(output_file)
    filtered_df = df[df['Фамилия исполнителя'] == surname]
    print(filtered_df)
    prik_zavod = filtered_df["Участок"]
    print(prik_zavod[0])
    total_vork = df[df['Участок'] == prik_zavod[0]]['Кол-во'].sum()
    print(total_vork)

    persent = filtered_df['Кол-во'].sum() / total_vork

    hours_total = filtered_df['Время всего'].sum()
    print(surname, hours_total, persent)
    return (surname, str(hours_total), f"{round(persent, 2)}%")

    #res = df.to_json(force_ascii=False, orient='columns')
    #return [res]


@app.get("/update")
async def update_Function():
    """Метод обновляет Реестр операций.xlsm"""
    df = pd.read_excel(main_file)
    file_list = os.listdir(directory_path)
    error_log = []
    counter = 1
    for item in range(len(file_list)):
        file_list_vlojenie = os.listdir(f"{directory_path}/{file_list[item]}")
        for file in file_list_vlojenie:
            try:
                inside_file = pd.read_excel(f"{directory_path}/{file_list[item]}/{file}", sheet_name=None)
                for sheet_name, df_in in inside_file.items():
                    if sheet_name == "Лист1":
                        pass
                    else:
                        names = df_in.columns
                        second_data = df_in.iloc[1]
                        len_of_actions = len(df_in)-2
                        itog = [len(df_in)-1, len(df_in)]

                        for len_act_number in range(4, len_of_actions):
                            third_data = df_in.iloc[len_act_number]
                            if str(third_data[2]) == 'nan':
                                pass
                            else:
                                try:
                                    df.loc[counter, 'Участок']                = file_list[item]
                                    if str(names[21]) == 'Unnamed: 21':
                                        df.loc[counter, 'Дата запуска']           = ' '
                                    else:
                                        df.loc[counter, 'Дата запуска']           = names[21]
                                    df.loc[counter, 'Номер КД']               = names[16]
                                    df.loc[counter, 'Статья расхода']         = names[20]
                                    df.loc[counter, 'Имя файла']              = file
                                    df.loc[counter, 'Наименование детали']    = second_data[0]
                                    df.loc[counter, 'Кол-во']                 = second_data[1]

                                    df.loc[counter, 'Наименование операции']  = third_data[2]
                                    df.loc[counter, 'Краткий текст']          = third_data[12]
                                    df.loc[counter, 'Время подготовительное'] = third_data[16]
                                    df.loc[counter, 'Время на 1шт.']          = third_data[17]
                                    #==========================================================
                                    try:
                                        time_all = (int(third_data[16]) + int(third_data[17])) *int(second_data[1]) 
                                        df.loc[counter, 'Время всего']        = time_all
                                    except Exception as err:
                                        error_log.append({"err":str(err)+' passing this value, not critical', "file": file})
                                    #==========================================================
                                    df.loc[counter, 'Фамилия исполнителя']    = third_data[18]
                                    df.loc[counter, 'Дата изготовления']      = third_data[20]
                                    df.loc[counter, 'Статус']                 = third_data[21]

                                except Exception as err:
                                    error_log.append({"err":str(err), "file": file})
                                counter = counter + 1
            except Exception as err:
                error_log.append({"err":str(err), "file": file})
    df.to_excel(output_file, index=False)
    return True, error_log
