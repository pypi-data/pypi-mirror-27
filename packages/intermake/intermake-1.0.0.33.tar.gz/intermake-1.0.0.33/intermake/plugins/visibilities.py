from typing import cast, Optional

from intermake.engine.constants import EThread
from intermake.hosts.base import ERunMode

from mhelper import reflection_helper


_OUV = "Optional[Union[bool, VisibilityClass]]"


class VisibilityClass:
    """
    Designates a class that manages visibility of a plugin.
    It is a callable returning a boolean, so can be passed to the plugin's `visibility` parameter.
    
    Example:
    ```
    MARTINS_SET = VisibilityClass( name = "martin", default = False )
    
    @command(visibility = MARTINS_SET)
    def martins_plugin(...):
        ....
        
    @command(visibility = MARTINS_SET[lambda: time().minute == 42])
    def hourly(...):
        ....
        
    def show_martins_plugins():
        MARTINS_SET.enabled = True        
    ```
     
    """
    
    
    def __init__( self, *, name: str, functional: _OUV = None, default: _OUV = None, comment = None ):
        """
        CONSTRUCTOR
        :param *: 
        :param functional: 
        :param name:        Name of the class
        :param functional:  Is this set functional? (see `VisibilityClass`).
                            If this is `False` the class won't even show up in the list of optional `VisibilityClass`es.
        :param default:     Default visibility (see `VisibilityClass`).
        """
        if functional is None:
            functional = True
        
        if default is None:
            default = True
        
        default = reflection_helper.as_delegate( default, bool )
        functional = reflection_helper.as_delegate( functional, bool )
        
        self.name = name
        self.enabled = cast( Optional[bool], None )
        self.default = default
        self.functional = functional
        self.comment = comment or ""
    
    
    def __call__( self ) -> bool:
        """
        When called, returns the default visibility, unless overridden.
        """
        if self.enabled is True:
            return True
        elif self.enabled is False:
            return False
        
        return self.functional() and self.default()
    
    
    def __getitem__( self, item: _OUV ):
        """
        Combines two visibilities together.
        """
        if item is None:
            return self
        
        if item is True:
            return self
        
        item = reflection_helper.as_delegate( item, bool )
        return lambda: self() and item()
    
    
    def __str__( self ) -> str:
        return "{} is {}".format( self.name, "visible" if self.enabled else "hidden" )


def __are_any_plugins_multithreaded() -> bool:
    from intermake.engine.environment import MENV
    return any( True for x in MENV.plugins.all_plugins() if x.threading() != EThread.SINGLE )


def __is_gui_host() -> bool:
    from intermake.engine.environment import MENV
    return MENV.host.run_mode != ERunMode.GUI


HELP = VisibilityClass( name = "help",
                        comment = "Help commands. Hidden by default because they can are already listed using the `help` command." )

COMMON = VisibilityClass( name = "common",
                          comment = "Common commands. Visible by default." )

CLUSTER = VisibilityClass( name = "cluster",
                           functional = __are_any_plugins_multithreaded,
                           comment = "Commands relating to a compute cluster. Visible by default if any plugins support a compute cluster." )

ADVANCED = VisibilityClass( name = "advanced",
                            default = False,
                            comment = "Advanced commands. Hidden by default." )

CLI = VisibilityClass( name = "cli",
                       default = __is_gui_host,
                       comment = "Commands best suited to the CLI." )

TEST = VisibilityClass( name = "test",
                        functional = False,
                        comment = "Commands for testing and debugging." )

INTERNAL = VisibilityClass( name = "internal",
                            functional = False,
                            comment = "Commands for use internally." )
