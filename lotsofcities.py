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
             description='City of full of Arts')

session.add(City1)
session.commit()

City2 = City(name='Chandigarh',
             description='City of fully designed by master')

session.add(City2)
session.commit()

City3 = City(name='Tokyo',
             description='Fast City')

session.add(City3)
session.commit()

City4 = City(name='Barcelona',
             description='Full of Exitement')

session.add(City4)
session.commit()

City5 = City(name='London',
             description='Sophisticated City')
session.add(City5)
session.commit()

City6 = City(name='Berlin',
             description='Diversed City')

session.add(City6)
session.commit()

City7 = City(name='New York',
             description='Center of the World')
session.add(City7)
session.commit()

# architect1 = Architect(name='Le Corbusier')
# session.add(architect1)
# session.commit()

# architect2 = Architect(name='Renzo Piano')
# session.add(architect2)
# session.commit()

architecture1 = Architecture(name='villa savoye',
                            description='https://www.wikiwand.com/en/Villa_Savoye',
                            # architect=architect1,
                            picture='https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/VillaSavoye.jpg/480px-VillaSavoye.jpg',
                            city=City1
                            )

session.add(architecture1)
session.commit()

architecture2 = Architecture(name='Centre Pompidou',
                             description='https://en.wikipedia.org/wiki/Centre_Georges_Pompidou',
                            #  architect=architect2,
                             picture='https://upload.wikimedia.org/wikipedia/en/thumb/9/95/Pompidou_center.jpg/480px-Pompidou_center.jpg',
                             city=City1
                             )
session.add(architecture2)
session.commit()



'''
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    architect_id = Column(Integer, ForeignKey('architect.id')
    architect = relationship(Architect)
'''

'''
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
'''