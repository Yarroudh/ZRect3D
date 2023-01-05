# Automatic correction of negative height-above-ground in 3D Building Models

## Usage of the CLI
After installation, you have a small program called <code>zrect</code>, to see its possibilities:

<code>zrect --help</code>

<code>Usage: zrect [OPTIONS] CITYJSON POINTCLOUD [OUTPUT]</code>

<code>Correct the heights of buildings in a 3D city model [CityJSON] using ground points from LiDAR data [LAS/LAZ/PCD/PLY].</code>

  Options:
    -l, --lod TEXT          Specify the LoD to correct.  [default: 2.2]
    -d, --differences PATH  Export the list of height differences.  [default:
                            heights.json]

    -k, --knn INTEGER       K nearest neighbors of the lowest vertex to estimate
                            height.  [default: 2000]

    -t, --threshold FLOAT   Height difference threshold to perform the
                            correction.  [default: 0.1]

    --help                  Show this message and exit.
