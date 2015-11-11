def p2gScripter(InputLAS, Prefix, UTMZone, Cores, Hillshade=False):
    '''
    Code to generate two bash files, the first will run points2grid to generate
    DEMs from a pointcloud at a range of resolutions from 1 meter to 60 meters.
    The second will project the DEMs into UTM and convert the files to *.bil
    format. The hillshade switch can be set to true to also generate a hillshade
    of each DEM using GDAL.

    This script will need modified to run on the Southern Hemisphere. It does
    not test if the UTM zone given is correct. The generated scripts will delete
    intermediate files as they go to save space.

    Script is designed to allow simple parralelization of gridding using the
    Cores argument, the processing will be divided into separate scripts based
    on the value suppled. So Cores == 1 will generate a single file, Cores == 5
    will generate 5 files which can be run in parallel, and so on.

    Does not run the code, just generates the script.

    SWDG
    11/11/15
    '''

    import math

    Resolutions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24,
                   26, 28, 30, 35, 40, 45, 50, 55, 60]

    for a in range(Cores):

        with open(Prefix + '_p2g_Script_' + str(a) + '.sh', 'w') as p2g, \
                open(Prefix + '_gdal_Script_' + str(a) + '.sh', 'w') as gdal:

            # write the shebangs for the 2 scripts
            p2g.write('#!/bin/bash\n')
            gdal.write('#!/bin/bash\n')

            print '\nWriting to ' + Prefix + '_p2g_Script_' + str(a) + '.sh'
            print 'Writing to ' + Prefix + '_gdal_Script_' + str(a) + '.sh'

            for r in Resolutions[a::Cores]:
                Resolution = str(r)
                OuputName = Prefix + '_' + Resolution
                SearchRadius = str(int(math.ceil(r * math.sqrt(2))))

                p2g_str = ('points2grid -i %s -o %s --idw --fill_window_size=7 '
                           '--output_format=arc --resolution=%s -r %s'
                           % (InputLAS, OuputName, Resolution, SearchRadius))

                gdal_str = ("gdalwarp -t_srs \'+proj=utm +zone=%s "
                            "+datum=WGS84\' -of ENVI %s.idw.asc %s_DEM.bil"
                            % (UTMZone, OuputName, OuputName))

                del_str = ('rm %s.idw.asc\n' % OuputName)

                # write the commands to the 2 scripts
                p2g.write('nice ' + p2g_str + '\n')
                gdal.write('nice ' + gdal_str + '\n')
                gdal.write(del_str)
                if Hillshade:
                    hs_str = ('gdaldem hillshade -of ENVI '
                              '%s_DEM.bil %s_HS.bil\n'
                              % (OuputName, OuputName))
                    gdal.write(hs_str)

    print '\tScripts successfully written.'

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 6 and len(sys.argv) != 5:
        sys.exit('\nIncorrect number of arguments.\n\nPlease enter a point '
                 'cloud filename, a filename prefix, a UTM zone number, the '
                 'number of cores code will be run on, and set the hillshade '
                 'flag (optional). Valid filetypes are LAS and ASC\n\ne.g. '
                 'p2g_generator.py SC_point_cloud.las SC 10 5 True\n')

    if (len(sys.argv) == 6):
        p2gScripter(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]),
                    sys.argv[5])
    if (len(sys.argv) == 5):
        p2gScripter(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
