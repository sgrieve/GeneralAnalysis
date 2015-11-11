def p2gScripter(InputLAS, Prefix, UTMZone, Hillshade=False):
    '''
    Code to generate two bash files, the first will run points2grid to generate
    DEMs from a pointcloud at a range of resolutions from 1 meter to 60 meters.
    The second will project the DEMs into UTM and convert the files to *.bil
    format. The hillshade switch can be set to true to also generate a hillshade
    of each DEM using GDAL.

    This script will need modified to run on the Southern Hemisphere. It does
    not test if the UTM zone given is correct. The generated scripts will delete
    intermediate files as it goes to save space.

    Does not run the code, just generates the script.
    '''

    import math

    Resolutions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24,
                   26, 28, 30, 35, 40, 45, 50, 55, 60]

    with open(Prefix + '_p2g_Script_1.sh', 'w') as p2g, open(Prefix + '_gdal_Script_2.sh', 'w') as gdal:

        # write the shebangs for the 2 scripts
        p2g.write('#!/bin/bash\n')
        gdal.write('#!/bin/bash\n')

        print 'Writing p2g script to ' + Prefix + '_p2g_Script_1.sh'
        print 'Writing p2g script to ' + Prefix + '_gdal_Script_2.sh'

        for r in Resolutions:
            Resolution = str(r)
            OuputName = Prefix + '_' + Resolution
            SearchRadius = str(int(math.ceil(r * math.sqrt(2))))

            p2g_str = ('points2grid -i %s -o %s --idw --fill_window_size=7 '
                       '--output_format=arc --resolution=%s -r %s'
                       % (InputLAS, OuputName, Resolution, SearchRadius))

            gdal_str = ("gdalwarp -t_srs \'+proj=utm +zone=%s +datum=WGS84\' "
                        "-of ENVI %s.idw.asc %s_DEM.bil"
                        % (UTMZone, OuputName, OuputName))

            del_str = ('rm %s.idw.asc\n' % OuputName)

            # write the commands to the 2 scripts
            p2g.write('nice ' + p2g_str + '\n')
            gdal.write('nice ' + gdal_str + '\n')
            gdal.write(del_str)
            if Hillshade:
                hs_str = ('gdaldem hillshade -of PNG %s_DEM.bil %s_HS.png\n'
                          % (OuputName, OuputName))
                gdal.write(hs_str)

    print '\tScripts successfully written.'

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5 and len(sys.argv) != 4:
        sys.exit('\nIncorrect number of arguments.\n\nPlease enter a point '
                 'cloud filename, a filename prefix, a UTM zone number and set '
                 'the hillshade flag (optional). Valid filetypes are LAS and '
                 'ASC\n\ne.g. p2g_generator.py SC_point_cloud.las SC 10 True\n')

    if (len(sys.argv) == 5):
        p2gScripter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    if (len(sys.argv) == 4):
        p2gScripter(sys.argv[1], sys.argv[2], sys.argv[3])
