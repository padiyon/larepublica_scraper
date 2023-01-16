import requests
import lxml.html as html
# Lo usaremso para crear una carpeta
import os 
# Lo usaremos para manipular fechas.
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
            # Traigo el docuemnto html de la noticia.
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            #Quiero traer el título, el cuerpo y el resumen, hago una validación
            # try -except, estoy haciendolo para los índices de la lista.
            # Pueden haber noticias con nodos faltantes por lo que arrojará un error
            try:
                #Traemos el primer elemento de la lista.
                tittle = get_title(link)

                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)


            except IndexError as ie:
                print(ie)
                return

            try:
                # Guardamos en  un archivo

                # with es un manejador contextual. Si algo sucede y el script se cierra, mantiene las cosas
                # de manera segura y así no se corrompe el archivo.


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


# Creamos las funcioens para ejecutar el script.

def parse_home():
    # Creamos un bloque try para manejar los errores. Y manejar los Status Code.
    try:
        response = requests.get(HOME_URL)
         # Aqui va la lógica para traer los links.
        if response.status_code == 200:
            # .content trae  el HTML que necesita ser traducido con un decode para que python lo entienda
            # en terminos de caracteres, me devuelve un string que no es más que el HTML crudo.
            home = response.content.decode('utf-8')
            # home = response.text

            # En esta línea uso el parser html para transformar el contentido
            # html a un archivo que sea de utilidad para las expresiones xpath
            parsed = html.fromstring(home)

            # En esta línea estoy usando el archivo parseado con la función xpath y le paso por parámetro mi constante
            # la cual almacena la expresión Xpath.

            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # La línea de código me arroja un array vacío. Pero en google si lo enseña.

            # Traigo una fecha con la función fecha. Y Today, la fecha del dái de hoy. La variable today
            # se almacena un objeto de tipo fecha, pero nos interesa más tener una cadena de caracteres que contenga la fecha
            # en determinado formato que será guardado en la carpeta y con la función strftime logramos esto


            today = datetime.date.today().strftime('%d-%m-%Y')
            # Este condicional sirve para decirle que si no existe una carpeta con la fehca del día de hoy
            # me cree una carpeta.
            if not os.path.isdir(today):
                os.mkdir(today)

            # Creo la función para recorrer la lista de links y ejecuto en cada ciclo la función parse_notice()
            
            for link in links_to_notice:
                parse_notice(link,today)

        else:
            #Elevamos el error para ser capturado en el try-except, too lo que sea un error.
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()