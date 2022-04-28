# Generate Grasp Regions

## Requirements:
* Blender (tested on 2.93 and 3.1)
    - Install blender on linux with the following:
    ```console
    sudo snap install blender --classic
    ```
    - After installing blender it is useful to add a shortcut in .bashrc that allows you to use "blender" instead of the full path to the executable.



## Run Code:

* Use the grasp_region.json (also at the bottom) as a template to create the json with the hand measurements for a gripper.

    - Measurments should be put in meters (blender defaults to meters for meshes).

* To generate the grasp region meshes run:

    ```console
    blender -b --python visualize_grasp_region.py <name_of_json>.json
    ```

    - This will create a directory named after the hand_name, containing all of the .obj meshes that represent the grasp region for that hand.


## Below is the reference json for the hand measurements (grasp_region.json):
* Span, depth, and width should all be floats in meters. 

``` JSON
{
    "gripper_name": "hand_name",
    "grasp_style": "cylindrical/spherical",
    "power" : {
        "max" : [["base_span", "base_depth"], ["mid_span", "mid_depth"], ["distal_span", "distal_depth"]],
        "int" : [["base_span", "base_depth"], ["mid_span", "mid_depth"], ["distal_span", "distal_depth"]],
        "min" : [["base_span", "base_depth"], ["mid_span", "mid_depth"], ["distal_span", "distal_depth"]],
        "width" : ["min_width", "max_width"]
    },
    "precision": {
        "max" : [["base_span", "base_depth"], ["mid_span", "mid_depth"], ["distal_span", "distal_depth"]],
        "int" : [["base_span", "base_depth"], ["mid_span", "mid_depth"], ["distal_span", "distal_depth"]],
        "min" : [["base_span", "base_depth"], ["mid_span", "mid_depth"], ["distal_span", "distal_depth"]],
        "abs_max" : ["span", "depth"],
        "width" : ["min_width", "max_width"]
    }
}
```
