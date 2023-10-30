print('IMPORTING pigeon')
import pigeon
print('PF DIR: ' + str(dir(pigeon)))


print('IMPORTING pigeon SETTINGS')
from pigeon.conf.settings import Settings
print('CREATING NEW SETTINGS')
settings = Settings(
    '',
    81,
    {},
    {},
    static=('/static/', '/home/lstuma/programming/projects/protifre_example_static/')
)


print('IMPORTING pigeon SERVER')
import pigeon.core.server as server
print('STARTING SERVER')
server.start(settings)