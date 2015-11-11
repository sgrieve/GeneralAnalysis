def p2gScripter(InputLAS, Prefix):
    '''
    Code to generate a bash file that will run points2grid to generate DEMs from
    a pointcloud at a range of resolutions from 1 meter to 60 meters.

    Does not run the code, just generates the script.
    '''

    import math

    Resolutions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24,
                   26, 28, 30, 35, 40, 45, 50, 55, 60]

    with open(Prefix + '_p2g_Script_1.sh', 'w') as f:
        f.write('#!/bin/bash\n')

        print 'Writing p2g script to ' + Prefix + '_p2g_Script_1.sh'

        for r in Resolutions:
            Resolution = str(r)
            OuputName = Prefix + '_' + Resolution
            SearchRadius = str(int(math.ceil(r * math.sqrt(2))))

            p2g_str = ('points2grid -i %s -o %s --idw --fill_window_size=7 '
                       '--output_format=arc --resolution=%s -r %s'
                       % (InputLAS, OuputName, Resolution, SearchRadius))

            f.write('nohup nice ' + p2g_str + ' &\n')

    print '\tScript successfully written.'

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        sys.exit('\nIncorrect number of arguments.\n\nPlease enter a point '
                 'cloud filename and a filename prefix. Valid filetypes are LAS'
                 ' and ASC\n\ne.g. p2g_generator.py SC_point_cloud.las SC\n')

    p2gScripter(sys.argv[1], sys.argv[2])
