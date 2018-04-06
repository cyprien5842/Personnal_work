import pymel.core as pmc
import operator


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
            # Get the worldspace position of translateY value
            sum = pmc.xform(transform_parent, query=True, worldSpace=True, rotatePivot=True)[1]

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
    start_frame, end_frame = getFrameRange(time)
    setting_dictionnary['frame_range'] = (start_frame, end_frame)
    dif_frame_range = end_frame - start_frame

    # Do the operation
    compt = 0
    gap = float(dif_frame_range)/float(len(sorted_geometry_dict))
    for geometry, size_bounding_box in sorted_geometry_dict:
        compt += 1
        if visible:
            pmc.setKeyframe(geometry, attribute=attribute, value=0, time=start_frame)
            pmc.setKeyframe(geometry, attribute=attribute, value=1, time=gap * compt)
        else:
            # TODO: Choose direction (Z, Y, X axis)
            current_value = pmc.getAttr("{0}.{1}".format(geometry, attribute))
            # TODO: Choose the height (speed)
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


