import requests as rq
import zipfile as zpf
import shutil as sh
import os
import pandas as pd
import json

urls = {
    2016: 'https://drive.google.com/uc?export=download&id=0B0DL28AqnGsrV0VldnVIT1hyb0E',
    2017: 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM',
    2018: 'https://drive.google.com/uc?export=download&id=1_9On2-nsBQIw3JiY43sWbrF8EjrqrR4U',
    2019: 'https://drive.google.com/uc?export=download&id=1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV',
}

filenames = {
    2016: '2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Responses.csv',
    2017: 'survey_results_public.csv',
    2018: 'survey_results_public.csv',
    2019: 'survey_results_public.csv',
}

question_name = {
    2016: 'tech_do',
    2017: 'HaveWorkedLanguage',
    2018: 'LanguageWorkedWith',
    2019: 'LanguageWorkedWith',
}

def survey_csvname(year):
    return 'survey{}.csv'.format(year)

def download_survey(year):
    request = rq.get(urls[year])

    with open('survey.zip', 'wb') as file:
        file.write(request.content)

    with zpf.ZipFile('survey.zip', 'r') as zipfile:
        zipfile.extractall('data')

    sh.move('data/' + filenames[year], survey_csvname(year))
    sh.rmtree('data', ignore_errors=True)
    os.remove('survey.zip')
