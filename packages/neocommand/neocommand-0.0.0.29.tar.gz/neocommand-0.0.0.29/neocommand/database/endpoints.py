"""
Endpoints - where entities are sent and received from.
    
Plugins can take these as arguments allowing them to abstract themselves from the means of importing or exporting data.
"""
import warnings
from collections import OrderedDict
from os import path
from typing import Dict, Iterator, List, Optional, Tuple, Union, Type, TypeVar, Sequence
from uuid import uuid4

import keyring as keyring_
from keyring.errors import PasswordDeleteError

from intermake import EColour, IVisualisable, MCMD, MENV, UiInfo
from mhelper import EFileMode, Filename, ManagedWith, NotSupportedError, SwitchError, abstract, array_helper, file_helper, io_helper, override, sealed, virtual
from neocommand.data import constants
from neocommand.data.settings import ENeo4jDriver
from neocommand.database.entities import Edge, IEntity, Node, iterate_all
from neocommand.gui_qt import resources, resources as Res
from neocommand.helpers.neo_csv_helper import NeoCsvFilename, NeoCsvMultiWriter, NeoCsvReader
from neocommand.helpers.special_types import TEdgeLabel, TNodeLabel, TNodeProperty, TNodeUid


T = TypeVar( "T" )

ENDPOINT_COLOUR = EColour.RED
FILE_ENDPOINT_COLOUR = EColour.GREEN
ENDPOINT_ICON = Res.parcel
FILE_ENDPOINT_ICON = Res.parcel

_DbManager = "neocommand.database.database_manager.DbManager"
_EntityResolverUsage_ = "EntityResolverUsage"


class AddFailedError( Exception ):
    """
    Endpoints raise this if an add fails for any reason.
    """
    pass


class InvalidEntityError( Exception ):
    """
    An error used when trying to retrieve an entity from the database when that entity does not exist in the database.
    """
    pass


# noinspection PyAbstractClass
class IIoBase( IVisualisable ):
    """
    Base class for all `IOrigin` and `IEndpoint`
    """
    
    
    @sealed
    def __not_supported( self ) -> NotSupportedError:
        """
        Internal method that returns a `NotSupportedError`.
        """
        return NotSupportedError( "Sorry, but this «{}» endpoint does not support the requested feature. Please use a different endpoint for this purpose.".format( self ) )
    
    
    @property
    def endpoint_name( self ) -> str:
        """
        Obtains the user-provided name for the endpoint.
        """
        return self._ENDPOINT__get_name()
    
    
    @endpoint_name.setter
    def endpoint_name( self, value: str ):
        """
        SETTER 
        """
        self._ENDPOINT__set_name( value )
    
    
    @virtual
    def endpoint_deleted( self ) -> None:
        """
        Allows handling if the endpoint is deleted by the user.
        
        :except Exception: The endpoint may raise any exception, this prevents deletion.
        """
        pass
    
    
    @abstract
    def _ENDPOINT__get_name( self ) -> str:
        """
        The derived class should obtain the user-provided name for the endpoint.
        """
        raise NotImplementedError( "abstract" )
    
    
    @abstract
    def _ENDPOINT__set_name( self, value: str ):
        """
        The derived class should set the user-provided name for the endpoint to `value`.
        """
        raise NotImplementedError( "abstract" )


# noinspection PyAbstractClass
class IOrigin( IIoBase ):
    """
    Endpoints that can read data. 
    """
    
    
    def origin_get_all( self ) -> Iterator[IEntity]:
        """
        Iterates over all nodes and edges.
        
        :except InvalidEntityError: Failed to locate entity
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise self.__not_supported()
    
    
    def origin_get_all_nodes_property( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        """
        Gets a UID-to-property dictionary for the specified node label.
         
        :param label:      Label of node 
        :param property:   Property to get 
        :return:           Iterator over UIDs and properties: Tuple[UID, property-value]
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise self.__not_supported()


# noinspection PyAbstractClass
class IMasterOrigin( IOrigin ):
    """
    Special case of `IOrigin` that allows individual lookups.
    """
    
    
    def origin_get_edge_by_iid( self, iid: int ) -> Edge:
        """
        Finds an edge by its internal identifier.
        
        :param iid:     IID 
        :return: The edge
        :except InvalidEntityError: Failed to locate entity
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise self.__not_supported()
    
    
    def origin_get_edge_by_node_uids( self, label: str, start_label: str, end_label: str, start_uid: str, end_uid: str ) -> Edge:
        """
        Finds an edge by the UIDs of its nodes.
        :param label:           Label, of edge 
        :param start_label:     Label, of start node 
        :param end_label:       Label, of end node
        :param start_uid:       Uid, of start node 
        :param end_uid:         Uid, of end node
        :return: The edge 
        :except InvalidEntityError: Failed to locate entity 
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise self.__not_supported()
    
    
    def origin_get_edge_by_node_iids( self, start_iid: int, end_iid: int ) -> Edge:
        """
        Finds an edge by the IIDs of its nodes.
        :param start_iid:   IID, of start node 
        :param end_iid:     IID, of end node 
        :return: The edge
        :except InvalidEntityError: Failed to locate entity 
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise self.__not_supported()
    
    
    def origin_get_node_property_by_uid( self, label: str, uid: str, property: str ) -> Optional[object]:
        """
        Finds a single property of a node.
        :param label:       Label of node 
        :param uid:         UID of node 
        :param property:    Property to retrieve 
        :return:            The property, or `None` if the node was found but it doesn't have that property. 
        :except InvalidEntityError: Failed to locate entity
        :except NotSupportedError:  The endpoint does not support this feature
        """
        raise self.__not_supported()
    
    
    def origin_get_node_property_by_iid( self, iid: int, property: str ) -> Optional[object]:
        """
        Finds a single property of a node.
        :param iid:         IID of node
        :param property:    Property to retrieve 
        :return:            The property, or `None` if the node was found but it doesn't have that property. 
        :except InvalidEntityError: Failed to locate entity
        :except NotSupportedError:  The endpoint does not support this feature 
        """
        raise self.__not_supported()
    
    
    def origin_get_node_by_uid( self, label: str, uid: str ) -> Node:
        """
        Gets a specific node
        :param label:      Label of node
        :param uid:        UID of node
        :return:            The node
        :except InvalidEntityError: Failed to locate entity
        :except NotSupportedError:  The endpoint does not support this feature 
        """
        raise self.__not_supported()
    
    
    def origin_get_node_by_iid( self, iid: int ) -> Node:
        """
        Gets a specific node
        :param iid:        IID
        :return:            The node
        :except InvalidEntityError: Failed to locate entity
        :except NotSupportedError:  The endpoint does not support this feature 
        """
        raise self.__not_supported()


# noinspection PyAbstractClass
class IEndpoint( IIoBase ):
    """
    Endpoints that can write data. 
    """
    
    
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        """
        self.__dirty = False
    
    
    def __str__( self ) -> str:
        """
        Returns a name that is better than the Python default.
        This function does not preclude a more detailed result from a derived class.
        """
        return "{}::{}".format( type( self ).__name__, self.endpoint_name )
    
    
    @sealed
    def endpoint_create_node( self, *, label: str, uid: str, properties: Dict[str, object] ):
        """
        Adds a node to the endpoint.

        If a node with the same label and UID does not already exists it should be created.
        The endpoint should update the specified `properties` on the node. object other properties should remain intact.
        
        :param label:       Node label 
        :param uid:         Node UID 
        :param properties:  Node properties to be updated.
                                ¡WARNING!
                                The caller should NOT assume that `properties` is not modified.
                                The implementing class is free to modify this dictionary (thus avoiding copies where unnecessary).
        :return:            The created node
        :except AddFailedError:     The add failed.
        :except NotSupportedError:  The endpoint does not support this feature
        """
        node = Node( label = label, uid = uid, properties = properties )
        self.endpoint_add_node( node )
        return node
    
    
    @sealed
    def endpoint_create_edge( self, *, label: str, start_label: str, start_uid: str, end_label: str, end_uid: str, properties: Dict[str, object] ):
        """
        Adds an edge to the endpoint.
        
        If an edge with the same label does not exist between the specified nodes, the edge should be created.
        The endpoint should update the specified `properties` on the edge. object other properties should remain intact.
        
        If the specified nodes do not exist, the behaviour is undefined (preferably an exception, though this cannot be guaranteed).
         
        :param label:           Edge type 
        :param start_label:     Starting node label 
        :param start_uid:       Starting node UID 
        :param end_label:       Ending node label 
        :param end_uid:         Ending node UID 
        :param properties:      Edge properties to be updated.
                                    ¡WARNING!
                                    The caller should NOT assume that `properties` is not modified.
                                    The implementing class is free to modify this dictionary (thus avoiding copies where unnecessary).
        :return: The created edge
        :except AddFailedError:     The add failed.
        :except NotSupportedError:  The endpoint does not support this feature
        """
        start = Node( label = start_label, uid = start_uid, properties = { } )
        end = Node( label = end_label, uid = end_uid, properties = { } )
        edge = Edge( label = label, start = start, end = end, data = properties )
        self.endpoint_add_edge( edge )
        return edge
    
    
    @sealed
    def endpoint_add_node( self, node: Node ):
        """
        See `endpoint_create_node`. 
        """
        self.__dirty = True
        self._ENDPOINT_add_node( node )
    
    
    @sealed
    def endpoint_add_edge( self, edge: Edge ):
        """
        See `endpoint_create_edge`.
        """
        self.__dirty = True
        self._ENDPOINT_add_edge( edge )
    
    
    @sealed
    def endpoint_create_folder( self, name: str ) -> "IEndpoint":
        """
        Adds a folder to the endpoint.
        
        Folders logically sort the results for the GUI, they may not have any actual effect if writing
        to a file, in which case the endpoint may just return it`self`.
        
        The default implementation of this function returns `self`, hence this function should never raise a `NotSupportedError`.
        
        :param name:                Folder name 
        :return:                    The new endpoint for this folder
        :except AddFailedError:     The add failed.
        """
        self.__dirty = True
        return self._ENDPOINT_create_folder( name )
    
    
    @sealed
    def endpoint_add_data( self, data: object ) -> None:
        """
        Adds arbitrary data to the endpoint.
        Note that not all endpoints support the addition of arbitrary data.
        
        If the endpoint does not support this operation it will ideally fail silently or issue a warning, allowing other operations to proceed,
        This does not mean that this function will not raise, cases such as malformed data may still raise the appropriate exception.
        
        :param data: Data to add.
        :return: 
        """
        self._ENDPOINT_add_data( data )
    
    
    @sealed
    def endpoint_add_entity( self, entity: IEntity ):
        """
        Adds a node or an edge to the endpoint.
        May not be used for arbitrary data.
        
        :param entity:  Node or edge to add.
        """
        if isinstance( entity, Edge ):
            self.endpoint_add_edge( entity )
        elif isinstance( entity, Node ):
            self.endpoint_add_node( entity )
        else:
            raise SwitchError( "entity", entity, instance = True )
    
    
    @abstract
    def _ENDPOINT_add_data( self, data: object ):
        """
        Abstracted implementation of `endpoint_add_data`.
        """
        raise NotImplementedError( "abstract" )
    
    
    @abstract
    def _ENDPOINT_add_node( self, node: Node ):
        """
        Abstracted implementation of `endpoint_add_node`.
        """
        raise NotImplementedError( "abstract" )
    
    
    @abstract
    def _ENDPOINT_add_edge( self, edge: Edge ):
        """
        Abstracted implementation of `endpoint_add_edge`.
        """
        raise NotImplementedError( "abstract" )
    
    
    @virtual
    def _ENDPOINT_create_folder( self, name: str ) -> "IEndpoint":
        """
        Abstracted implementation of `endpoint_create_folder`.
        """
        return self
    
    
    @sealed
    def endpoint_flush( self ) -> None:
        """
        Flushes the endpoint.
        
        The endpoint should be capable of handling excessive (redundant or unnecessary) flushes.
        This must be called if changes are made.
        If this is not called, any changes made may or may not be committed, or the output file may be incomplete, though the
        endpoint should ensure to preserve the integrity of primary data-sources (i.e. the database).
        
        Implementation notice:
        This function is required even if the endpoint does not perform any flushing action. The default implementation raises
        a `NotSupportedError`, since missing functionality would cause more problematic issues, such as sporadic output corruption.
        """
        if self.__dirty:
            self.__dirty = False
            self._ENDPOINT_flush()
    
    
    @abstract
    def _ENDPOINT_flush( self ) -> None:
        """
        Abstracted implementation of `endpoint_flush`.
        """
        raise NotImplementedError( "abstract" )


class NullEndpoint( IEndpoint ):
    """
    A write-only endpoint that doesn't write the data anywhere.
    """
    FIXED_NAME = "null"
    
    
    def _ENDPOINT__get_name( self ) -> str:
        return self.FIXED_NAME
    
    
    def _ENDPOINT__set_name( self, value: str ):
        raise ValueError( "Cannot change the name of a system endpoint." )
    
    
    def visualisable_info( self ) -> UiInfo:
        return UiInfo( name = "null",
                       comment = "IEndpoint that doesn't send anywhere.",
                       type_name = "NULL_EP",
                       value = "Maps I/O to null",
                       colour = ENDPOINT_COLOUR,
                       icon = ENDPOINT_ICON )
    
    
    def __str__( self ) -> str:
        return "NULL_EP"
    
    
    def _ENDPOINT_add_data( self, data: object ):
        pass  # by intent
    
    
    def _ENDPOINT_create_folder( self, name: str ) -> "IEndpoint":
        pass  # by intent
    
    
    def _ENDPOINT_add_edge( self, edge: Edge ):
        pass  # by intent
    
    
    def _ENDPOINT_add_node( self, node: Node ):
        pass  # by intent
    
    
    def _ENDPOINT_flush( self ) -> None:
        pass
    
    
    def __bool__( self ) -> bool:
        return False


NULL_ENDPOINT = NullEndpoint()


class EchoingEndpoint( IEndpoint, IVisualisable ):
    """
    An write-only endpoint that echos data to the terminal.
    """
    FIXED_NAME = "echo"
    
    
    def _ENDPOINT__get_name( self ) -> str:
        return self.FIXED_NAME
    
    
    def _ENDPOINT__set_name( self, value: str ):
        raise ValueError( "Cannot set the name of a system endpoint «{}».".format( self.endpoint_name ) )
    
    
    def _ENDPOINT_flush( self ) -> None:
        MCMD.print( "---ENDPOINT-FLUSH---" )
    
    
    def visualisable_info( self ) -> UiInfo:
        return UiInfo( name = "echo",
                       comment = "Echos output to std. out.",
                       type_name = "ECHO_EP",
                       value = "Maps I/O to echo",
                       colour = ENDPOINT_COLOUR,
                       icon = Res.export )
    
    
    def __str__( self ) -> str:
        return "ECHO_EP"
    
    
    def __init__( self, title = "echo" ) -> None:
        super().__init__()
        self.title = title
    
    
    def __print( self, message: str ):
        MCMD.print( "{}) {}".format( self.title, message ) )
    
    
    def __print_properties( self, properties: Dict[str, object] ):
        if not properties.items():
            return
        
        items = sorted( properties.items(), key = lambda x: str( x[0] ) )
        longest = max( len( str( item[0] ) ) for item in items )
        
        for k, v in items:
            MCMD.print( "{})            {} = {}".format( self.title, str( k ).ljust( longest ), v ) )
    
    
    def _ENDPOINT_create_folder( self, name: str ) -> "IEndpoint":
        self.__print( name + "/" )
        return EchoingEndpoint( self.title + "/" + name )
    
    
    def _ENDPOINT_add_data( self, data: object ):
        self.__print( "DATA {}".format( data ) )
    
    
    def _ENDPOINT_add_edge( self, edge: Edge ):
        self.__print( "EDGE ( {} «{}» )----[ {} ]---->( {} «{}» )".format( edge.start.label, edge.start.uid, edge.label, edge.end.label, edge.end.uid ) )
        self.__print_properties( edge.properties )
    
    
    def _ENDPOINT_add_node( self, node: Node ):
        self.__print( "NODE ( {} «{}» )".format( node.label, node.uid ) )
        self.__print_properties( node.properties )


ECHOING_ENDPOINT = EchoingEndpoint()


class __DbEndpointScriptsClass:
    def __init__( self ) -> None:
        from neocommand.extensions.plugin_classes.script import HScriptParam, HDbParam, Script
        
        self.PROPERTY_LOOKUP_UID = Script( cypher = """
                                                    MATCH (a:<LABEL> {uid: {uid}})
                                                    RETURN a.`<PROPERTY>`
                                                    """,
                                           timeout = constants.TIME_SHORT_TIMEOUT,
                                           arguments = { "label"   : HScriptParam[TNodeLabel],
                                                         "uid"     : HDbParam[TNodeUid],
                                                         "property": HScriptParam[TNodeProperty] } )
        
        self.PROPERTY_LOOKUP_IID = Script( cypher = """
                                            MATCH (a) WHERE ID(a) = {iid}
                                            RETURN a.`<PROPERTY>`
                                            """,
                                           arguments = { "iid"     : HDbParam[TNodeUid],
                                                         "property": HScriptParam[TNodeProperty] },
                                           timeout = constants.TIME_SHORT_TIMEOUT )
        
        self.NODE_LOOKUP_UID = Script( cypher = """
                                        MATCH (n:<LABEL> { uid:{uid} })
                                        RETURN n
                                     """,
                                       arguments = { "label": HScriptParam[TNodeLabel],
                                                     "uid"  : HDbParam[TNodeUid] }, )
        
        self.NODE_LOOKUP_IID = Script( cypher = """
                                        MATCH (n) WHERE ID(n) = {id}
                                        RETURN n
                                     """,
                                       arguments = { "id": HDbParam[int] }, )
        
        self.EDGE_LOOKUP = Script( cypher = """
                                            MATCH (n:<START_LABEL> { uid:{start_uid} })-[r:<LABEL>]->(m:<END_LABEL> { uid:{end_uid} })
                                            RETURN r
                                            """,
                                   arguments = { "start_label": HScriptParam[TNodeLabel],
                                                 "end_label"  : HScriptParam[TNodeLabel],
                                                 "label"      : HScriptParam[TEdgeLabel],
                                                 "start_uid"  : HDbParam[TNodeUid],
                                                 "end_uid"    : HDbParam[TNodeUid] } )
        
        self.EDGE_LOOKUP_NODE_ID = Script( cypher = """
                                            MATCH (n)-[r]->(m) WHERE ID(n) = {start_id} AND ID (m) = {end_id}
                                            RETURN r
                                         """,
                                           arguments = { "start_id": HDbParam[int],
                                                         "end_id"  : HDbParam[int] } )
        
        self.EDGE_ID_LOOKUP = Script( cypher = """
                                               MATCH p = (n)-[r]->(m) WHERE ID(r) = {id}
                                               RETURN p
                                               """,
                                      arguments = { "id": HDbParam[int] } )


__db_endpoint_scripts = None


def _db_endpoint_scripts() -> __DbEndpointScriptsClass:
    global __db_endpoint_scripts
    
    if __db_endpoint_scripts is None:
        __db_endpoint_scripts = __DbEndpointScriptsClass()
    
    return __db_endpoint_scripts


class DbEndpoint( IMasterOrigin, IEndpoint ):
    """
    A read/write endpoint that reads and writes data to/from the database
    
    For obvious reasons, attempts to read the entire database will result in an error.
    """
    
    
    class _ConnectionInfo:
        """
        Holds the connection information as a single marshallable object.
        """
        
        
        def __init__( self, name: str, driver: ENeo4jDriver, remote_address: str, user_name: str, directory: Optional[str], is_unix: Optional[bool], port: str ):
            self.name = name
            self.driver = driver
            self.remote_address = remote_address
            self.user_name = user_name
            self.directory = directory
            self.is_unix = is_unix
            self.port = port
        
        
        def get_directory( self ) -> str:
            if self.directory:
                return self.directory
            
            raise NotSupportedError( "Cannot obtain the Neo4j directory because the directory was not specified when the DbEndpoint was created." )
        
        
        def get_binary_directory( self ) -> str:
            return path.join( self.get_directory(), "bin" )
        
        
        def get_import_directory( self ) -> str:
            return path.join( self.get_directory(), "import" )
        
        
        def get_is_unix( self ) -> bool:
            if self.is_unix is not None:
                return self.is_unix
            
            raise NotSupportedError( "Cannot determine if Neo4j is running under Windows or Unix because that was not specified when the DbEndpoint was created." )
    
    
    def __getstate__( self ) -> Dict[str, object]:
        result = { "connection_info": self.__connection_info,
                   "password_key"   : self.__password_key }
        
        if not self.__password_key:
            result["password"] = self.__password
        
        return result
    
    
    def __setstate__( self, state: Dict[str, object] ) -> None:
        self.__connection_info = state["connection_info"]
        self.__password_key = state["password_key"]
        
        if self.__password_key:
            self.__password = keyring_.get_password( constants.KEYRING_NAME, self.__get_password_key() )
        else:
            self.__password = state["password"]
        
        self.__connections = []
        self.__used_connections = []
    
    
    def __get_password_key( self ) -> str:
        return "DbEndpoint:{}@{}+{}".format( self.__connection_info.user_name, self.__connection_info.remote_address, self.__password_key )
    
    
    def __init__( self,
                  *,
                  name: str,
                  driver: ENeo4jDriver,
                  remote_address: str,
                  user_name: str,
                  password: str,
                  directory: Optional[str],
                  is_unix: Optional[bool],
                  port: str,
                  keyring: bool ):
        super().__init__()
        
        self.__connection_info = self._ConnectionInfo( name, driver, remote_address, user_name, directory, is_unix, port )
        self.__password = password
        self.__password_key = str( uuid4() ) if keyring else None
        self.__connections = []
        self.__used_connections = []
        
        if keyring:
            keyring_.set_password( constants.KEYRING_NAME, self.__get_password_key(), self.__password )
            MCMD.progress( "Endpoint created. I have added the password to your system keyring." )
    
    
    def endpoint_deleted( self ) -> None:
        if self.__password_key:
            try:
                keyring_.delete_password( constants.KEYRING_NAME, self.__get_password_key() )
                MCMD.progress( "Endpoint deleted. I have removed the password from your system keyring." )
            except PasswordDeleteError as ex:
                warnings.warn( str( ex ), UserWarning )
    
    
    @property
    def connection_info( self ) -> "DbEndpoint._ConnectionInfo":
        return self.__connection_info
    
    
    def visualisable_info( self ) -> UiInfo:
        return UiInfo( name = self.__connection_info.name,
                       comment = self.__doc__,
                       type_name = "DB_EP",
                       value = str( self ),
                       colour = ENDPOINT_COLOUR,
                       icon = ENDPOINT_ICON,
                       extra = { "user_name"       : self.__connection_info.user_name,
                                 "remote_address"  : self.__connection_info.remote_address,
                                 "driver"          : self.__connection_info.driver,
                                 "directory"       : self.__connection_info.directory,
                                 "is_unix"         : self.__connection_info.is_unix,
                                 "password"        : "********" if (self.__password_key and self.__password) else self.__password,
                                 "connections"     : len( self.__connections ) + len( self.__used_connections ),
                                 "connections_idle": len( self.__connections ),
                                 "connections_used": len( self.__used_connections ) } )
    
    
    def __str__( self ) -> str:
        return "{}@{}".format( self.__connection_info.user_name, self.__connection_info.remote_address )
    
    
    def __acquire_manager( self ) -> _DbManager:
        if not self.__connections:
            from neocommand.database.database_manager import DbManager
            self.__connections.append( DbManager( self.__connection_info.driver, self.__connection_info.remote_address, self.__connection_info.user_name, self.__password, self.__connection_info.port ) )
        
        result = self.__connections.pop()
        self.__used_connections.append( result )
        return result
    
    
    def __release_manager( self, manager: _DbManager ) -> None:
        self.__used_connections.remove( manager )
        self.__connections.append( manager )
    
    
    def get_database( self ) -> ManagedWith:
        return ManagedWith( on_get_target = self.__acquire_manager, on_exit = self.__release_manager )
    
    
    def origin_get_edge_by_iid( self, iid: int ) -> Edge:
        ep = MemoryEndpoint()
        _db_endpoint_scripts().EDGE_ID_LOOKUP( id = iid,
                                               database = self,
                                               output = ep,
                                               quiet = True )
        
        return ep.only_child( Edge )
    
    
    def origin_get_edge_by_node_uids( self, label: str, start_label: str, end_label: str, start_uid: str, end_uid: str ) -> Edge:
        ep = MemoryEndpoint()
        _db_endpoint_scripts().EDGE_LOOKUP( label = label,
                                            start_label = start_label,
                                            end_label = end_label,
                                            start_uid = start_uid,
                                            end_uid = end_uid,
                                            database = self,
                                            output = ep,
                                            quiet = True )
        
        return ep.only_child( Edge )
    
    
    def origin_get_edge_by_node_iids( self, start_iid: int, end_iid: int ) -> Edge:
        ep = MemoryEndpoint()
        _db_endpoint_scripts().EDGE_LOOKUP_NODE_ID( start_id = start_iid,
                                                    end_id = end_iid,
                                                    database = self,
                                                    output = ep,
                                                    quiet = True )
        
        return ep.only_child( Edge )
    
    
    def origin_get_all( self ) -> Iterator[IEntity]:
        raise NotSupportedError( "Refusing to retrieve the entire database («{}»). Perhaps you meant to operate on a subset of the database?".format( self ) )
    
    
    def origin_get_all_nodes_property( self, label: str, property: str ) -> List[Tuple[str, object]]:
        text = "MATCH (n:`" + label + "`) RETURN n.`uid`, n.`" + property + "`"
        
        with self.get_database() as db:
            result = MemoryEndpoint()
            db.run_cypher( "Get properties", text, { } )
            result_list = array_helper.deinterleave_as_list( result.contents )  # type: List[Tuple[ str, object ] ]
            return result_list
    
    
    def origin_get_node_property_by_uid( self, label: str, uid: str, property: str ):
        ep = MemoryEndpoint()
        _db_endpoint_scripts().PROPERTY_LOOKUP_UID( label = label,
                                                    uid = uid,
                                                    property = property,
                                                    database = self,
                                                    output = ep,
                                                    quiet = True )
        return ep.only_child( object )
    
    
    def origin_get_node_property_by_iid( self, iid: int, property: str ):
        ep = MemoryEndpoint()
        _db_endpoint_scripts().PROPERTY_LOOKUP_IID( iid = iid,
                                                    property = property,
                                                    database = self,
                                                    output = ep,
                                                    quiet = True )
        return ep.only_child( object )
    
    
    def origin_get_node_by_uid( self, label: str, uid: str ):
        assert label
        assert uid
        
        ep = MemoryEndpoint()
        _db_endpoint_scripts().NODE_LOOKUP_UID( label = label,
                                                uid = uid,
                                                database = self,
                                                output = ep,
                                                quiet = True )
        return ep.only_child( Node )
    
    
    def origin_get_node_by_iid( self, iid: int ):
        ep = MemoryEndpoint()
        _db_endpoint_scripts().NODE_LOOKUP_IID( id = iid,
                                                database = self,
                                                output = ep,
                                                quiet = True )
        
        return ep.only_child( Node )
    
    
    def _ENDPOINT__set_name( self, value: str ):
        self.__connection_info.name = value
    
    
    def _ENDPOINT__get_name( self ) -> str:
        return self.__connection_info.name
    
    
    def _ENDPOINT_create_folder( self, _: str ) -> "IEndpoint":
        return self
    
    
    def _ENDPOINT_add_data( self, data: object ):
        warnings.warn( "This endpoint «{}» does not support the adding of arbitrary (non-node/edge) data «{}». This action has been ignored.".format( self, data ) )
    
    
    def _ENDPOINT_add_edge( self, edge: Edge ):
        from neocommand.database import database_manager
        
        args = []
        for k in edge.properties.keys():
            args.append( "r.`" + k + "` = {" + k + "}" )
        
        args = ",".join( args )
        
        if args:
            args = " SET " + args
        
        text = "MATCH (n:`" + edge.start.label + "` {uid:{start_uid}}), (m:`" + edge.end.label + "` {uid:{end_uid}}) MERGE (n)-[r:`" + edge.label + "`]->(m)" + args
        
        # noinspection PyTypeChecker
        parameters = dict( edge.properties.items() )
        parameters["start_uid"] = edge.start.uid
        parameters["end_uid"] = edge.end.uid
        
        with MCMD.host.database() as db:  # type: database_manager
            stats = None
            
            try:
                stats = db.run_cypher( "Create edge", text, MCMD, parameters, output = NULL_ENDPOINT )
                
                if stats.nodes_created != 0:
                    raise AddFailedError( "stats.nodes_created is {0} (expected 0)".format( stats.nodes_created ) )
                    
                    # if stats.relationships_created != 1:
                    #     raise AddFailedError( "stats.relationships_created is {0} (expected 1)".format( stats.relationships_created ) )
            
            except Exception as ex:
                raise AddFailedError( "Failed to add the edge due to the error «{0}». Properties: ({1} {2})-[{3}]>({4} {5}) {6}. Stats: {7}".format( ex, edge.start.label, edge.start.uid, edge.label, edge.end.label, edge.end.uid, edge.properties, stats ) ) from ex
    
    
    def _ENDPOINT_flush( self ) -> None:
        pass
    
    
    def _ENDPOINT_add_node( self, node: Node ):
        from neocommand.database import database_manager
        
        args = []
        # noinspection PyTypeChecker
        parameters = dict( node.properties.items() )
        parameters["uid"] = node.uid
        
        for k in parameters.keys():
            args.append( "n.`" + k + "` = {" + k + "}" )
        
        args = ",".join( args )
        
        if args:
            args = " SET " + args
        
        text = "MERGE (n:`" + node.label + "` {uid: {uid}})" + args
        
        with self.get_database() as db:  # type: database_manager.DbManager
            stats = None
            
            try:
                stats = db.run_cypher( title = "Create node",
                                       cypher = text,
                                       parameters = parameters,
                                       output = NULL_ENDPOINT )  # type:database_manager.DbStats
                
                # if stats.nodes_created != 1:
                #     raise AddFailedError( "stats.nodes_created is {0} (expected 1)".format( stats.nodes_created ) )
            except Exception as ex:
                raise AddFailedError( "Failed to add a database node due to the error «{0}». Label: «{1}»\nProperties: «{2}»\nStats: {3}".format( ex, node.label, node.properties, stats ) ) from ex


# noinspection SpellCheckingInspection
_EXT_ENDPOINT_PICKLE = ".eppickle"


# noinspection PyAbstractClass
class __ListBackedEndpoint( IOrigin, IEndpoint ):
    def _ENDPOINT__get_name( self ) -> str:
        return self.__name
    
    
    # noinspection PyMethodOverriding
    def _ENDPOINT__set_name( self, value: str ) -> None:
        self.__name = value
    
    
    def __init__( self, name: str, comment: Optional[str] ):
        super().__init__()
        self.__name = name
        self.comment = comment or ""
    
    
    def __len__( self ) -> int:
        """
        Folders have a length that is the size of the contents
        """
        if self.contents is not None:
            return len( self.contents )
        else:
            return -1
    
    
    @property
    def contents( self ) -> List[Optional[object]]:
        raise NotImplementedError( "abstract" )
    
    
    def _ENDPOINT_create_folder( self, name: str ) -> IEndpoint:
        result = MemoryEndpoint( name = name )
        self.contents.append( result )
        return result
    
    
    def _ENDPOINT_add_data( self, data: object ):
        self.contents.append( data )
    
    
    def _ENDPOINT_add_edge( self, edge: Edge ):
        self.contents.append( edge )
    
    
    def _ENDPOINT_add_node( self, node: Node ):
        self.contents.append( node )
    
    
    def origin_get_all( self ) -> Iterator[Union[Node, Edge]]:
        result = list( iterate_all( self, lambda x: isinstance( x, Node ) or isinstance( x, Edge ) ) )
        
        return result
    
    
    def origin_get_all_nodes_property( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        def __filter( x ) -> bool:
            return isinstance( x, Node ) and x.label == label
        
        
        for x in iterate_all( self, __filter ):
            if x.data is not None and property in x.data:
                yield x.uid, x.data[property]
    
    
    def visualisable_info( self ) -> UiInfo:
        return super().visualisable_info().supplement( count = len( self ),
                                                       contents = self.contents )
    
    
    def only_child( self, expected: Optional[Type[T]] = None ) -> T:
        """
        Returns the only child of this folder, or `None` if it is empty.
        Raises a `ValueError` if there is more than 1 item.
        """
        if len( self ) == 0:
            raise ValueError( "Cannot obtain the only child of a {} «{}» because the folder doesn't contain any elements.".format( type( self ), self ) )
        elif len( self ) == 1:
            result = self.contents[0]
            
            if isinstance( result, MemoryEndpoint ):
                result = result.only_child( expected )
            
            if expected is not None:
                if not isinstance( result, expected ):
                    raise ValueError( "Cannot obtain the only child of a {} «{}» because the result is of type «{}», not the expected type «{}».".format( type( self ), self, type( result ), expected ) )
            
            return result
        
        else:
            raise ValueError( "Cannot obtain the only child of a {} «{}» because the folder contains more than 1 child.".format( type( self ), self ) )
    
    
    def as_text( self ) -> List[str]:
        """
        Sometimes we want basic text from the database, such as UIDs or names.
        Our `DbManager` still gives back the results as `Docket`s, so we use this function to pull the text from the dockets into a simple list. 
        :return: 
        """
        result = [array_helper.decomplex( x ) for x in self.contents]  # due to mistakes in parsing, sometimes items are stored in the database as strings inside lists of length 1, this just pulls them out
        
        for x in result:
            if not isinstance( x, str ):
                raise ValueError( "At least one element is not `str` in `docket_to_text. The offending item is of type «{0}» and has a value of «{1}»".format( type( x ).__name__, repr( x ) ) )
        
        # noinspection PyTypeChecker
        return result
    
    
    def get_or_create_folder( self, path: str ) -> "List[__ListBackedEndpoint]":
        """
        Given a `/` separated path, locating or creating subfolders as necessary. Returns a list of the complete path.
        """
        if not path:
            return [self]
        
        path = path.replace( "\\", "/" )
        
        elements = path.split( "/" )
        results = []
        
        current = self  # type:MemoryEndpoint
        results.append( self )
        
        for element in elements:
            if element:
                element = MENV.host.translate_name( element )
                found = False
                
                for docket in current.contents:
                    if isinstance( docket, MemoryEndpoint ):
                        if MENV.host.translate_name( docket.endpoint_name ) == element:
                            current = docket  # type: MemoryEndpoint
                            found = True
                            break
                
                if not found:
                    new = MemoryEndpoint( name = element )
                    current.contents.append( new )
                    current = new
                
                results.append( current )
        
        return results


class PickleEndpoint( __ListBackedEndpoint ):
    """
    An endpoint, as a disk pickle.
    """
    
    
    def __init__( self, name: str, file_name: Filename[_EXT_ENDPOINT_PICKLE], *, comment = None ):
        super().__init__( name, comment )
        self.__file_name = file_name
        self.__contents = None
    
    
    @property
    def contents( self ) -> List[Optional[object]]:
        if self.__contents is None:
            if path.isfile( self.__file_name ):
                try:
                    self.__contents = io_helper.load_binary( self.__file_name )
                    assert isinstance( self.__contents, list )
                except Exception as ex:
                    raise ValueError( "Failed to recover the PickleEndpoint disk-list from «{0}». The internal error is «{1}: {2}». If this is causing problems, you may have to delete the endpoint and recreate it.".format( self.__file_name, type( ex ).__name__, ex ) )
            else:
                self.__contents = []
        
        return self.__contents
    
    
    def _ENDPOINT_flush( self ) -> None:
        io_helper.save_binary( self.__file_name, self.__contents )
    
    
    def visualisable_info( self ) -> UiInfo:
        value_str = ("{} items".format( len( self.__contents ) )) if (self.__contents is not None) else "Not yet loaded"
        
        return UiInfo( name = self.endpoint_name,
                       comment = "Endpoint backed to pickle" + ((": " + self.comment) if self.comment else ""),
                       type_name = "RAM_EP",
                       value = value_str,
                       colour = EColour.YELLOW,
                       icon = resources.folder,
                       extra = { "file": self.__file_name } )
    
    
    @override
    def __getstate__( self ) -> Dict[str, object]:
        return { "name"     : self.endpoint_name,
                 "file_name": self.__file_name }
    
    
    @override
    def __setstate__( self, state: Dict[str, object] ) -> None:
        self.endpoint_name = state["name"]
        self.__file_name = state["name"]
        self.__contents = None


class MemoryEndpoint( __ListBackedEndpoint ):
    """
    An endpoint, in local system memory.
    Can be pickled to disk.
    """
    
    
    def _ENDPOINT_flush( self ) -> None:
        pass
    
    
    def __init__( self, name: Optional[str] = None, *, comment = None ) -> None:
        super().__init__( name, comment )
        self.__contents = _SafeList()
    
    
    def visualisable_info( self ) -> UiInfo:
        return UiInfo( name = self.endpoint_name,
                       comment = "Endpoint in local memory" + ((": " + self.comment) if self.comment else ""),
                       type_name = "RAM_EP",
                       value = "{} items".format( len( self.contents ) ),
                       colour = EColour.YELLOW, icon = resources.folder )
    
    
    @property
    def contents( self ) -> List[Optional[object]]:
        return self.__contents


class _SafeList( list ):
    SAFE_TYPES = (int, str, float, bool, list, tuple, Node, Edge, MemoryEndpoint)
    
    
    def append( self, item: object ) -> None:
        if not type( item ) in self.SAFE_TYPES:
            raise ValueError( "Attempt to add an item «{}» of type «{}» to a SafeList, but the SafeList doesn't expect such items." )
        
        super().append( item )


class NeoCsvFolderEndpoint( IEndpoint, IOrigin ):
    """
    Represents a single folder and the actions to perform upon it
    
    When used as a function annotation to a Plugin this denotes the parcel may or may not exist because the default `create` value on `__init__` is `None`.
    """
    
    
    def _ENDPOINT__get_name( self ) -> str:
        return self.__name
    
    
    def _ENDPOINT__set_name( self, value: str ) -> None:
        self.__name = value
    
    
    # region Unique
    
    
    def remove_folder_from_disk( self ) -> None:
        """
        Remove the folder from the disk
        """
        file_helper.recycle_file( self.__path )
    
    
    def __init__( self, name: str, path: str ):
        """
        CONSTRUCTOR
        :param name: Name or path of parcel 
        """
        super().__init__()
        self.__name = name
        self.__path = path
        self.__writer = NeoCsvMultiWriter( self.full_path() )
        file_helper.create_directory( self.__path )
    
    
    def validate( self ) -> None:
        """
        Raises an error of the parcel directory doesn't exist
        """
        if not path.isdir( self.full_path() ):
            raise FileNotFoundError( "The parcel «{0}» does not exist".format( self ) )
    
    
    def get_file( self, name ) -> str:
        """
        Obtains the full filename of the file called `name`
        """
        return path.join( self.full_path(), name )
    
    
    def iterate_contents( self ) -> Iterator[NeoCsvFilename]:
        if not self.exists():
            return
        
        for file_name in file_helper.list_dir( self.full_path(), constants.EXT_B42CSV, False ):
            try:
                yield NeoCsvFilename.construct_from_file( file_name )
            except:
                pass
    
    
    def exists( self ) -> bool:
        return path.isdir( self.full_path() )
    
    
    def full_path( self ) -> str:
        return self.__path
    
    
    # endregion
    
    # region object
    
    @override
    def __str__( self ) -> str:
        return file_helper.get_filename( self.__path )
    
    
    @override
    def __len__( self ) -> int:
        return len( list( self.iterate_contents() ) )
    
    
    # endregion
    
    # region IVisualisable
    
    
    @override
    def visualisable_info( self ) -> UiInfo:
        if self.exists():
            value_text = "Maps I/O to folder on disk ({} items)".format( len( self ) )
        else:
            value_text = "Maps I/O to folder on disk (**MISSING**)"
        
        return UiInfo( name = str( self ),
                       comment = "NeoCsvFolderEndpoint at «{}»".format( self.full_path() ),
                       type_name = "NEOCSV_EP",
                       value = value_text,
                       colour = FILE_ENDPOINT_COLOUR,
                       icon = FILE_ENDPOINT_ICON,
                       extra_named = self.iterate_contents,
                       extra = { "directory": file_helper.get_directory( self.__path ),
                                 "file_name": file_helper.get_filename( self.__path ),
                                 "full_path": self.full_path() } )
    
    
    # endregion
    
    # region IOrigin
    
    @override
    def origin_get_all( self ) -> Iterator[IEntity]:
        for file in self.iterate_contents():
            reader = NeoCsvReader( file )
            
            is_edge = file.is_edge
            
            if is_edge:
                for line in reader:
                    start = Node( label = file.start_label, uid = line[constants.NEO4J_START_ID_SUFFIX], iid = None, name = None, comment = None, properties = None )
                    end = Node( label = file.end_label, uid = line[constants.NEO4J_END_ID_SUFFIX], iid = None, name = None, comment = None, properties = None )
                    data = { }
                    
                    for key, value in line.items():
                        if key not in (constants.NEO4J_START_ID_SUFFIX, constants.NEO4J_END_ID_SUFFIX):
                            data[key] = value
                    
                    yield Edge( name = None, comment = None, iid = None, label = file.label, start = start, end = end, data = data )
    
    
    @override
    def origin_get_all_nodes_property( self, label: str, property: str ) -> Iterator[Tuple[str, object]]:
        raise NotImplementedError( "Not implemented yet, sorry." )
    
    
    # endregion
    
    # region IEndpoint
    
    
    @override
    def _ENDPOINT_create_folder( self, name: str ) -> IEndpoint:
        """
        OVERRIDE IEndpoint
        Does nothing
        """
        return self
    
    
    @override
    def _ENDPOINT_add_data( self, data: object ):
        warnings.warn( "This endpoint «{}» does not support the adding of arbitrary (non-node/edge) data «{}». This action has been ignored.".format( self, data ) )
    
    
    @override
    def _ENDPOINT_add_edge( self, edge: Edge ):
        """
        Adds an edge-csv
        """
        self.__writer.write_edge( edge )
    
    
    @override
    def _ENDPOINT_add_node( self, node: Node ):
        """
        OVERRIDE
        Write a node
        """
        assert all( node.properties.keys() )
        
        try:
            self.__writer.write_node( node )
        except Exception as ex:
            ss = ["Failed to write node. See causing error for details. Node details follow:",
                  "-- label = {}".format( node.label ),
                  "-- uid = {}".format( node.uid ),
                  "\n--",
                  "\n-- ".join( "{} = {}".format( k, v ) for k, v in node.properties.items() )]
            
            raise ValueError( "\n".join( ss ) ) from ex
    
    
    @override
    def _ENDPOINT_flush( self ) -> None:
        """
        OVERRIDE
        Flush 
        """
        self.__writer.close_all()
        
        
        # endregion IEndpoint


class CountingEndpointWrapper( IEndpoint ):
    """
    Wraps another endpoint and counts the operations thereupon.
    """
    
    
    def _ENDPOINT__set_name( self, value: str ):
        raise ValueError( "Cannot set the name of the endpoint through a `CountingEndpointWrapper`." )
    
    
    def _ENDPOINT__get_name( self ) -> str:
        return self.__endpoint.endpoint_name
    
    
    def __init__( self, endpoint: IEndpoint ):
        super().__init__()
        self.__endpoint = endpoint
        self.num_nodes = 0
        self.num_edges = 0
    
    
    @override
    def _ENDPOINT_add_data( self, data: object ):
        return self.__endpoint.endpoint_add_data( data )
    
    
    def _ENDPOINT_add_node( self, node: Node ):
        self.num_nodes += 1
        return self.__endpoint.endpoint_add_node( node )
    
    
    def _ENDPOINT_add_edge( self, edge: Edge ):
        self.num_edges += 1
        return self.__endpoint.endpoint_add_edge( edge )
    
    
    def _ENDPOINT_create_folder( self, name: str ) -> "IEndpoint":
        return self.__endpoint.endpoint_create_folder( name = name )
    
    
    def _ENDPOINT_flush( self ) -> None:
        return self.__endpoint.endpoint_flush()
    
    
    def __str__( self ) -> str:
        return "{} nodes and {} edges to {}".format( self.num_nodes, self.num_edges, self.__endpoint )
    
    
    def visualisable_info( self ) -> UiInfo:
        return self.__endpoint.visualisable_info()


_EXT_GEXF = ".gexf"


class EntityResolver:
    """
    The `EntityResolver` manages an `IMasterOrigin`, which is used to resolve incomplete database entities.
    """
    
    
    def __init__( self, endpoint: Optional[IMasterOrigin], cache_enabled: bool, enforce_enabled: bool ) -> None:
        self.name: str = endpoint.endpoint_name if endpoint is not None else None
        self.cache_enabled: bool = cache_enabled
        self.enforce_enabled: bool = enforce_enabled
    
    
    def acquire( self ) -> _EntityResolverUsage_:
        return EntityResolverUsage( self )
    
    
    def _get_origin( self ) -> Optional[IMasterOrigin]:
        from neocommand.data.core import CORE
        
        if self.name is None:
            # None = default database
            result = CORE.endpoint_manager.get_database_endpoint( tolerant = True )
            
            if result is None:
                MCMD.warning( "There are empty nodes and due to a previous issue I cannot obtain their data. Some data may be missing from your output." )
        
        else:
            # Name = find named
            result = CORE.endpoint_manager.find_endpoint( self.name )
            
            if result is None:
                MCMD.warning( "There are empty nodes and due to a previous issue I cannot obtain their data. Some data may be missing from your output." )
        
        return result
    
    
    def __str__( self ) -> str:
        return self.name or "(default)"


class EntityResolverUsage:
    def __init__( self, resolver: EntityResolver ):
        self.__resolver: EntityResolver = resolver
        self.__origin: IMasterOrigin = resolver._get_origin()
        self.__used_missing_edge_warning: bool = False
        self.__used_missing_node_warning: bool = False
        self.__edge_cache: Dict[str, Edge] = { }
        self.__node_cache: Dict[str, Node] = { }
        self.__edge_count = 0
        self.__node_count = 0
    
    
    def __getstate__( self ) -> Dict[str, object]:
        raise NotSupportedError( "This class should not be serialised." )
    
    
    def describe( self ) -> str:
        return "{} nodes and {} edges resolved from {}.".format( self.__node_count, self.__edge_count, self.__origin )
    
    
    def is_node_valid( self, node: Node ) -> bool:
        assert node is not None
        
        return node.label and node.uid
    
    
    def is_edge_valid( self, edge: Edge ) -> bool:
        assert edge is not None
        
        return edge.label \
               and edge.start \
               and ((edge.start.label and edge.start.uid) or edge.start.iid) \
               and edge.end \
               and ((edge.end.label and edge.end.uid) or edge.end.iid)
    
    
    def get_node_cache_names( self, nodes: Sequence[Node] ) -> List[str]:
        results = []
        
        for node in nodes:
            if node.label is not None and node.uid is not None:
                results.append( "n" + node.label + "\t" + node.uid )
                break
        
        for node in nodes:
            if node.iid is not None:
                results.append( node.iid )
                break
        
        return results
    
    
    def get_edge_cache_names( self, edges: Sequence[Edge] ) -> List[str]:
        results = []
        
        for edge in edges:
            if edge.start is not None and edge.end is not None and edge.start.label is not None and edge.start.uid is not None and edge.end.label is not None and edge.end.uid is not None:
                results.append( "e" + edge.label + "\t" + edge.start.label + "\t" + edge.end.label + "\t" + edge.start.uid + "\t" + edge.end.uid )
                break
        
        for edge in edges:
            if edge.start is not None and edge.end is not None and edge.start.iid is not None and edge.end.iid is not None:
                results.append( "e" + str( edge.start.iid ) + "\t" + str( edge.end.iid ) )
                break
        
        for edge in edges:
            if edge.iid is not None:
                results.append( "e" + str( edge.start.iid ) + "\t" + str( edge.end.iid ) )
                break
        
        return results
    
    
    def prepare_node( self, node: Node ) -> None:
        if self.is_node_valid( node ):
            self.cache_node( (node,) )
    
    
    def prepare_edge( self, edge: Edge ) -> None:
        if self.is_edge_valid( edge ):
            self.cache_edge( (edge,) )
    
    
    def cache_node( self, nodes: Sequence[Node] ) -> None:
        first = nodes[0]
        
        if not self.is_node_valid( first ):
            raise ValueError( "Attempt to cache a node that itself is not complete is probably a mistake." )
        
        for name in self.get_node_cache_names( nodes ):
            self.__node_cache[name] = first
    
    
    def cache_edge( self, edges: Sequence[Edge], include_nodes: bool = True ) -> None:
        first = edges[0]
        
        assert self.is_edge_valid( first )
        
        if not self.__resolver.cache_enabled:
            return
        
        for name in self.get_edge_cache_names( edges ):
            self.__edge_cache[name] = first
        
        if include_nodes:
            if self.is_node_valid( first.start ):
                self.cache_node( [x.start for x in edges] )
            
            if self.is_node_valid( first.end ):
                self.cache_node( [x.end for x in edges] )
    
    
    def uncache_node( self, nodes: Sequence[Node] ) -> Optional[Node]:
        for name in self.get_node_cache_names( nodes ):
            result = self.__node_cache.get( name )
            
            if result is not None:
                return result
        
        return None
    
    
    def uncache_edge( self, edges: Sequence[Edge] ) -> Optional[Edge]:
        if not self.__resolver.cache_enabled:
            return None
        
        for name in self.get_edge_cache_names( edges ):
            result = self.__edge_cache.get( name )
            
            if result is not None:
                return result
        
        return None
    
    
    def resolve_node( self, node: Node ) -> Optional[Node]:
        if self.is_node_valid( node ):
            self.cache_node( (node,) )
            return node
        
        result = self.uncache_node( (node,) )
        
        if result is not None:
            return result
        
        if self.__origin is not None:
            if node.label is not None and node.uid is not None:
                result = self.__origin.origin_get_node_by_uid( node.label, node.uid )
            
            if result is None and node.iid is not None:
                result = self.__origin.origin_get_node_by_iid( node.iid )
        
        if result is not None:
            if not self.is_node_valid( result ):
                raise ValueError( "Attempt to resolve a node resulted in another node which also isn't resolved." )
            
            self.__node_count += 1
            self.cache_node( (result, node) )
            return result
        elif self.__resolver.enforce_enabled:
            raise ValueError( "Cannot make the node concrete because I can't find it or it doesn't exist in the database." )
        elif not self.__used_missing_node_warning:
            self.__used_missing_node_warning = True
            MCMD.warning( "Nodes without data have been detected. Some data may be missing from your output. See section `Needs resolve` in `neocommand/readme.md`." )
        
        return None
    
    
    def resolve_edge_nodes( self, include_nodes: bool, edge: Edge ) -> Edge:
        if not include_nodes:
            return edge
        
        assert self.is_edge_valid( edge )
        
        if not self.is_node_valid( edge.start ) or not self.is_node_valid( edge.end ):
            edge = Edge( label = edge.label,
                         start = self.resolve_node( edge.start ),
                         end = self.resolve_node( edge.end ),
                         name = edge.name,
                         comment = edge.comment,
                         iid = edge.iid,
                         data = dict( edge.properties ) )
        
        return edge
    
    
    def resolve_edge( self, edge: Edge, include_nodes: bool = True ) -> Optional[Edge]:
        #
        # Already complete
        #
        if self.is_edge_valid( edge ):
            edge = self.resolve_edge_nodes( include_nodes, edge )
            self.cache_edge( (edge,) )
            return edge
        
        #
        # In cache
        #
        result = self.uncache_edge( (edge,) )
        
        if result is not None:
            return result
        
        #
        # From origin
        #
        if self.__origin is None:
            if edge.start is not None and edge.end is not None:
                if edge.start.label is not None and edge.start.uid is not None and edge.end.label is not None and edge.end.uid is not None:
                    result = self.__origin.origin_get_edge_by_node_uids( label = edge.label,
                                                                         start_label = edge.start.label,
                                                                         end_label = edge.end.label,
                                                                         start_uid = edge.start.uid,
                                                                         end_uid = edge.end.uid )
                elif edge.start.iid is not None and edge.end.iid is not None:
                    result = self.__origin.origin_get_edge_by_node_iids( start_iid = edge.start.iid, end_iid = edge.end.iid )
            
            if result is None and edge.iid is not None:
                result = self.__origin.origin_get_edge_by_iid( edge.iid )
        
        if result is not None:
            result = self.resolve_edge_nodes( include_nodes, result )
            self.__edge_count += 1
            self.cache_edge( (result, edge) )
            return result
        
        if self.__resolver.enforce_enabled:
            raise ValueError( "Cannot make the edge concrete because I can't find it or it doesn't exist in the database." )
        elif not self.__used_missing_edge_warning:
            self.__used_missing_edge_warning = True
            MCMD.warning( "Edges without nodes have been detected. Some data may be missing from your output. See section `needs-resolve` in `readme.md`." )
        
        return None


class GexfEndpoint( IEndpoint ):
    def _ENDPOINT__get_name( self ) -> str:
        return self.__name
    
    
    def _ENDPOINT__set_name( self, value: str ) -> None:
        self.__name = value
    
    
    def visualisable_info( self ) -> UiInfo:
        return UiInfo( name = self.__name,
                       comment = "GEXF endpoint to «{}»".format( self.__file_name ),
                       type_name = "GEXF_EP",
                       value = self.__file_name,
                       colour = FILE_ENDPOINT_COLOUR,
                       icon = FILE_ENDPOINT_ICON,
                       extra = { "resolver"         : self.__resolver.name,
                                 "resolver_cached"  : self.__resolver.cache_enabled,
                                 "resolver_enforced": self.__resolver.enforce_enabled } )
    
    
    def __init__( self, name: str,
                  file_name: Filename[EFileMode.WRITE, _EXT_GEXF],
                  resolver: Optional[IMasterOrigin],
                  cache_enabled: bool,
                  enforce_enabled: bool ):
        super().__init__()
        self.__name = name
        self.__file_name = file_name
        self.__edges = []
        self.__nodes = []
        self.__resolver = EntityResolver( resolver, cache_enabled, enforce_enabled )
    
    
    @property
    def file_name( self ) -> str:
        return self.__file_name
    
    
    def __getstate__( self ) -> Dict[str, object]:
        return { "name"     : self.__name,
                 "file_name": self.__file_name,
                 "resolver" : self.__resolver }
    
    
    def __setstate__( self, state: Dict[str, object] ) -> None:
        self.__name = state["name"]
        self.__file_name = state["file_name"]
        self.__resolver = state["resolver"]
        self.__edges = []
        self.__nodes = []
    
    
    @override
    def _ENDPOINT_add_data( self, data: object ):
        if data is None:
            return
        
        warnings.warn( "This endpoint «{}» does not support the adding of arbitrary (non-node/edge) data «{}». This action has been ignored.".format( self, data ) )
    
    
    def _ENDPOINT_add_edge( self, edge: Edge ):
        self.__edges.append( edge )
    
    
    def _ENDPOINT_add_node( self, node: Node ):
        self.__nodes.append( node )
    
    
    def _ENDPOINT_flush( self ) -> None:
        resolver = self.__resolver.acquire()
        
        TEMPLATE = \
            """
            <gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
                <meta lastmodifieddate="2017-04-20">
                    <creator>$(APP_DISPLAY_NAME)</creator>
                    <description>This file was exported by $(APP_DISPLAY_NAME)'s GephiExport plugin</description>
                </meta>
                <graph mode="static" defaultedgetype="directed">
                    <attributes class="node">
        {0}
                    </attributes>
                    <attributes class="edge">
        {1}
                    </attributes>
                    <nodes>
        {2}
                    </nodes>
                    <edges>
        {3}
                    </edges>
                </graph>
            </gexf>
            """
        
        TEMPLATE = MENV.host.substitute_text( TEMPLATE )
        
        nodes: Dict[str, Tuple[Node, int]] = OrderedDict()
        edges: Dict[str, Tuple[Edge, int]] = OrderedDict()
        
        num_nodes = 0
        num_edges = 0
        
        for node in self.__nodes:
            resolver.prepare_node( node )
        
        for edge in self.__edges:
            resolver.prepare_edge( edge )
        
        for node in self.__nodes:
            self.__add_node_to_list( resolver, node, nodes )
        
        for edge in self.__edges:
            edge = resolver.resolve_edge( edge )
            start = self.__add_node_to_list( resolver, edge.start, nodes )
            end = self.__add_node_to_list( resolver, edge.end, nodes )
            
            if edge is None:
                continue
            
            local_key = "\t".join( [edge.label, start.label, start.uid, end.label, end.uid] )
            
            if local_key in edges:
                continue
            
            edges[local_key] = edge, len( edges )
        
        node_xml = []
        edge_xml = []
        node_attrs = { }
        node_attr_xml = []
        edge_attrs = { }
        edge_attr_xml = []
        
        for node, node_id in nodes.values():
            node_xml.append( '                <node id="{0}" label="{1}">'.format( node_id, node.label ) )
            num_nodes += 1
            self.__write_attributes( node, node_attr_xml, node_attrs, node_xml )
            node_xml.append( '                </node>' )
        
        for edge, edge_id in edges.values():
            start_id = nodes[self.__get_node_local_key( edge.start )][1]
            end_id = nodes[self.__get_node_local_key( edge.end )][1]
            edge_xml.append( '                <edge id="{0}" label="{1}" source="{2}" target="{3}">'.format( edge_id, edge.label, start_id, end_id ) )
            num_edges += 1
            self.__write_attributes( edge, edge_attr_xml, edge_attrs, edge_xml )
            edge_xml.append( '                </edge>' )
        
        xml = TEMPLATE.format( "\n".join( node_attr_xml ), "\n".join( edge_attr_xml ), "\n".join( node_xml ), "\n".join( edge_xml ) )
        
        
        
        if self.__file_name == "stdout":
            print( xml )
        elif self.__file_name == "ui":
            MCMD.print( xml )
        else:
            directory_name = file_helper.get_directory( self.__file_name )
            file_helper.create_directory( directory_name )
            file_helper.write_all_text( self.__file_name, xml )
        
        MCMD.progress( "Flushed GEXF endpoint to disk: " + self.__file_name )
        MCMD.progress( "{} nodes and {} edges.".format( len( nodes ), len( edges ) ) )
        MCMD.progress( "{}".format( resolver.describe() ) )
        
        self.__edges.clear()
        self.__nodes.clear()
    
    
    def __add_node_to_list( self, resolver: EntityResolverUsage, node: Node, nodes: Dict[str, Tuple[Node, int]] ) -> Node:
        node = resolver.resolve_node( node )
        
        local_key = self.__get_node_local_key( node )
        
        if local_key in nodes:
            return node
        
        nodes[local_key] = node, len( nodes )
        
        return node
    
    
    @staticmethod
    def __get_node_local_key( node: Node ) -> str:
        assert node.label
        assert node.uid
        
        luid = [str( node.label ), str( node.uid )]
        return "\t".join( luid )
    
    
    @staticmethod
    def __write_attributes( entity: Union[Edge, Node], attr_xml: List[str], attrs, xml: List[str] ):
        xml.append( '                    <attvalues>' )
        for k, v in entity.properties.items():
            if k not in attrs:
                aid = len( attrs )
                attrs[k] = aid
                attr_xml.append( '                <attribute id="{0}" title="{1}" type="string"/>'.format( aid, k ) )
            else:
                aid = attrs[k]
            
            xml.append( '                        <attvalue for="{0}" value="{1}"/>'.format( aid, str( v ) ) )
        xml.append( '                    </attvalues>' )
