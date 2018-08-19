from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, City, Architecture

engine = create_engine('sqlite:///city.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name='Kate', email='kate@fake.com')
session.add(User1)
session.commit()

City1 = City(name='Paris',
             description='Center of France')

session.add(City1)
session.commit()

City2 = City(name='Tokyo',
             description='Center of Japan')

session.add(City2)
session.commit()

City3 = City(name='Barcelona',
             description='Center of Spain')

session.add(City3)
session.commit()

City4 = City(name='London',
             description='Center of UK')
session.add(City4)
session.commit()

City5 = City(name='Berlin',
             description='Center of Germany')

session.add(City5)
session.commit()

City6 = City(name='New York',
             description='Center of USA')
session.add(City6)
session.commit()

architecture1 = Architecture(name='Villa Savoye',
                            description='Architect: Le Corbusier',
                            picture='https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/VillaSavoye.jpg/480px-VillaSavoye.jpg',
                            city=City1
                            )

session.add(architecture1)
session.commit()

architecture2 = Architecture(name='Centre Pompidou',
                             description='Architect: Renzo Piano',
                             picture='https://upload.wikimedia.org/wikipedia/en/thumb/9/95/Pompidou_center.jpg/480px-Pompidou_center.jpg',
                             city=City1
                             )
session.add(architecture2)
session.commit()

architecture3 = Architecture(name="Unite d'habitation",
                             description='Architect: Le Corbusier',
                             picture='http://www.fondationlecorbusier.fr/CorbuCache/900x720_2049_791.jpg?r=0',
                             city=City1)
session.add(architecture3)
session.commit()

architecture4 = Architecture(name='Omotesando Hills',
                             description='Architect: Tadao Ando',
                             picture='https://eliinbar.files.wordpress.com/2011/02/001_b.jpg',
                             city=City2)
session.add(architecture4)
session.commit()

architecture5 = Architecture(name='Reversible Destiny Lofts MITAKA',
                             description='Architect: Shusaku Arakawa',
                             picture='https://s3.amazonaws.com/files.collageplatform.com.prod/image_cache/1010x580_fit/57e1a75587aa2c703cbd6ecf/6630861cad0ef3f5be2e7f63349eb032.jpeg',
                             city=City2)
session.add(architecture5)
session.commit()

architecture6 = Architecture(name='Nakagin Capsule Tower',
                             description='Architect: Kisho Kurokawa',
                             picture='https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Nakagin.jpg/640px-Nakagin.jpg',
                             city=City2)
session.add(architecture6)
session.commit()
