# Maya_breakdown
This is a script which allow to make an easy breakdown for your showreel.
This script is currently use at <a href="http://www.artfx.fr/en/">ArtFx</a>

# 1.] How to setup the plugin ? 

It's easy ! 
Create a python shelf in Maya with the next script.


    import sys
    sys.path.append("C:/your_path/maya_breakdown")
    import mbui
    mbui.show_window()
