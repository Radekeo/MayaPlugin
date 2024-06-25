### Capture default rig data - Done
### Capture pose data
    - Identify and only store data from modified pose by comparing to default data- Done
    - Save captured data in JSON dump - Done
### Create directory to store pose data for each rig file - Done
    ***plugin will always load data for each project from it's unique directory
### Load Saved Poses
    - Read Data from json file and update controllers - Done('edge cases' found)
    - Handle exceptions such as 'locked controllers' which cannot be modified-Done
    - More tests and research to find more rig control issues
### Create UI
    - Connect existing functions (capture and load pose functions) to UI- Done
    - Save snapshots of poses and show snapshots in UI to help user select pose to load- Done

### Convert Project to Plugin
    
### Code Cleanup
    - Use classes- Done

### Plugin Functionality
    - Update pose while plugin is open - Done
    - Allow edits to be made while plugin is running- Done(maya mixin)
    - Add reset to default pose button - Done
    - Warning when conflicting poses are selected