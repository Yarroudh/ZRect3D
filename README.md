# Automatic correction of buildings height in 3D City Models
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
    
