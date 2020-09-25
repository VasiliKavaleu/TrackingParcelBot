from load_page import Load, Parser

url = ''

html = Load().load_page_on_local(url)
print(Parser().get_info_from_posylka(html))
