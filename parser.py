import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


class ParsedHabr:
    def __init__(self, link, configurations):
        self.links = link
        self.configurations = configurations
        self.data = {'date': [],
                     'company_name': [],
                     'specialization': [],
                     'vacancy': [],
                     'meta_information': [],
                     'level': [],
                     'required_skills': [],
                     'link_to_vacancy': []
                     }

        self.levels = ['Младший (Junior)',
                       'Средний (Middle)',
                       'Старший (Senior)',
                       'Ведущий (Lead)']

    def parse_vacancies_page(self, soup):
        """
        Parsing vacancies from the link
        """
        all_section = soup.find_all("div", class_="vacancy-card")
        for element in all_section:
            date = element.find('div', class_="vacancy-card__date").get_text()  # добавить дату с годом прям
            self.data['date'].append(date)

            company_name = element.find('div', class_="vacancy-card__company-title").get_text()
            self.data['company_name'].append(company_name)

            vacancy = element.find('div', class_="vacancy-card__title").find('a').get_text()
            self.data['vacancy'].append(vacancy)

            meta = self.get_meta(element)
            self.data['meta_information'].append(meta)

            specialization, level, skills = self.get_skills(element)
            self.data['specialization'].append(specialization)
            self.data['level'].append(level)
            self.data['required_skills'].append(skills)
            self.data['link_to_vacancy'].append(self.get_vacancy_link(element))

    @staticmethod
    def get_meta(element):
        """
        Get meta information,
        such as city, remote possibility etc
        """
        meta_info = element.find('div', class_="vacancy-card__meta").find_all('span')
        mets = []

        for el in meta_info:
            meta = el.get_text()
            if meta != ' • ':
                mets.append(meta)

        return ', '.join(mets)

    def get_skills(self, element):
        """
        Get specialization, level and required_skills
        """
        skills_list = element.find('div', class_="vacancy-card__skills").find_all('span')
        skill = []
        for el in skills_list:
            one_skill = el.get_text()
            if one_skill != ' • ':
                skill.append(one_skill)

        specialization = skill.pop(0)

        if skill[0] in self.levels:
            level = skill.pop(0)
        else:
            level = np.NaN

        return specialization, level, ', '.join(skill)

    @staticmethod
    def get_vacancy_link(element):
        """
        Get full link to vacancy
        """
        to_vacancies = 'https://career.habr.com'
        link_vac = element.find('div', class_="vacancy-card__title").find('a').get('href')

        return ''.join([to_vacancies, link_vac])

    def parse_pages(self):
        """
        Get soup from all pages given
        """
        for link in self.links:
            response = requests.get(link,
                                    self.configurations.get('headers'),
                                    timeout=self.configurations.get('timeout'),
                                    verify=self.configurations.get('should_verify_certificate'))
            soup = BeautifulSoup(response.text, 'lxml')
            self.parse_vacancies_page(soup)

    def get_dataframe(self):
        """
        Getting dataframe with all data
        """
        self.parse_pages()
        result_data = pd.DataFrame(self.data)
        return result_data