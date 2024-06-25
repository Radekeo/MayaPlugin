import unittest
import os
import json

TEST_DIR = os.path.join(os.path.expanduser('~'), 'TEST')

class PoseManagerInitializationTest(unittest.TestCase):
    def setUp(self):
        # Set up the Maya scene with some dummy rig controllers
        self.ctrl1 = cmds.circle(name='ctrl1')[0]
        self.ctrl2 = cmds.circle(name='ctrl2')[0]

    def test_pose_manager_initialization(self):
        expected_rig_controllers = [self.ctrl1, self.ctrl2]
        pose_manager = PoseManager()
        self.assertEqual(pose_manager.nurbs, expected_rig_controllers)

class PluginStarterTest(unittest.TestCase):
    def test_plugin_start_up(self):
        # Arrange
        pose_manager = PoseManager()

        # Call the function to start the plugin
        pose_manager.startPlugin()

        # Check if the JSON file is created with default data
        default_pose_data_path = os.path.join(TEST_DIR, 'DEFAULT.json')
        self.assertTrue(os.path.exists(default_pose_data_path))
        
        # Read the JSON file and check its content
        with open(default_pose_data_path, 'r') as file:
            default_pose_data = json.load(file)

        self.assertIsInstance(default_pose_data, dict)
        self.assertEqual(len(default_pose_data), 0)

class PoseManager:
    def __init__(self) -> None:
        # Get rig controllers in the scene
        self.nurbs = [nurb[:-5] for nurb in cmds.ls(type=['nurbsCurve'])]

    def startPlugin(self):
        if not os.path.exists(os.path.join(TEST_DIR, 'DEFAULT.json')): 
            self.addJSONToDir('DEFAULT.json')

    def addJSONToDir(self, file_name):
        self.pose_data = {}
        file_path = os.path.join(TEST_DIR, file_name)
        for nurb in self.nurbs:
            try:
                data = self.getPoseData(nurb)
                self.pose_data[nurb] = {'translation': data[0], 'rotation': data[1]}
            except:
                continue

        if os.path.exists(TEST_DIR):
            with open(self.default_pose_data_path, 'r') as file:
                default_pose = json.load(file)

            for controller in default_pose:
                if self.pose_data[controller]:
                    if default_pose[controller] == self.pose_data[controller]:
                        del self.pose_data[controller]   
        else:
            os.makedirs(TEST_DIR)
        
        self.writeToJSON(file_path, self.pose_data)

    def writeToJSON(self,file_dir, data):
        with open(file_dir, 'w') as file:
            try:
                json.dump(data, file)
                print('done')
            except:
                print('not done')

if __name__ == '__main__':
    unittest.main()