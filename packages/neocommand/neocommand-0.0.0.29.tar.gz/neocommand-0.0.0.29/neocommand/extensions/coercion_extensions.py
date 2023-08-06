"""
Creates and registers additional string coercers.
"""
from typing import Optional

import stringcoercion
from neocommand.database.endpoints import IIoBase
from stringcoercion import Coercer, CoercionInfo



class __EndpointCoercion( Coercer ):
    def coerce( self, info: CoercionInfo ) -> Optional[object]:
        from neocommand.data.core import CORE
        return CORE.endpoint_manager.find_endpoint( info.source )
    
    
    def can_handle( self, info: CoercionInfo ):
        return info.annotation.is_directly_below( IIoBase )


# Register coercers
stringcoercion.get_default_coercer().register( __EndpointCoercion() )
