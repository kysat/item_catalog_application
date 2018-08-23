from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, City, Architecture
import json

engine = create_engine('sqlite:///city.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name='Kate', email='kate@fake.com')
session.add(User1)
session.commit()

city_json = json.loads("""
{
    "Cities": [
        {
            "name": "Paris",
            "description": "Center of France"
        },
        {
            "name": "Tokyo",
            "description": "Center of Japan"
        },
        {
            "name": "Barcelona",
            "description": "Center of Spain"
        },
        {
            "name": "London",
            "description": "Center of UK"
        },
        {
            "name": "Berlin",
            "description": "Center of Germany"
        },
        {
            "name": "New York",
            "description": "Center of USA"
        }
    ],
    "Architectures": {
        "Paris": [
            {
                "name": "Villa Savoye",
                "description": "Architect: Le Corbusier",
                "picture": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/VillaSavoye.jpg/480px-VillaSavoye.jpg"
            },
            {
                "name": "Centre Pompidou",
                "description": "Architect: Renzo Piano",
                "picture": "https://upload.wikimedia.org/wikipedia/en/thumb/9/95/Pompidou_center.jpg/480px-Pompidou_center.jpg"
            },
            {
                "name": "Unite d'habitation",
                "description": "Architect: Le Corbusier",
                "picture": "http://www.fondationlecorbusier.fr/CorbuCache/900x720_2049_791.jpg?r=0"
            }
        ],
        "Tokyo": [
            {
                "name": "Omotesando Hills",
                "description": "Architect: Tadao Ando",
                "picture": "https://eliinbar.files.wordpress.com/2011/02/001_b.jpg"
            },
            {
                "name": "Reversible Destiny Lofts MITAKA",
                "description": "Architect: Shusaku Arakawa",
                "picture": "https://s3.amazonaws.com/files.collageplatform.com.prod/image_cache/1010x580_fit/57e1a75587aa2c703cbd6ecf/6630861cad0ef3f5be2e7f63349eb032.jpeg"
            },
            {
                "name": "Nakagin Capsule Tower",
                "description": "Architect: Kisho Kurokawa",
                "picture": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Nakagin.jpg/640px-Nakagin.jpg"
            }
        ]
    }
}
""")

# Add Cities in city_json to database
for e in city_json['Cities']:
    city_input = City(
        name=str(e['name']),
        description=str(e['description'])
    )
    session.add(city_input)
    session.commit()

# Add Architectures in city_json to database
for c in city_json['Architectures'].keys():
    city = session.query(City).filter_by(name=c).one()
    for e in city_json['Architectures'][c]:
        architecture_input = Architecture(
            name=str(e['name']),
            description=str(e['description']),
            picture=str(e['picture']),
            city=city
        )
        session.add(architecture_input)
        session.commit()
