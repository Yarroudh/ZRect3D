<img src="https://user-images.githubusercontent.com/72500344/210864557-4078754f-86c1-4e7c-b291-73223bdf4e4d.png" alt="logo" width="200"/>

# Automatic correction of buildings ground floor elevation in 3D City Models
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

*Command-Line Interface (CLI) application to process and correct buildings ground floor elevation in CityJSON files using ground points from LiDAR data.*

The first image shows the results of 3D reconstruction of buildings using [GeoFlow3D](https://github.com/geoflow3d/geoflow-bundle), a tool for reconstructing 3D building models from point clouds, fully automated with high-detail. The software requires that the point cloud includes some ground points around the building so that it can determine the ground floor elevation. However, for aerial point clouds, buildings surrounded by others may not meet this condition which may result in inaccurate height estimation above the ground.

![image](https://user-images.githubusercontent.com/72500344/210857587-52af1135-eb92-4682-acd7-6499096a292f.png)

The second image shows the results of our automatic approach to correct buildings ground floor elevation using ground points from LiDAR data. The correction is based on K-nearest neighbors algorithm (KNN) to find the ground floor neighbors in the ground points of the LiDAR data. Thus, KDTree's structure is used for fast retrieval of nearest neighbors. The elevation is calculated by averaging the heights of these neighboring points. The height difference, which is the difference between the minimum Z-coordinate of the ground floor vertices and the calculated height on the ground, is finally applied to correct the Z-coordinate for all vertices of the ground surface.

![image](https://user-images.githubusercontent.com/72500344/210857677-d50e6768-cb15-4640-bcd3-c1445b61b15a.png)

## Installation

The easiest way to install <code>ZRect3D</code> on Windows is to use the binary package on the [Release page](). In case you can not use the Windows installer, or if you are using a different operating system, you can build everything from source.

## Usage of the CLI
After installation, you have a small program called <code>zrect</code>. Use <code>zrect --help</code> to see the detailed help:

```
  Usage: zrect [OPTIONS] CITYJSON POINTCLOUD [OUTPUT]

    Correct buildings ground floor elevation in a 3D city model [CityJSON] 
    using ground points from LiDAR data [LAS/LAZ/PCD/PLY].

  Options:
    -l, --lod TEXT          Specify the LoD to correct.  [default: 2.2]
    -d, --differences PATH  Export the list of height differences.  [default:
                            heights.json]

    -k, --knn INTEGER       K nearest neighbors of the lowest vertex to estimate
                            height.  [default: 2000]

    -t, --threshold FLOAT   Height difference threshold to perform the
                            correction.  [default: 0.1]

    --help                  Show this message and exit.
```

### Basic Usage

```
  zrect buildings.city.json pointcloud.las
```

This corrects the buildings ground floor elevation using the default configuration. The output consists of two files: the first one is named <code>output.city.json</code> which contains a copy of the input CityJSON file data with corrected ground floor elevation for LoD2.2 buildings, and the second one is <code>heights.json</code> which contains the height differences for all the buildings in the 3D city model.

### Using Options

```
  zrect buildings.city.json pointcloud.las corrected_buildings.city.json -l '1.3' -k 1000 -t 0.05 -d height_list.json
```

In this example, we correct the LoD1.3 buildings ground floor elevation using 1000 neighboring points from the LiDAR data to estimate height and a threshold of 0.05 meters to apply correction. The CityJSON file in output is named <code>corrected_buildings.city.json</code> and the list of height differences is <code>height_list.json</code>

## Supported CityJSON versions

The application expects that your file is using the latest version [CityJSON schema](https://www.cityjson.org/specs/1.1.3/). If your file uses an earlier version, you can upgrade it with the upgrade operator of [cjio, CityJSON/io](https://github.com/cityjson/cjio): <code>cjio old.json upgrade save newfile.city.json</code>

Alternatively, any CityGML file can be automatically converted to CityJSON with the open-source project [citygml-tools](https://github.com/citygml4j/citygml-tools).

## Requirements on the Point Cloud

* Classified, with at least a *ground* class (scalar field named *classification* with value 2 for all ground points).
* Well aligned with the 3D Building Model.
* Supported formats: <code>.LAS</code>, <code>.LAZ</code>, <code>.PCD</code> and <code>.PLY</code>.

## About ZRect3D

This software was developped by Anass Yarroudh, a Research Engineer in the [Geomatics Unit of the University of Liege](http://geomatics.ulg.ac.be/fr/home.php).

For more detailed information please contact us via <ayarroudh@uliege.be>, we are pleased to send you the necessary information.
