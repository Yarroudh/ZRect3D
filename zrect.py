import click
import time
import json
import copy
import numpy as np
import laspy
import open3d as o3d
from progress.bar import Bar

@click.command()
@click.argument('cityjson', type=click.Path(exists=True), required=True)
@click.argument('pointcloud', type=click.Path(exists=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=False)
@click.option('-l', '--lod', help='Specify the LoD to correct.', type=click.STRING, default='2.2', show_default=True)
@click.option('-d', '--differences', help='Export the list of height differences.', type=click.Path(exists=False), default='heights.json', show_default=True)
@click.option('-k', '--knn', help='K nearest neighbors of the lowest vertex to estimate height.', type=click.INT, default=2000, show_default=True)
@click.option('-t', '--threshold', help='Height difference threshold to perform the correction.', type=click.FLOAT, default=0.1, show_default=True)

def zrect(cityjson, pointcloud, output, lod, differences, knn, threshold):
    '''
    Correct the buildings ground floor elevation in a 3D city model [CityJSON] using ground points from LiDAR data [LAS/LAZ/PCD/PLY].
    '''
    start = time.time()
    outputFile = output if output is not None else "output.city.json"

    print("Start processing...\n")
    
    try:
        with open(cityjson) as file:
            bar1 = Bar('Reading CityJSON file', max=4, suffix='%(percent)d%%')
            
            # Read CityJSON
            data = json.load(file)
            bar1.next()
            scale = data['transform']['scale']
            bar1.next()
            translate = data['transform']['translate']
            bar1.next()
            dataCopy = copy.deepcopy(data)
            bar1.next()
            bar1.finish()    

            bar2 = Bar('Reading and processing Point Cloud', max=6, suffix='%(percent)d%%')

            # Read the Point Cloud
            if (pointcloud.lower().endswith(('.las', '.laz'))):
                las = laspy.read(pointcloud)
                bar2.next()
                ground = las.points[las.classification == 2]
                bar2.next()
                points = np.vstack((ground.x, ground.y, ground.z)).transpose()
                bar2.next()
                pcd = o3d.geometry.PointCloud()
                bar2.next()
                pcd.points = o3d.utility.Vector3dVector(points)
                bar2.next()
            else:
                pcd = o3d.io.read_point_cloud(pointcloud)
                bar2.next()
                bar2.next()
                bar2.next()
                bar2.next()

            bar2.next()
            kdTree = o3d.geometry.KDTreeFlann(pcd)
            bar2.next()
            bar2.finish()

            bar3 = Bar('Correcting heights', max=len(data['CityObjects']), suffix='%(percent)d%%')
            
            # Correcting heights
            heightDifferences = []
            for (key, value) in data['CityObjects'].items():
                geometry = data['CityObjects'][key].get('geometry')
                correctedVertices = []
                semantics = []

                if (data['CityObjects'][key]['type'][:8] == 'Building'):
                    for (a, geom) in enumerate(geometry):
                        if (geom['lod'] == str(lod)):
                            for value in geom['semantics']['values'][0]:
                                semantics.append(geom['semantics']['surfaces'][int(value)].get('type'))

                            for (b, primitive) in enumerate(geom['boundaries']):
                                for (c, surface) in enumerate(primitive):
                                    for (d, polygon) in enumerate(surface):
                                        if (semantics[c] == 'GroundSurface'):
                                            heights = []
                                            vertices = []
                                            for vertex in polygon:
                                                index = int(vertex)
                                                z = float(data['vertices'][index][2]) * scale[2] + translate[2]
                                                
                                                heights.append(z)
                                                vertices.append(index)
                                                
                                            minZ = min(heights)
                                            indexZ = vertices[heights.index(minZ)]
                                            
                                            searchX = float(data['vertices'][indexZ][0]) * scale[0] + translate[0]
                                            searchY = float(data['vertices'][indexZ][1]) * scale[1] + translate[1]
                                            searchZ = float(data['vertices'][indexZ][2]) * scale[2] + translate[2]
                                            
                                            [k, idx, _] = kdTree.search_knn_vector_3d([searchX, searchY, searchZ], knn)
                                        
                                            sum = 0
                                            for j in range(k):
                                                sum += pcd.points[idx[j]][2]
                                            corrZ = sum / k
                                            
                                            offset = minZ - corrZ

                                            if (np.abs(offset) >= threshold):
                                                for (e, vertex) in enumerate(polygon):
                                                    index = int(vertex)

                                                    x = float(data['vertices'][index][0])
                                                    y = float(data['vertices'][index][1])
                                                    z = float(data['vertices'][index][2]) - (offset / scale[2] - translate[2])
                                                    
                                                    dataCopy['vertices'].append([x, y, z])
                                                    newVertex = len(dataCopy['vertices']) - 1
                                                    
                                                    dataCopy['CityObjects'][key]['geometry'][a]['boundaries'][b][c][d][e] = newVertex
                                                    correctedVertices.append(vertex)
                                                    correctedVertices.append(newVertex)

                                            heightDifferences.append(
                                                {
                                                    key: 
                                                        {
                                                            '3D Model Height': round(minZ, 2),
                                                            'Height on ground': round(corrZ, 2),
                                                            'Height difference': round(offset, 2)
                                                        }
                                                }
                                            )

                                        if (semantics[c] == 'WallSurface'):
                                            for (e, vertex) in enumerate(polygon):
                                                if (vertex in correctedVertices):
                                                    i = correctedVertices.index(vertex)
                                                    dataCopy['CityObjects'][key]['geometry'][a]['boundaries'][b][c][d][e] = correctedVertices[i+1]
                bar3.next()

    except Exception as error:
        if (cityjson.lower().endswith(('.json'))==False):
            print("\nUsage: zrect [OPTIONS] CITYJSON POINTCLOUD [OUTPUT]")
            print("Try 'zrect --help' for help.\n")
            print("Error: Unexpected file extension ({})".format(cityjson[-4:]))
        elif (pointcloud.lower().endswith(('.las', '.laz', '.pcd', '.ply'))==False):
            print("\nUsage: zrect [OPTIONS] CITYJSON POINTCLOUD [OUTPUT]")
            print("Try 'zrect --help' for help.\n")
            print("Error: Unexpected file extension ({})".format(pointcloud[-4:]))
        else:
            print("\nUsage: zrect [OPTIONS] CITYJSON POINTCLOUD [OUTPUT]")
            print("Try 'zrect --help' for help.\n")
            print("Error: <{}>".format(error))
        exit()

    bar3.finish()

    with open(outputFile, 'w') as file:
        json.dump(dataCopy, file)

    with open(differences, 'w') as file:
        json.dump(heightDifferences, file)

    end = time.time()
    processTime = end - start

    click.echo("\nDONE PROCESSING")
    click.echo("Time: {}".format(time.strftime("%H:%M:%S", time.gmtime(processTime))))
    click.echo("Output: '{}' '{}'".format(outputFile, differences))

def main():
    zrect(prog_name='zrect')
 
if __name__ == '__main__':
    main()