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


def do_the_breakdown(mode=None, visible=None, time=None):
    breakdown_dict = {}
    breakdown_dict['mode'] = mode
    breakdown_dict['visible'] = visible
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

        # Convert to absolute value
        transform_dict[transform_parent] = sum

    # Sort the transform dictionnary
    if mode in ["Bounding_box", "Top_to_the_bottom"]:
        sorted_geometry_dict = sorted(transform_dict.items(), key=operator.itemgetter(1), reverse=True)

    if mode in ["Bottom_to_the_top"]:
        sorted_geometry_dict = sorted(transform_dict.items(), key=operator.itemgetter(1))

    breakdown_dict['transform_lst'] = sorted_geometry_dict

    # Calculate frame range
    start_frame, end_frame = getFrameRange(time)
    breakdown_dict['frame_range'] = (start_frame, end_frame)
    dif_frame_range = end_frame - start_frame

    print("####### Initialize Processing  #######")
    compt = 0
    gap = float(dif_frame_range)/float(len(sorted_geometry_dict))
    for geometry, size_bounding_box in sorted_geometry_dict:
        compt += 1
        print("{0}/{1}".format(compt, len(sorted_geometry_dict)))
        if visible:
            attribute = "visibility"
            pmc.setKeyframe(geometry, attribute=attribute, value=0, time=start_frame)
            pmc.setKeyframe(geometry, attribute=attribute, value=1, time=gap * compt)
        else:
            # TODO: Choose direction (Z, Y, X axis)
            attribute = "translateY"
            offset = 1000
            breakdown_dict['offset'] = offset
            current_value = pmc.getAttr("{0}.{1}".format(geometry, attribute))
            # TODO: Choose the height (speed)
            pmc.setKeyframe(geometry, attribute=attribute, value=current_value + offset, time=start_frame)
            pmc.setKeyframe(geometry, attribute=attribute, value=current_value, time=gap*compt)

        breakdown_dict['attribute'] = attribute

    # Go back to the start frame
    pmc.currentTime(start_frame, edit=True)

    return breakdown_dict


def undo(dict):
    for geometry, value in dict['transform_lst']:
        print(geometry, value)
        pmc.cutKey(geometry, time=(dict['frame_range'][0], dict['frame_range'][1]), attribute=dict['attribute'], option="keys")
        if dict['visible']:
            pmc.setAttr("{0}.{1}".format(geometry, dict['attribute']), 1)
            sel = pmc.ls(geometry)[0]
            shape = sel.getShape()
            shape.setAttr(dict['attribute'], 1)
        else:
            pmc.setAttr("{0}.{1}".format(geometry, dict['attribute']), value)


