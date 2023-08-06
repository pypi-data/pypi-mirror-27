"""
Creates and registers additional UI editors.
"""
import editorium
    
    
def __register():
    from neocommand.extensions.hosts.gui_editorium_extensions import Editor_SpecialString
    return Editor_SpecialString


editorium.register( __register )
