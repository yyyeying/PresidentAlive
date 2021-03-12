import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt


def get_html_text(url):
    proxy = {'https': '127.0.0.1:10809'}
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'}
    print('HTTP GET: {}'.format(url))
    try:
        response = requests.get(url, headers=user_agent, proxies=proxy)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        print('访问成功')
        return response.text
    except:
        print('Retry...')
        get_html_text(url)


if __name__ == '__main__':
    president_list_page = 'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States'
    president_list_response = get_html_text(president_list_page)
    # print(president_list_response)
    president_list_soup = BeautifulSoup(president_list_response, 'html5lib')
    president_list_soup = president_list_soup.body
    president_list_soup = president_list_soup.find('div', id='content', class_='mw-body')
    president_list_soup = president_list_soup.find('div', id='bodyContent', class_='mw-body-content')
    president_list_soup = president_list_soup.find('div', id='mw-content-text')
    president_list_soup = president_list_soup.find('div', class_='mw-parser-output')
    president_list_soup = president_list_soup.find('table', class_='wikitable').tbody
    president_list_soup = president_list_soup.find_all('tr')
    president_link_list = []
    for soup in president_list_soup[1:]:
        soup = soup.find_all('td')
        if len(soup) >= 6:
            soup = soup[2].b.a['href']
            president_link_list.append(soup)
    print(president_link_list)
    print(len(president_link_list))
    time_list = []
    for link in president_link_list[:-1]:
        president_response = get_html_text('https://en.wikipedia.org' + link)
        president_soup = BeautifulSoup(president_response, 'html5lib')
        president_soup = president_soup.body
        president_soup = president_soup.find('table', class_='infobox vcard').tbody
        start_soup = president_soup.find('a', string=re.compile('President')).parent.parent.next_sibling.text
        start_soup = re.findall(re.compile('\d{4}'), start_soup)[1]
        start = int(start_soup)
        end_soup = president_soup.find('th', string=re.compile('Died'))
        if end_soup:
            end_soup = end_soup.next_sibling.text
            end_soup = re.findall(re.compile('\d{4}'), end_soup)[0]
            end = int(end_soup)
        else:
            end = 2020
        time_dict = {'start': start, 'end': end}
        time_list.append(time_dict)
        print(time_dict)
    final_dict = {}
    for i in range(1797, 2021):
        final_dict.update({i: 0})
    for duration in time_list:
        if duration['start'] != duration['end']:
            for i in range(duration['start'], duration['end'] + 1):
                final_dict[i] += 1
    print(final_dict)
    keys = []
    values = []
    for key, value in final_dict.items():
        keys.append(key)
        values.append(value)
    plt.plot(keys, values)
    plt.title('amount of alive former president in USA')
    plt.ylabel('amount of alive former president')
    plt.xlabel('year')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.savefig('20200312.png')
