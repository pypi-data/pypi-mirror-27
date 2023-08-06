from typing import Optional

from intermake import MCMD, MENV, PathToVisualisable, command, console_explorer, visibilities
from intermake.plugins.command_plugin import help_command
from intermake.plugins.console_explorer import re_ls
from mhelper import Dirname, Filename, MOptional, MUnion, Password, file_helper
from neocommand.data import constants
from neocommand.data.core import CORE
from neocommand.data.settings import ENeo4jDriver
from neocommand.database.endpoints import DbEndpoint, GexfEndpoint, IEndpoint, IIoBase, IMasterOrigin, IOrigin, NeoCsvFolderEndpoint


@command( names = ["list_endpoints", "endpoints"] )
def list_endpoints():
    """
    Lists the available endpoints.
    """
    # Just use the read-made `ls` function
    re_ls( PathToVisualisable.find_path( CORE, CORE.endpoint_manager ) )


@help_command()
def needs_resolve_help():
    """
    When transferring data from one endpoint to another (i.e. `source` --> `destination`) sometimes the origin may not contain all of the information you want to place in the endpoint. Consider the following Cypher query:

    ```cypher
    MATCH (:Sequence)-[r:Like]->(:Sequence) RETURN r LIMIT 1
    ```
    
    Unfortunately, the relationship is returned from Neo4j _without_ the node data, hence `destination` receives a relationship but is unable to specify the nodes that relationship is connected to.
    
    To fix this issue consider the following:
    
    * **Use the `PY2NEO` driver on your `source`** - When constructing your database, specify the PY2NEO driver. This driver does a better job of returning pertinent data.
    * **Specify a resolver on your `destination`** - The resolver argument specifies a database that can be queried, during the transfer, in order to fill out the missing information.
        * The resolver takes a three arguments:
            * `resolver` specifies the database used to resolve missing entries. The default `None` is the primary database. If you have multiple database connections then you should specify a database explicitly. You can use `null` endpoint to suppress automated resolution.
            * `no_cache` disables the resolver cache. Resolved entities are retained in memory. The cache is enabled by default - disable it if you are expecting very large output where caching entries may lead to an out of memory error.
            * `no_enforce` prevents raising an error if resolving fails. Errors are enabled by default - if you don't wish to resolve entities and don't care about missing data, disable this option.
    """
    pass


@command( visibility = visibilities.HIGHLIGHT )
def new_gephi( name: Optional[str] = None,
               path: MOptional[Filename] = None,
               resolver: Optional[IMasterOrigin] = None,
               no_cache: bool = False,
               no_enforce: bool = False ) -> IIoBase:
    """
    Creates a new endpoint: Gephi
    
    At least the `name` or `path` argument must be specified.
    
    :param no_enforce:  Whether to prevent enforced resolution. See `needs_resolve_help` for details. 
    :param no_cache:    Whether to prevent allow caching of resolution data. See `needs_resolve_help` for details. 
    :param resolver:    Used to resolve missing data. See `needs_resolve_help` for details.
    :param name:        Name of the endpoint.
                        If not specified, the filename will be used.
    :param path:        Path to GEXF file.
                        This will be created if it doesn't already exist.
                        If not specified, a file in the `workspace` will be created with the specified `name`.
                        Note that the following special paths are also accepted:
                            `ui` - write to MCMD (STDERR for CLI, output messages for GUI)
                            `stdout` - write to STDOUT. Not compatible with GUI.
    :return:            The endpoint is returned. 
    """
    name, path = __resolve_name_and_path( name, path )
    endpoint = GexfEndpoint( name, path, resolver, not no_cache, not no_enforce )
    CORE.endpoint_manager.add_user_endpoint( endpoint )
    MCMD.information( "New GEXF endpoint created at «{}».".format( endpoint.file_name ) )
    return endpoint


@command( visibility = visibilities.HIGHLIGHT )
def new_parcel( name: Optional[str] = None, path: MOptional[Dirname] = None ) -> IIoBase:
    """
    Creates a new endpoint: CSV-folder
    
    (These endpoints are folders containing CSV files in the correct format for bulk importing into the database)
    
    At least the `name` or `path` argument must be specified.
    
    :param name:    Name of the endpoint.
                    If not specified, the path will be used.
    :param path:    Path to folder.
                    This will be created if it doesn't already exist.
                    If not specified, a folder in the `workspace` will be created with the specified `name`.
    :return: The endpoint is returned. 
    """
    name, path = __resolve_name_and_path( name, path )
    endpoint = NeoCsvFolderEndpoint( name, path )
    CORE.endpoint_manager.add_user_endpoint( endpoint )
    
    if len( endpoint ) == 0:
        MCMD.information( "New parcel created at «{}».".format( endpoint.full_path() ) )
    else:
        MCMD.information( "Existing parcel opened at «{}».".format( endpoint.full_path() ) )
    
    return endpoint


@command( visibility = visibilities.HIGHLIGHT )
def new_connection( name: str, driver: ENeo4jDriver, host: str, user: str, password: Password, directory: MOptional[Dirname] = None, unix: Optional[bool] = None, windows: Optional[bool] = None, port: str = "7474", plain = False ) -> IIoBase:
    """
    Creates a new endpoint: Neo4j database
    
    :param windows:     Set if the database is hosted on Windows. Optional.
    :param unix:        Set if the database is hosted on Unix. Optional.
    :param directory:   Set to the local Neo4j installation directory. Optional.
    :param name:        Name you will call the endpoint
    :param driver:      Database driver 
    :param host:        Database host
    :param user:        Database username
    :param password:    Database password. Nb. Use `password=prompt` to be prompted by the CLI.
    :param port:        Database port 
    :param plain:       Normally, passwords will be stored on the system keyring (requires the `keyring` Python package) and are not displayed to the user. If this flag is set, the password is stored in plain text and is not masked by the UI.
    :return:            The endpoint is returned.  
    """
    if windows and unix:
        raise ValueError( "Cannot specify both the `windows` and `unix` parameters." )
    
    unix = not windows
    
    endpoint = DbEndpoint( name = name,
                           driver = driver,
                           remote_address = host,
                           user_name = user,
                           password = password.value,
                           directory = str( directory ) if directory else None,
                           is_unix = unix,
                           port = port,
                           keyring = not plain )
    
    CORE.endpoint_manager.add_user_endpoint( endpoint )
    return endpoint


def __resolve_name_and_path( name: Optional[str], path: MOptional[MUnion[Filename, Dirname]] ):
    if name is None:
        if path is None:
            raise ValueError( "A name and/or a path must be specified." )
        
        name = file_helper.get_filename_without_extension( path )
    
    if path is None:
        path = file_helper.join( MENV.local_data.get_workspace(), constants.FOLDER_PIPELINES, name )
    
    return name, path


@command()
def connections() -> None:
    """
    Lists the endpoints.
    """
    console_explorer.re_ls( PathToVisualisable.find_path( CORE, CORE.endpoint_manager ) )


@command()
def close( endpoint : IIoBase ):
    """
    Removes a reference to a user-endpoint.
    (This affects $(APPNAME) only - contents on disk, if any, are unaffected)
    
    :param endpoint: The endpoint to remove.
    """
    CORE.endpoint_manager.remove_user_endpoint( endpoint )
    MCMD.information( "Endpoint closed: {}".format( endpoint.endpoint_name ) )
    MCMD.information( "(Note that closing endpoints does not remove them from disk)" )


@command()
def transfer( input: IOrigin, output: IEndpoint ):
    """
    Transfers all information from one endpoint to another.
     
    :param input:   Input, where to source data from.
    :param output:  Output, where to send data to. 
    """
    for entity in input.origin_get_all():
        output.endpoint_add_entity( entity )


@command( visibility = visibilities.TEST )
def small_test( endpoint: IEndpoint ):
    """
    Tests the endpoint
    :param endpoint:    Endpoint to send to 
    """
    endpoint.endpoint_create_node( label = "node_label", uid = "start_node_uid", properties = { "prop1": 1, "prop2": 2 } )
    endpoint.endpoint_create_node( label = "node_label", uid = "end_node_uid", properties = { "prop1": 1, "prop2": 2 } )
    endpoint.endpoint_create_edge( label = "edge_label", start_label = "node_label", start_uid = "start_node_uid", end_label = "node_label", end_uid = "end_node_uid", properties = { "prop1": 1, "prop2": 2 } )
    folder = endpoint.endpoint_create_folder( "folder" )
    folder.endpoint_create_node( label = "node_label", uid = "start_node_uid_2", properties = { "prop1": 1, "prop2": 2 } )
    folder.endpoint_create_node( label = "node_label", uid = "end_node_uid_2", properties = { "prop1": 1, "prop2": 2 } )
    folder.endpoint_create_edge( label = "edge_label", start_label = "node_label", start_uid = "start_node_uid_2", end_label = "node_label", end_uid = "end_node_uid_2", properties = { "prop1": 1, "prop2": 2 } )
