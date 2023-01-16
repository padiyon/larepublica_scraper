import requests
import lxml.html as html
import os
import datetime

#Url de la pagina
HOME_URL = 'https://www.larepublica.co'

#url del articulo
XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'

#Extraer de cada articulo
XPATH_TITTLE='//div/text-fill/span/text()'
XPATH_SUMMARY='//*[@id="proportional-anchor-1"]/div/div/p/text()'
XPATH_BODY='//div/div[4]/p/text()'



def get_title(link):
    #separamos por "/" y nos quedamos con el ultimo que elemento 
    url = link.split('/')[-1]
    #separamos por "-" y eliminamos el ultimo elemento
    title_list=url.split('-')[:-1]
    #Unimos lo anterior
    title = " ".join(title_list)

    return(title)



def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code==200:
            notice = response.content.decode('utf-8') #Guarda el contenido
            parsed = html.fromstring(notice)
            
            try:
                tittle = get_title(link) #obtiene el titulo
                
                summary = parsed.xpath(XPATH_SUMMARY)[0] #get te summary
                body = parsed.xpath(XPATH_BODY) #get the body


            except IndexError as ie:
                print(ie)
                return

            try:

                with open(f'{today}/{tittle}.txt', 'w', encoding='utf-8') as f:
                    f.write(tittle)
                    f.write('\n\n')
                    f.write(summary)
                    f.write('\n\n')
                    for p in body:
                        if p.endswith('.'):
                             f.write(p)
                             f.write('\n')
                        else: 
                             f.write(p)

            except:
                print('no se pudo escribir')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

#Extraer links
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200: #si la conexion es correcta
            home = response.content.decode('utf-8') #guarda en formato leible
            parsed = html.fromstring(home) #parsea
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notice)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notice:
                parse_notice(link,today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()