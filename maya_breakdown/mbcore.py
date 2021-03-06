import pymel.core as pmc
import operator
import math

def getFrameRange(time):
    frame_range = []
    start_frame = 0
    frame_range.append(start_frame)
    end_frame = time*25
    frame_range.append(end_frame)
    pmc.playbackOptions(minTime=start_frame, maxTime=end_frame, playbackSpeed=0, maxPlaybackSpeed=1, edit=True)
    return frame_range


def do_the_breakdown(setting_dictionnary, progressbar):
    # Get the user conditions
    selection = setting_dictionnary['selection']
    mode = setting_dictionnary['mode']
    visible = setting_dictionnary['visible']
    time = setting_dictionnary['time']
    attribute = setting_dictionnary['attribute']
    offset = setting_dictionnary['offset']
    axis_depth = setting_dictionnary['axis_depth']
    reverse_effect = setting_dictionnary['reverse_effect']

    # Create dict to save the position for the undo feature and another dict for make the breakdown
    transform_position_dict = {}
    transform_dict = {}

    # Get the selection
    list_to_parse = []
    if selection == "All":
        list_to_parse = pmc.ls(geometry=True)
    else:
        for selection in pmc.ls(selection=True):
            for children in pmc.listRelatives(selection, allDescendents=True):
                if pmc.nodeType(children) == "mesh":
                    list_to_parse.append(children)

    for transform in list_to_parse:
        # Get parent of the shape transform
        transform_parent = pmc.listRelatives(transform, parent=True)[0]
        sum = 0

        if mode in ["Bounding_box"]:
            for bounding_box in transform_parent.getBoundingBox():
                for bounding_box_value in bounding_box:
                    sum += abs(bounding_box_value)

        if mode in ["Top_to_bottom"]:
            # Get the worldspace position in terms of translate attribute
            sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[1]

        if mode in ["Depth"]:
            if axis_depth == "translateX":
                sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[0]
            if axis_depth=="translateZ":
                sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[2]


        # Get the transform position for the undo
        transform_position_dict[transform_parent.name()] = pmc.getAttr("{0}.{1}".format(transform_parent, attribute))
        transform_dict[transform_parent] = sum

    print(transform_dict)
    # Sort the transform dictionnary
    if mode in ["Bounding_box", "Top_to_bottom", "Depth"] and not reverse_effect:
        sorted_geometry_dict = sorted(transform_dict.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_geometry_dict)

    if mode in ["Bounding_box", "Top_to_bottom", "Depth"] and reverse_effect:
        sorted_geometry_dict = sorted(transform_dict.items(), key=operator.itemgetter(1))
        print(sorted_geometry_dict)

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

        # Unlock Attributes
        pmc.setAttr("{0}.{1}".format(geometry, attribute), lock=False)

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
        # Unlock Attributes
        pmc.setAttr("{0}.{1}".format(geometry, dict['attribute']), lock=False)
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


def get_current_cam():
    try:
        camera = pmc.PyNode(pmc.modelPanel(pmc.getPanel(withFocus=True), q=True, cam=True))
        return camera
    except RuntimeError:
        for current_camera in pmc.getPanel(visiblePanels=True):
            if "model" in current_camera:
                camera = pmc.modelPanel(current_camera, q=True, cam=True)
                return camera

def create_turn_around(dif_frame_range):
    pmc.warning("Feature in coming !")
