import pymel.core as pmc
import operator
import math

def getFrameRange(time):
    frame_range = []
    # TODO: Use current frame range
    #start_frame = int(pmc.playbackOptions(animationStartTime=True, query=True))
    #end_frame = int(pmc.playbackOptions(animationEndTime=True, query=True))
    start_frame = 0
    frame_range.append(start_frame)
    # TODO: Choose FPS
    end_frame = time*25
    frame_range.append(end_frame)
    pmc.playbackOptions(minTime=start_frame, maxTime=end_frame, playbackSpeed=0, maxPlaybackSpeed=1, edit=True)
    return frame_range


def do_the_breakdown(setting_dictionnary, progressbar):
    # Get the user conditions
    mode = setting_dictionnary['mode']
    visible = setting_dictionnary['visible']
    time = setting_dictionnary['time']
    attribute = setting_dictionnary['attribute']
    offset = setting_dictionnary['offset']

    # Create dict to save the position for the undo feature and another dict for make the breakdown
    transform_position_dict = {}
    transform_dict = {}

    for transform in pmc.ls(geometry=True):
        # Get parent of the shape transform
        transform_parent = pmc.listRelatives(transform, parent=True)[0]
        sum = 0

        if mode in ["Bounding_box"]:
            for bounding_box in transform_parent.getBoundingBox():
                for bounding_box_value in bounding_box:
                    sum += abs(bounding_box_value)

        if mode in ["Top_to_the_bottom", "Bottom_to_the_top"]:
            # Get the worldspace position in terms of translate attribute
            if attribute == "translateX":
                sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[0]
            if attribute == "translateY":
                sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[1]
            if attribute == "translateZ":
                sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[2]

        # Get the transform position
        transform_position_dict[transform_parent.name()] = pmc.getAttr("{0}.{1}".format(transform_parent, attribute))
        transform_dict[transform_parent] = sum

    # Sort the transform dictionnary
    if mode in ["Bounding_box", "Top_to_the_bottom"]:
        sorted_geometry_dict = sorted(transform_dict.items(), key=operator.itemgetter(1), reverse=True)

    if mode in ["Bottom_to_the_top"]:
        sorted_geometry_dict = sorted(transform_dict.items(), key=operator.itemgetter(1))

    setting_dictionnary['transform_lst'] = sorted(transform_position_dict.items(), key=operator.itemgetter(1))

    # Calculate frame range
    if isinstance(time, tuple):
        start_frame, end_frame = time
        setting_dictionnary['frame_range'] = time
    else:
        start_frame, end_frame = getFrameRange(time)
        setting_dictionnary['frame_range'] = (start_frame, end_frame)
    dif_frame_range = end_frame - start_frame

    if setting_dictionnary['camera']:
        create_turn_around(dif_frame_range)

    # Do the operation
    compt = 0
    gap = float(dif_frame_range)/float(len(sorted_geometry_dict))
    for geometry, size_bounding_box in sorted_geometry_dict:
        compt += 1
        if visible:
            pmc.setKeyframe(geometry, attribute=attribute, value=0, time=start_frame)
            pmc.setKeyframe(geometry, attribute=attribute, value=1, time=gap * compt)
        else:
            current_value = pmc.getAttr("{0}.{1}".format(geometry, attribute))
            pmc.setKeyframe(geometry, attribute=attribute, value=current_value + offset, time=start_frame)
            pmc.setKeyframe(geometry, attribute=attribute, value=current_value, time=gap*compt)
        progressbar.setValue((compt * 100) / int(len(sorted_geometry_dict)))

    # Go back to the start frame
    pmc.currentTime(start_frame, edit=True)

    return setting_dictionnary


def undo(dict, progressbar):
    compt = 0
    for geometry, value in dict['transform_lst']:
        compt += 1
        # Remove the keys
        pmc.cutKey(geometry, time=(dict['frame_range'][0], dict['frame_range'][1]), attribute=dict['attribute'], option="keys")
        if dict['visible']:
            pmc.setAttr("{0}.{1}".format(geometry, dict['attribute']), 1)
            sel = pmc.ls(geometry)[0]
            shape = sel.getShape()
            shape.setAttr(dict['attribute'], 1)
        else:
            pmc.setAttr("{0}.{1}".format(geometry, dict['attribute']), value)
        progressbar.setValue((compt * 100) / int(len(dict['transform_lst'])))


def create_turn_around(dif_frame_range):
    # # Function to set the camera translates in order to set a dynamically scale
    # camera_name = 'CAM_TURN_AROUND'
    #
    # # Get the gap for front, left, bottom and right camera movement
    # gap = dif_frame_range/4
    #
    # # Use the infinity value
    # top = -float("inf")
    # bottom = float("inf")
    # right = -float("inf")
    # left = float("inf")
    # near = -float("inf")
    # depth = float("inf")
    #
    # if not camera_name in str(pmc.ls(cameras=True)):
    #     cam = pmc.createNode('camera', name=camera_name+"_shape")
    #     cam_parent = cam.getParent()
    #     cam_parent.rename(camera_name)
    #
    #     # Get the extreme value in order to create camera
    #     for transform in pmc.ls(geometry=True):
    #         # Get parent of the shape transform
    #         transform_parent = pmc.listRelatives(transform, parent=True)[0]
    #
    #         right_value = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[0]
    #         if right < right_value:
    #             right = right_value
    #
    #         left_value = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[0]
    #         if left > left_value:
    #             left = left_value
    #
    #         top_value = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[1]
    #         if top < top_value:
    #             top = top_value
    #
    #         bottom_value = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[1]
    #         if bottom > bottom_value:
    #             bottom = bottom_value
    #
    #         near_value = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[2]
    #         if near < near_value:
    #             near = near_value
    #
    #         depth_value = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[2]
    #         if depth > depth_value:
    #             depth = depth_value
    #
    #     # Get the averages values
    #     average_top_bottom = (top+bottom)/2
    #     average_left_right = (left+right)/2
    #     average_depth_near = (depth+near)/2
    #
    #     print("top :" + str(top))
    #     print("bottom :" + str(bottom))
    #     print("right :" + str(right))
    #     print("left :" + str(left))
    #     print("near :" + str(near))
    #     print("depth :" + str(depth))
    #     print("average_top_bottom :" + str(average_top_bottom))
    #     print("average_left_right :" + str(average_left_right))
    #     print("average_depth_near :" + str(average_depth_near))
    #
    #     # First camera movement
    #     pmc.setKeyframe(cam_parent, attribute="translateX", value=right, time=gap * 0)
    #     pmc.setKeyframe(cam_parent, attribute="translateY", value=average_top_bottom, time=gap * 0)
    #     pmc.setKeyframe(cam_parent, attribute="translateZ", value=average_depth_near, time=gap * 0)
    #     pmc.setKeyframe(cam_parent, attribute="rotateY", value=-260, time=gap * 0)
    #
    #     # Second camera movement
    #     pmc.setKeyframe(cam_parent, attribute="translateX", value=average_left_right, time=gap * 1)
    #     pmc.setKeyframe(cam_parent, attribute="translateY", value=average_top_bottom, time=gap * 1)
    #     pmc.setKeyframe(cam_parent, attribute="translateZ", value=depth, time=gap * 1)
    #     pmc.setKeyframe(cam_parent, attribute="rotateY", value=-180, time=gap * 1)
    #
    #     # Third camera movement
    #     pmc.setKeyframe(cam_parent, attribute="translateX", value=left, time=gap * 2)
    #     pmc.setKeyframe(cam_parent, attribute="translateY", value=average_top_bottom, time=gap * 2)
    #     pmc.setKeyframe(cam_parent, attribute="translateZ", value=average_depth_near, time=gap * 2)
    #     pmc.setKeyframe(cam_parent, attribute="rotateY", value=-90, time=gap * 2)
    #
    #     # Fourth camera movement
    #     pmc.setKeyframe(cam_parent, attribute="translateX", value=left, time=gap * 3)
    #     pmc.setKeyframe(cam_parent, attribute="translateY", value=average_top_bottom, time=gap * 3)
    #     pmc.setKeyframe(cam_parent, attribute="translateZ", value=near, time=gap * 3)
    #     pmc.setKeyframe(cam_parent, attribute="rotateY", value=0, time=gap * 3)
    #
    #     # Fifth camera movement
    #     pmc.setKeyframe(cam_parent, attribute="translateX", value=right, time=gap * 4)
    #     pmc.setKeyframe(cam_parent, attribute="translateY", value=average_top_bottom, time=gap * 4)
    #     pmc.setKeyframe(cam_parent, attribute="translateZ", value=average_depth_near, time=gap * 4)
    #     pmc.setKeyframe(cam_parent, attribute="rotateY", value=90, time=gap * 4)
    #
    # else:
    pmc.warning("Feature in coming !")
