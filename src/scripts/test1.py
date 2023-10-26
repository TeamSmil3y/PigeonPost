print('IMPORTING PROTOFIRE')
import protofire
print('PF DIR: ' + str(dir(protofire)))


print('IMPORTING PROTOFIRE SETTINGS')
from protofire.utils.settings import Settings
print('CREATING NEW SETTINGS')
settings = Settings(
    '',
    81,
    {},
    {},
)


print('IMPORTING PROTOFIRE SERVER')
import protofire.core.server as server
print('STARTING SERVER')
server.run(settings)