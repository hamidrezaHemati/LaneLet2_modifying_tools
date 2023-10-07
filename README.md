# LaneLet2_ID_Mapping
Changing Tag ID's of a poorly made LL2 file to be able to use it on Autoware simulator

## Problem Definition
We had a lanelet2 file of a city in Japan and we wanted to use that as a main map to improve planning and mapping algorithms. But, the LaneLet2 map had some unknown problems which made it impossible to run it on Autoware simulator.  
#### After spending a lot of time and energy, we came to the conclusion that one of the main problems of this file is its used id's.


## LaneLet2 Definition and structure
Lanelet2 is an extended version of the OpenStreetMap (OSM) format, the extension is osm, and it becomes xml when exported to a file. Lanelet2 consists of the following basic objects and is divided into three types, namely node, way, and relation, according to OSM at the time of export. The following shows the description of each basic object, samples of exported files, and examples of displayed images in VMB.

Lanelet2 is a software library and data format designed for representing and working with high-definition maps for autonomous driving and other applications in the field of robotics. It provides a structured and standardized way to describe road networks, including lane geometries, traffic signs, traffic lights, and other relevant information.

## Primitives
Lanelet2 divides the world into a **hierarchical structure** of six different primitives: **Points**, **Line strings**, **polygons**, **Lanelets**, **Areas** and **regulatory elements**. [source](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletAndAreaTagging.md#subtype-and-location)

All elements have in common that they are identified by a unique ID (this is useful for an efficient construction of the topological layer) and that attributes in the form of key-value pairs can be assigned to them. Some of these attributes are fixed, but additional attributes can be used to enhance the map. [Source IV, A](https://www.mrt.kit.edu/z/publ/download/2018/Poggenhans2018Lanelet2.pdf)

pictures below shows the **hierarchical structure** of lanelet2.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/fb007745-5cce-492d-8240-876563314b8b/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/76b6a73d-ae4c-4cc9-a1cd-19edbb326a8b/Untitled.png)

**Points**: A point consists of an ID, a 3d coordinate and attributes. Points are no meaningful objects. Points are only meaningful together with other objects in Lanelet2. The only situation where individual points are important is when tagging start and end points of a dashed line marking.

**lineStrings**: Linestrings (also known as polylines or formerly linestrips) are defined by an ordered list of points with linear interpolation in between. They are the basic building block of a Lanelet map and used for any physically observable part of the map. [source](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a03e8044-89bc-47ac-aa15-e8f0eebbc252/Untitled.png)

**Polygon:** Polygons, are rarely used to transport mapping information (except for e.g. traffic signs). Instead, they often serve as a means to add customized information about an area to the map (e.g. a region of interest).

**Lanelet:** A Lanelet consists of exactly one left and exactly one right Linestring. Together they form the drivable area of the Lanelet. [source](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a6b80791-1f85-47f0-b1b8-fd4ff6c391ce/Untitled.png)

**Area**: An Area has similar properties like a Lanelet, but instead of representing directed traffic from entry to exit, an Area represents undirected traffic within its surface. An Area can have multiple entry and exit points. A typical example of an Area would be squares that are used by pedestrians or parking lots and emergency lanes for vehicles. Similar to Lanelets, traffic rules must not change on the areas. [source](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f8624ecf-a5f6-4146-9123-8f4a5a26d965/Untitled.png)

**Regulatory Elements:** Regulatory elements are a generic way to express traffic rules. They are referenced by Lanelets or areas for which they apply.

- *traffic_sign*
- *traffic_light*
- *speed_limit*
- *right_of_way*
- *all_way_stop*

In general, regulatory elements consist of tags that generally express the type of the rule (i.e. a traffic light regulatory element) and specific information about the observable things that have a certain role for this rule (e.g. the traffic light itself and the stop line). Other types of regulatory elements are right of way and traffic sign regulatory elements [source](https://github.com/fzi-forschungszentrum-informatik/Lanelet2/blob/master/lanelet2_core/doc/LaneletPrimitives.md)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a778d117-96d6-41ef-b427-911431623321/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a575ff91-3276-4e70-8263-57597dbb1cad/Untitled.png)

## LL2 file

- **format and tags**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b062bc3d-7fcd-4d0c-ac8c-ce907595ad0f/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8053180f-1583-41b9-8ef4-bce351abfb19/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5283035d-bea8-4fb1-9a66-ff1e541e83ee/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d29d77e2-d1b8-4dc4-93b5-519f6af3cd7b/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7f5a585a-5baf-47c6-a149-64fa8136e5bd/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/679b3343-acc2-427f-b70d-d730cf24a801/Untitled.png)
    
- **Header**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/333f5e46-b4b7-4171-a813-7904c2b34d30/Untitled.png)
    
- **Point**
    - Basic object which has the coordinate, the color information of a signal, etc.
    - It is classified into node of OSM. The z coordinate is displayed with the tag, ele.
    - To use a local coordinate, you can set the tags, local_x and local_y.
    - lat/lon is latitude/longitude and the unit of local_x, local_y, and ele is meter.
    
    ```xml
    <node id="1" lat="35.0000" lon="139.0000"><tag k="ele" v="19.546"/></node>
    ```
    
    !https://contents.docs.web.auto/en/user-manuals/vector-map-builder/introduction/assets/point.jpg
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e38cb0d7-65a1-4616-90e0-41a61b5afcac/Untitled.png)
    
- **Line string**
    - Object connecting the list of Points with lines in order. You can make up Lanelet by using two Linestrings or use Linestring for a traffic light or stop line.
    - It is classified ino way of OSM.
    - It has Point of a component with the nd tag.
    - You can represent a stop line and a dashed line by setting type to stop-line and subtype to dashed, respectively. You can apply various settings by changing the tag type: for example, if you change Linestring of the boundary of Lanelet to dashed, it is possible to change lanes into the adjacent Lanelet.
    
    ```xml
    <way id="1">
    	<nd ref="1"/>
    	<nd ref="2"/>
    	<nd ref="3"/>
    	<nd ref="4"/>
    	<tag k="type" v="line_thin"/>
    	<tag k="subtype" v="solid"/>
    </way>
    ```
    
    !https://contents.docs.web.auto/en/user-manuals/vector-map-builder/introduction/assets/linestring.jpg
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/39a7436f-4915-45ed-aabd-c217ac3f7f0c/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5d62e175-a5c0-4c9a-ab1a-783f722780d7/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cedee9fe-7863-4e8b-84fb-d70a933d7da8/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a12af426-5180-417f-a2e9-f5d332f685d0/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c2ee2504-dd5a-431b-9df5-c47d80036085/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/481d3264-97d9-4417-9413-ecb081a0150d/Untitled.png)
    
- **Polygon**
    - It represents an area surrounded by Points. It is used in DetectionArea, which represents an obstacle detection area, etc.
    - It is classified into way of OSM with the tag, area=yes.
    
    ```xml
    <way id="1">
    	<nd ref="1"/>
    	<nd ref="2"/>
    	<nd ref="3"/>
    	<nd ref="4"/>
    	<tag k="type" v="detection_area"/>
    	<tag k="area" v="yes"/>
    </way>
    ```
    
    !https://contents.docs.web.auto/en/user-manuals/vector-map-builder/introduction/assets/polygon.jpg
    
- **Lane lets**
    - It has one Linestring to right and left, respectively, and represents the area between them. It has a direction and is used for a lane, a crosswalk, etc.
    - It is classified into relation of OSM with the tag, type=lanelet.
    - It has the right and left Linestring as members.
    - If there are traffic rules (RegulatoryElement) which have to be observed on that lane, it has them as members.
    - It has information regarding the speed limit, traffic targets (vehicles, pedestrians, etc.), a one-way road, etc.
    
    ```xml
    <relation id="1">
    	<member type="way" role="left" ref="1"/>
    	<member type="way" role="right" ref="2"/>
    	<member type="relation" role="regulatory_element" ref="2"/>
    	<tag k="type" v="lanelet"/>
    	<tag k="subtype" v="road"/>
    	<tag k="speed_limit" v="50"/>
    	<tag k="location" v="urban"/>
    	<tag k="participant:vehicle" v="yes"/>
    	<tag k="one_way" v="yes"/>
    </relation>
    ```
    
    !https://contents.docs.web.auto/en/user-manuals/vector-map-builder/introduction/assets/lanelet.jpg
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/86d5182c-71e7-4980-8906-8ca4243006a6/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/926e61a2-b5a9-4172-a6b5-a253aed78d1b/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/536e43fd-d65a-448f-87a9-3a79c3430a2e/Untitled.png)
    
- **Area**
    - It represents an area surrounded by Linestrings. It is often used to represent traffic areas of vehicles and people but has no direction unlike Lanelet.
    - It is classified into relation of OSM with the tag, type=multipolygon.
    - It has the components, Linestrings, as members in a clockwise fashion.
    
    ```xml
    <relation id="1">
    	<member type="way" role="outer" ref="1"/>
    	<member type="way" role="outer" ref="2"/>
    	<tag k="type" v="multipolygon"/>
    </relation>
    ```
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6312b278-645a-46d0-a608-0a0b952e6a87/Untitled.png)
    
- **Regulatory Elements**
    
    Regulatory Elements are divided into categories. The most common ones are `TrafficLight`, `TrafficSign`, `SpeedLimit` and `RightOfWay`, which are already included in the core library, but there are many more ways to model restrictions on lanelets and areas. More might be added in the future and also users are able to add own regulatory elements by inheriting from the generic `RegulatoryElement` class and registering the new type using the `RegisterRegulatoryElement` class.
    
    This document describes the generic layout of a Regulatory Element and shows how the common Regulatory Elements are structured.
    
    ## Tags
    
    Regulatory Elements always have `type=regulatory_element`. If this tag is not present, Lanelet2 will add it when writing to an .osm file.
    
    ### Subtype
    
    The `subtype` tag helps Lanelet2 to distinguish between the different regulatory elements. For the basic Regulatory Elements this would be:
    
    - *traffic_sign*
    - *traffic_light*
    - *speed_limit*
    - *right_of_way*
    - *all_way_stop*
    
    ### Other, Optional Tags
    
    The following tags can be used to add more information to a Regulatory Element (of course you can add you own to enhance your map and implement a new `TrafficRule` object that implements them). The default values for the tag are highlighted.
    
    - *dynamic* (yes/**no**): Indicates that this Regulatory Element might change its meaning based on a condition. Examples would be a road that is closed on weekends. Or a speed limit that is only in action if the road is wet. By default, Lanelet2 cannot handle dynamic Regulatory Elements and will ignore them. Specialized traffic rule classes could be implemented that use background information (such as the current time) to resolve dynamic Regulatory Elements.
    - *fallback* (yes/**no**): Indicates that this Regulatory Element has a lower priority than another Regulatory Element. Examples are right of way regulations that become valid if the traffic lights of an intersection are out of order.
    
    ## Parameters
    
    The main feature of a Regulatory Element is that it can reference other parts of the map that are important for the traffic restriction that they represent. These parts are called *parameters* of a Regulatory Element. Every parameter is characterized by a role (a string) that explains what he expresses within the Regulatory Element. Multiple parameters can have the same role if they do not contradict.
    
    An example of parameters are the traffic lights that referenced by the *refers* role of a `TrafficLight` Regulatory Element. These are the traffic lights that a vehicle has to pay attention to when driving along a specific lanelet/area that has this Regulatory Elements. Because parameters with the same role cannot contradict, this means all traffic lights must refer to the same driving direction within that intersection.
    
    The most common roles that are used across all regulatory elements are:
    
    - *refers*: The primitive(s) that are the very origin of the restriction. Traffic lights/signs, et cetera. Most Regulatory Elements need a *refers* role.
    - *cancels*: The primitive(s) that mark the end of the restriction (if applicable).
    - *ref_line*: The line (usually a LineString) from which a restrictions becomes valid. If not used, that usually means that the whole lanelet/area is affected by the restriction. However, there are exceptions, e.g. for traffic lights the stop line is the *end* of the lanelet.
    - *cancel_line*: The line (usally a LineString) from which a restriction is no longer in place (if applicable)
    
    ## Basic Regulatory Elements
    
    ### Traffic Sign
    
    A traffic sign generically expresses a restriction that is expressed by a traffic sign. The *refers* part refers to traffic signs that form the rule. The *cancels* parameter then refers to traffic signs that mark the end of the restriction expressed by the sign (e.g. the end of no-overtaking section). The *ref_line* and *cancel_line* parameters can then be used to define the exact start and end points of the rule. The LineStrings referenced by that do not necessarily need to have an intersection with the referencing lanelet or Area. If they do, the rule is valid from/to this intersection point. If not, the rule is valid for the whole lanelet/area.
    
    ### Speed Limit
    
    Speed limits work very similar to traffic signs. If they are put up by a traffic sign, they simply reference this traffic sign. Similar for the *ref_line* and the *cancels* role. The `TrafficRules` class then takes care of interpreting the speed limit from the `subtype` of the referenced traffic sign.
    
    Alternatively, if the speed limit does not originate from a traffic sign, a `sign_type` tag can be used to define the speed limit. The value should contain the unit, eg "50 km/h". mph or mps or similar units are possible as well. If no unit is given, km/h is assumed.
    
    ### Traffic Light
    
    Traffic lights are also similar to traffic signs. Instead of a sign, the light itself is referenced as *refers* parameter. The *cancels* and *cancels_line* role have no meaning for traffic lights. The *ref_line* can reference the respective stop line. If they are not present, the stop line is implicitly at the end of the lanelet or Area.
    
    ### Right of Way
    
    By default, intersecting lanelets are treated as a "first come first served" situation, meaning that the vehicle that arrives first at the intersection point has right of way. The `RightOfWay` Regulatory Element changes this. It has three roles:
    
    - *yield*: References the lanelets that have to yield
    - *right_of_way*: the lanelets that have the right of way over the yielding ones
    - *ref_line*: The lines where vehicles that are crossing a *yield* lanelet have to stop at. If not set, this is the end of the *yield* lanelet.
    
    Only one lanelet of a chain of lanelets that belong to the same lane have to be referenced. Generally this is the last lanelet that can be undoubtedly assigned to one specific intersection arm (i.e. the last lanelet before the intersection begins). All lanelets that are mentioned by the right of way Regulatory Element also have to reference the regulatory element.
    
    ### All Way Stop
    
    While in a *Right of Way* regelem, the right of way only depends on the lanelet, the right of way in an [All-Way Stop](https://en.wikipedia.org/wiki/All-way_stop) regelem depends on the order of arrival and the route through the intersection. Therefore, all lanelets are potentially yield lanelets. All approaching vehicles have to stop before entering the intersection. The intersection entry is either defined by one stop line for each lanelet or is otherwise determined by the end of each lanelet. To avoid confusion when matching lanelets and stop lines, an *All Way Stop* regelem is only valid if either no lanelet has a stop line or all lanelets have exactly one. The following roles are used in an all way stop:
    
    - *yield*: References the lanelets that might have to yield
    - *ref_line*: The lines where *yield* lanelets have to stop. This either empty or has the same order and size as the number of lanelets in *yield*.
    - *refers*: The traffic sign(s) that constitute this rule
    
    All lanelets referenced in this regelem also have to reference this regelem.
    
    ---
    
    ```xml
    <relation id="1">
    	<member type="way" role="refers" ref="1"/>
    	<member type="way" role="light_bulbs" ref="2"/>
    	<member type="way" role="ref_line" ref="3"/>
    	<tag k="type" v="regulatory_element"/>
    	<tag k="subtype" v="traffic_light"/>
    </relation>
    ```
    
    RegulatoryElement has a different number and types of members depending on the rule type. The following description is an example of the traffic light described in the sample. There are three members of a traffic light: `refers(mandatory)`, `ref_line(optional)`, and `light_bulbs(optional)`. Each type is way, so it represents Linestring or Polygon but all traffic lights are associated with Linestrings. Firstly, refers represents the outline of a traffic light. If it is exported to a file, it becomes way with id 1 as in the following example; 2 and 3 in nd indicate the width of a traffic light, and the height-tag indicates the height.
    
    ```xml
    <way id="1">
    	<nd ref="2"/>
    	<nd ref="3"/>
    	<tag k="type" v="traffic_light"/>
    	<tag k="height" v="0.450000"/>
    </way>
    ```
    
    !https://contents.docs.web.auto/en/user-manuals/vector-map-builder/introduction/assets/traffic_light.jpg
    
    Next, as for light_bulbs, it becomes way with id 2 as in the following example and traffic_light_id indicates the id of the Linestring of the outline of the traffic light. 4 to 6 in nd indicate Points and each color tag has the color information of the traffic light. (red, yellow, and green in the case of the traffic light in the image)
    
    ```xml
    <way id="2">
    	<nd ref="4"/>
    	<nd ref="5"/>
    	<nd ref="6"/>
    	<tag k="type" v="light_bulbs"/>
    	<tag k="traffic_light_id" v="1"/>
    </way>
    <node id="4" lat="35.0000" lon="139.0000">
    	<tag k="ele" v="19.546"/>
    	<tag k="color" v="red"/>
    </node>
    ```
    
    Finally, since ref_line represents the stop line when the traffic light is red, set stop_line to type as in the following way.
    
    ```xml
    <way id="3">
    	<nd ref="7"/>
    	<nd ref="8"/>
    	<tag k="type" v="stop_line"/>
    </way>
    ```
    
    ---
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/32db5788-b568-4a36-ab86-26dafcd08788/Untitled.png)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0e4a6d2d-0bac-43d4-823b-f24a470ec41c/Untitled.png)