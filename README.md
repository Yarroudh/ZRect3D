# Automatic correction of buildings height in 3D City Models
Command-Line Interface (CLI) application to process and correct buildings height in CityJSON files using ground points from LiDAR data.


![image](https://user-images.githubusercontent.com/72500344/210857587-52af1135-eb92-4682-acd7-6499096a292f.png)
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
