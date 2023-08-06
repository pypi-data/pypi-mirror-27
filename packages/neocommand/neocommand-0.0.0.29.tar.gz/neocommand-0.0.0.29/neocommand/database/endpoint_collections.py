"""
Classes for managing "parcels" - folders that contain a formatted set of entries to be added to the database
"""
from intermake.engine.environment import MENV, MCMD


__author__ = "Martin Rusilowicz"

from typing import List, cast, Optional, Iterator, Tuple

from intermake import EColour, IVisualisable, UiInfo, constants as mconstants
from neocommand.database.endpoints import ECHOING_ENDPOINT, NULL_ENDPOINT, IIoBase, IMasterOrigin
from neocommand.gui_qt import resources as Res
from mhelper import NotFoundError


class EndpointManager( IVisualisable ):
    """
    Manages pipeline folders
    """
    
    
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        See methods of same name for parameter details
        """
        self.__user_endpoints = cast( List[IIoBase], MENV.local_data.store.get( "user_endpoints", [] ) )
        self.__other_endpoints = [NULL_ENDPOINT, ECHOING_ENDPOINT]
    
    
    def find_endpoint( self, name: str ) -> Optional[IIoBase]:
        for endpoint in self:
            if endpoint.endpoint_name == name:
                return endpoint
        
        MCMD.warning( "Cannot find the endpoint named «{}». Did you specify a valid name? Perhaps it has been deleted?".format( name ) )
        return None
    
    
    @property
    def user_endpoints( self ) -> Tuple[IIoBase, ...]:
        return tuple(self.__user_endpoints)
    
    
    def remove_user_endpoint( self, endpoint: IIoBase ):
        """
        Removes the specified endpoint from the user endpoint collection.
        """
        if endpoint not in self.__user_endpoints:
            raise NotFoundError( "«{}» is not a user endpoint.".format( endpoint.endpoint_name ) )
            
        try:
            endpoint.endpoint_deleted()
        except Exception as ex:
            raise ValueError( "«{}» has not been removed due to a previous error.".format( endpoint.endpoint_name ) ) from ex
        
        self.__user_endpoints.remove( endpoint )
        self.__save_endpoints()
    
    
    def __save_endpoints( self ) -> None:
        MENV.local_data.store["user_endpoints"] = self.__user_endpoints
    
    
    def add_user_endpoint( self, endpoint: IIoBase ) -> None:
        for x in self:
            if x.visualisable_info().name == endpoint.endpoint_name:
                raise ValueError( "The name «{}» is already taken.".format( x.endpoint_name ) )
        
        self.__user_endpoints.append( endpoint )
        self.__save_endpoints()
    
    
    def __str__( self ) -> str:
        return "Endpoints"
    
    
    def visualisable_info( self ) -> UiInfo:
        x = "{} user and {} inbuilt endpoints".format( len( self.__user_endpoints ), len( self.__other_endpoints ) )
        
        return UiInfo( name = self,
                       comment = "",
                       type_name = mconstants.VIRTUAL_FOLDER,
                       value = x,
                       colour = EColour.YELLOW,
                       icon = Res.folder,
                       extra_named = self.__iter__ )
    
    
    def __iter__( self ) -> Iterator[IIoBase]:
        yield from self.__other_endpoints
        yield from self.__user_endpoints
    
    
    def get_database_endpoint( self, tolerant = False ) -> Optional[IMasterOrigin]:
        database = None
        
        for ep in self:
            if isinstance( ep, IMasterOrigin ):
                if database is not None:
                    message = "Problem obtaining default database: I found multiple «DbEndpoint»s that could act as a reasonable default. Perhaps you meant to specify the a database explicitly?"
                    
                    if tolerant:
                        MCMD.warning( message )
                        return None
                    
                    raise ValueError( message )
                
                database = ep
        
        if database is None:
            message = "Problem obtaining default database: I could not find any «DbEndpoint» to act as a reasonable default. Perhaps you meant to call «new_connection» first?"
            
            if tolerant:
                MCMD.warning( message )
                return None
            raise ValueError( message )
        
        return database
