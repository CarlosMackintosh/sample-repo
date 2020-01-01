import requests as rq
import zipfile as zpf
import shutil
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

    shutil.move('data/' + filenames[year], survey_csvname(year))
    shutil.rmtree('data', ignore_errors=True)
    os.remove('survey.zip')

def languages_breakdown(year):

    file_exists = os.path.exists(survey_csvname(year))
    if not file_exists:
        download_survey(year)

    print(f"Processing {year}")
    data = pd.read_csv(survey_csvname(year), encoding='latin1')
    # print(data[1:3]['HaveWorkedLanguage'])

    languages = data[question_name[year]].str.split(';', expand=True)
    languages = languages.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    summary = languages.apply(pd.Series.value_counts)
    summary = pd.DataFrame({'count': summary.sum(axis=1)})
    # summary.to_csv(r'summaries.csv')

    total = data[data[question_name[year]].notnull()].shape[0]
    summary['percent'] = summary['count']/total*100
    
    return summary

if __name__ == "__main__":
    
    totals = {}
    for year in urls.keys():
        totals = languages_breakdown(year).to_dict()
    
    with open('data.json', 'w') as fo:
        fo.write(json.dumps(totals, indent=4, separators=([',','; '])))
