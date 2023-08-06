def __setup():
    #
    # INTERMAKE Setup
    #
    from mhelper import reflection_helper
    from intermake import MENV
    from neocommand.data import constants
    from neocommand.data.core import CORE
    
    if not MENV.is_locked():
        MENV.name = "NeoCommand"
        MENV.constants.update( (k, str( v )) for k, v in reflection_helper.public_dict( constants.__dict__ ).items() )
        MENV.root = CORE


# Setup MCMD *before* exporting CORE
__setup()

# Export stuff
from neocommand.data import constants
from neocommand.data.core import CORE
from neocommand.data.settings import Settings, ENeo4jDriver
from neocommand.database.endpoints import IEndpoint, CountingEndpointWrapper
from neocommand.helpers.neo_csv_helper import NEO_TYPE_COLLECTION
from neocommand.extensions.plugins.basic import database, endpoints
from neocommand.extensions.plugins.exportation import exportation, neo_csv_exports, neo_csv_exchange, neo_csv_tools
import neocommand.extensions.coercion_extensions
import neocommand.extensions.editorium_extensions