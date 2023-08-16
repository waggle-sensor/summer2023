# import sys
# sys.path.append("/app/source")

import time
import datetime
import os
import glob
import os.path
import traceback
import subprocess

import argparse

import numpy as np

from source import sunapi_control

from waggle.plugin import Plugin

def set_random_position(camera):
    status = 1
    while status != 0:
        pan_pos = np.random.randint(0, 360)
        tilt_pos = np.random.randint(-20, 90)
        zoom_pos = np.random.randint(1, 2)
        status = camera.absolute_control(float(pan_pos), float(tilt_pos), float(zoom_pos))
        time.sleep(1)


def grab_image(camera):
    position = camera.requesting_cameras_position_information()
    pos_str = str(position[0]) + ',' + str(position[1]) + ',' + str(position[2]) + ' '
    # ct stores current time
    ct = str(datetime.datetime.now())
    camera.snap_shot('./imgs/' + pos_str + ct + '.jpg')


def tar_images(output_filename, folder_to_archive):
    try:
        cmd = ['tar', 'cvf', output_filename, folder_to_archive]
        output = subprocess.check_output(cmd).decode("utf-8").strip()
        print(output)
    except Exception:
        print(f"E: {traceback.format_exc()}")


def publish_images():
    # run tar -cvf images.tar ./imgs
    tar_images('images.tar', './imgs')
    files = glob.glob('./imgs/*.jpg', recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    with Plugin() as plugin:
        ct = str(datetime.datetime.now())
        os.rename('images.tar', ct + '_images.tar')
        plugin.upload_file(ct + '_images.tar')


def main():
    parser = argparse.ArgumentParser("PTZ sampler")
    parser.add_argument("-it", "--iterations",
                        help="An integer with the number of iterations (PTZ rounds) to be run (default=10).", type=int,
                        default=10)
    parser.add_argument("-mv", "--movements",
                        help="An integer with the number of movements in each PTZ round to be run (default=10).",
                        type=int, default=10)
    args = parser.parse_args()


    iterations = args.iterations
    number_of_commands = args.movements

    Camera1 = sunapi_control.CameraControl('10.31.81.17', 'dario', 'Why1Not@')

    status = 1
    while status != 0:
        status = Camera1.absolute_control(1, 1, 1)
        time.sleep(1)

    pan_modulation = 2
    tilt_modulation = 2
    zoom_modulation = 1

    pan_values = np.array([-5, -1, -0.1, 0, 0.1, 1, 5])
    pan_values = pan_values * pan_modulation
    tilt_values = np.array([-5, -1, -0.1, 0, 0.1, 1, 5])
    tilt_values = tilt_values * tilt_modulation
    zoom_values = np.array([-0.2, -0.1, 0, 0.1, 0.2])
    zoom_values = zoom_values * zoom_modulation

    for iteration in range(iterations):
        os.mkdir('./imgs')
        PAN = np.random.choice(pan_values, number_of_commands)
        TILT = np.random.choice(tilt_values, number_of_commands)
        ZOOM = np.random.choice(zoom_values, number_of_commands)
        set_random_position(camera=Camera1)
        grab_image(camera=Camera1)

        for (pan, tilt, zoom) in zip(PAN, TILT, ZOOM):
            Camera1.relative_control(pan=pan, tilt=tilt, zoom=zoom)
            grab_image(camera=Camera1)
            # if np.random.rand() > 0.85:
            #    set_random_position(camera=Camera1)
            #    grab_image(camera=Camera1)

        publish_images()
        os.rmdir('./imgs')

    status = 1
    while status != 0:
        status = Camera1.absolute_control(1, 1, 1)
        time.sleep(1)

    print('DONE!')


if __name__ == "__main__":
    main()
