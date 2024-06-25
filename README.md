# Maya Pose Manager Plugin

## Overview
The PoseManager Plugin is a Python-based plugin for Autodesk Maya that allows animators to store and manage key poses for their animation projects. This plugin enhances the animation pipeline by providing a convenient way to save and reuse key poses, improving efficiency and consistency in animation production.

## Features
- **Pose Data Management**: Capture, store, update, and combine multiple poses within the Maya scene.
- **Easy Access**: Quickly access and apply saved key poses through a user-friendly interface.
- **Screenshot Functionality**: Take screenshots of poses when captured, for easy viewing when user is ready to use the pose
- **Dockable GUI**: Easy-to-use, dockable interface within Maya..

## Installation
**1.Download the Project**: Clone the plugin repository or download the MayaPoseManagerPlugin containing the MayaPoseManager.mod, PoseManagerPlugin, PoseManager.py files

**2.Modify File Path**: Update the file path in MayaPoseManager.mod to the path on your system (use the pwd command to get the current directory).  

    + MayaPoseManager 1.0 /replace/with/your/pwd  
    
**3.Copy the MayaPoseManager.mod into your maya/modules folder**  

    cp MayaPoseManager.mod ~/maya/modules  
    

**4.Open Maya**: Once the file_path has been updated in the MayaPoseManager.mod and MayaPoseManager.mod has been copied into  the modules folder in maya, you can start your program and the plugin should appear in the plug-in manager

**5.Load Plugin**: In the Maya Plugin Manager window, find and load the PoseManager

## Usage
### Option 1: Run Plugin from Maya Editor
In the Maya script editor, enter and run the python code;  

    from PoseManager import PoseManager  
    
    pm = PoseManager()  
    
        
### Option 2: Create a Shelf and a Button to launch the Plugin
Create a shelf once and there would be no need to rerun the code  

    from PoseManager import PoseManagerShelf  
    
     shelf = PoseManagerShelf()  
     
     shelf.create_shelf()  
     

#### Steps
**Open a file in Maya containing your rig**  

**Start the plugin**; Once the plugin is started for the first time, it captures and stores your rig data as the default pose.  

**Modify your rig and capture key poses to be reused**  

**You can select and combine saved poses to use in your animation project**  


## Example
The plugin creates a default 'PoseManager' folder in the home directory when started and a subdirectory for each rig file is also created within the PoseManager. This allows the program to easily map a rig file to its stored data.  
    ```DEFAULT_FILE_PATH = {HOME_DIR}/PoseManager/{Rig_File_Name}```  

**Download the example folder in the repo and unzip so the folder is saved in your home directory. If you have the plugin installed and loaded in Maya, once you open the rig file in the example folder and start the plugin, you should get a window with the existing poses which can be loaded.** 
    
## Contact
For questions, feedback, or support, please contact Radeke(mailto:s5636764@bournemouth.ac.uk).

