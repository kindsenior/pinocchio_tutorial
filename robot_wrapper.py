import numpy as np
import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer, GepettoVisualizer

# add a frames and XYZaxis
def add_fixed_frame_with_axis(self, name, parent_joint_name,
                              offset_pos=(0,0,0), offset_rpy=(0,0,0),
                              axis_radius=0.01, axis_size=0.05):
    # add a frame
    parent_id  = self.model.getJointId(parent_joint_name)
    local_offset  = pin.SE3(pin.rpy.rpyToMatrix(*offset_rpy), np.array(offset_pos))
    frame_id = self.model.addFrame(pin.Frame(name, parent_id, local_offset, pin.FrameType.FIXED_JOINT))
    self.rebuildData()

    # add an XYZaxis
    if name not in getattr(self, "_axis_nodes", {}):
        node_name = f"world/{name}"
        self.viewer.gui.addXYZaxis(node_name, [1., 0., 0., 1.], axis_radius, axis_size)

        self._axis_nodes = getattr(self, "_axis_nodes", {})
        self._axis_nodes[frame_id] = node_name
    return frame_id

# FK + frameFK + update frames
def display_with_frames(self, q):
    # pin.forwardKinematics(self.model, self.data, q)
    ## update viz.data and viz.visual_data for visualizing
    ## data and visual_data are different b/w robot and viz
    # pin.forwardKinematics(self.model, self.viz.data, q)
    # pin.updateGeometryPlacements(self.model, self.viz.data, self.viz.visual_model, self.viz.visual_data)
    # self.viz.display()
    self.display(q)
    self.framesForwardKinematics(q)

    for frame_id, node_name in getattr(self, "_axis_nodes", {}).items():
        print(f"node_name: {node_name}")
        self.viewer.gui.applyConfiguration(node_name, pin.SE3ToXYZQUATtuple(self.data.oMf[frame_id]))
    self.viewer.gui.refresh()

# monkey-patch to RobotWrapper
from pinocchio.robot_wrapper import RobotWrapper
# add method after import
RobotWrapper.add_fixed_frame_with_axis = add_fixed_frame_with_axis
RobotWrapper.display_with_frames       = display_with_frames

