from data.producers import Producer
from data.kits import Kit
from data import db_session

def push_data():
    # prod = Producer()
    # prod.name = "Овен"
    # prod.about = """Фирма «Овен» начала работу в 2000 году, продавая различные товары для рукоделия. С 2002 года основной ее деятельностью является производство и реализация наборов для вышивания «Стильные вещи для дома»."""
    # prod.logo = "logo_oven.png"
    # session = db_session.create_session()
    # session.add(prod)
    # session.commit()
#     kit = Kit(name="Неожиданная встреча", about="""Размер: (33×26)
# Количество нитей: 2
# Количество цветов мулине: 30
# Канва: 18
# Мулине: ПНК им. Кирова
# Схема: Цветная,символьная
# В набор входит: Канва,мулине,схема,игла""", pic="oven_512.png",
#                 prod_id=2)
#     session = db_session.create_session()
#     session.add(kit)
#     session.commit()
    session = db_session.create_session()
    kit = session.query(Kit).filter(Kit.id == 1).first()
    kit.pic = "static/img/oven_512.png"
    session.commit()