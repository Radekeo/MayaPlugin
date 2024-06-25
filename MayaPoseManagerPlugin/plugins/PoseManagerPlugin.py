import maya.api.OpenMaya as om
import maya.cmds as cmds
from PoseManager import PoseManager

'''
def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass
'''

maya_useNewAPI = True
pose_manager_dialog = None


class PoseManagerImporter(om.MPxCommand):

    CMD_NAME = "PoseManagerImporter"

    def __init__(self):
        super(PoseManagerImporter, self).__init__()

    def doIt(self, args):
        pose_manager_dialog = PoseManager()
        

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return PoseManagerImporter()


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "PM"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(PoseManagerImporter.CMD_NAME, PoseManagerImporter.creator)
    except:
        om.MGlobal.displayError(
            "Failed to register command: {0}".format(PoseManagerImporter.CMD_NAME)
        )


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(PoseManagerImporter.CMD_NAME)
    except:
        om.MGlobal.displayError(
            "Failed to deregister command: {0}".format(PoseManagerImporter.CMD_NAME)
        )


if __name__ == "__main__":
    """
    So if we execute this in the script editor it will be a __main__ so we can put testing code etc here
    Loading the plugin will not run this
    As we are loading the plugin it needs to be in the plugin path.
    """

    plugin_name = "PoseManagerPlugin.py"

    cmds.evalDeferred(
        'if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(
            plugin_name
        )
    )
    cmds.evalDeferred(
        'if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(
            plugin_name
        )
    )