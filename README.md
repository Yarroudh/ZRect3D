# Automatic correction of buildings height in 3D City Models
Command-Line Interface (CLI) application to process and correct buildings height in CityJSON files using ground points from LiDAR data.

The first image shows the results of 3D Reconstruction using [GeoFlow3D](https://github.com/geoflow3d/geoflow-bundle), A tool for reconstructing 3D building models from point clouds, fully automated, with high-detail. Free and open-source. The software requires that the point cloud includes some ground points around the building so that it can determine the ground floor elevation. For aerial point clouds, buildings surrounded by others may not meet this condition which may result in inaccurate height estimation above the ground.

![image](https://user-images.githubusercontent.com/72500344/210857587-52af1135-eb92-4682-acd7-6499096a292f.png)

The second image shows the results of our automatic approach to correct buildings height using ground points from LiDAR data :

![image](https://user-images.githubusercontent.com/72500344/210857677-d50e6768-cb15-4640-bcd3-c1445b61b15a.png)

## Usage of the CLI
After installation, you have a small program called <code>zrect</code>. Use <code>zrect --help</code> to see the detailed help:

```
  Usage: zrect [OPTIONS] CITYJSON POINTCLOUD [OUTPUT]

    Correct the heights of buildings in a 3D city model [CityJSON] using
    ground points from LiDAR data [LAS/LAZ/PCD/PLY].

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

<code>zrect buildings.city.json pointcloud.las</code>

This corrects the height of buildings using the default configuration.

### Using Options

<code>zrect buildings.city.json pointcloud.las corrected_buildings.city.json -l '1.3' -k 5000 -t 0.05 -d height_list.json</code>

In this example, we specify LoD1.3 with 5000 points from the LiDAR data to estimate height and a threshold of 0.05 meters to apply correction. The CityJSON file in output is named <code>corrected_buildings.city.json</code> and the list of height differences is <code>height_list.json</code>

## Supported CityJSON versions

The application expects that your file is using the latest version [CityJSON schema](https://www.cityjson.org/specs/1.1.3/). If your file uses an earlier version, you can upgrade it with the upgrade operator of [cjio, CityJSON/io](https://github.com/cityjson/cjio): <code>cjio old.json upgrade save newfile.city.json</code>

Alternatively, any CityGML file can be automatically converted to CityJSON with the open-source project [citygml-tools](https://github.com/citygml4j/citygml-tools).

## Requirements on the Point Cloud

* Acquired through aerial scanning, either Lidar or Dense Image Matching. But Lidar is preferred, because it is often of higher quality.
* Classified, with at least *ground* and *off-ground* classes.
* Well aligned with the 3D Building Model.
* Supported formats: <code>.LAS</code>, <code>.LAZ</code>, <code>.PCD</code> and <code>.PLY</code>.

## About ZRect3D

This software was developped by Anass Yarroudh, a Research Engineer in the [Geomatics Unit of the University of Liege](http://geomatics.ulg.ac.be/fr/home.php).

In case you have the need for professional support don't hesitate to contact me via <ayarroudh@uliege.be>

<img src="https://user-images.githubusercontent.com/72500344/210864557-4078754f-86c1-4e7c-b291-73223bdf4e4d.png" alt="logo" width="200"/>
