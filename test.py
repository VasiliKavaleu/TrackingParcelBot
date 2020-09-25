from load_page import Load, Parser


#url = 'https://posylka.net/parcel/SB001559895LV'

url = 'https://posylka.net/parcel/LA993502537CN'

html = Load().load_page_on_local(url)
print(Parser().get_info_from_posylka(html))
