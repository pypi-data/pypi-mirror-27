#!/usr/bin/env python

import cv2  # OpenCV, the main workhorse of this script
import numpy as np  # to process array data similar to R way
import argparse  # to parse arguments
import os  # to manipulate files and run bash command
import re  # to do regular expression
import sys  # to display error msgs
import matplotlib.pyplot as plt  # to plot

# ============================= read TPS function =============================

def readtps(input):
    """
    Function to read a .TPS file

    Args:
        input (str): path to the .TPS file

    Returns:
        lm (str list): info extracted from 'LM=' field
        im (str list): info extracted from 'IMAGE=' field
        id (str list): info extracted from 'ID=' filed
        coords: returns a 3D numpy array if all the individuals have same
                number of landmarks, otherwise returns a list containing 2D
                numpy array of landmarks
    """

    # open the file
    tps_file = open(input, 'r')  # 'r' = read
    tps = tps_file.read().splitlines()  # read as lines and split by new lines
    tps_file.close()

    # initiate lists to take fields of "LM=","IMAGE=", "ID=" and the coords
    lm, im, ID, coords_array = [], [], [], []

    # looping thru the lines
    for i, ln in enumerate(tps):

        # Each individual starts with "LM="
        if ln.startswith("LM"):
            # number of landmarks of this ind
            lm_num = int(ln.split('=')[1])
            # fill the info to the list for all inds
            lm.append(lm_num)
            # initiate a list to take 2d coordinates
            coords_mat = []

            # fill the coords list by reading next lm_num of lines
            for j in range(i + 1, i + 1 + lm_num):
                coords_mat.append(tps[j].split(' '))  # split lines into values

            # change the list into a numpy matrix storing float vals
            coords_mat = np.array(coords_mat, dtype=float)
            # fill the ind 2d matrix into the 3D coords array of all inds
            coords_array.append(coords_mat)
            # coords_array.append(coords_mat)

        # Get info of IMAGE= and ID= fields
        if ln.startswith("IMAGE"):
            im.append(ln.split('=')[1])

        if ln.startswith("ID"):
            ID.append(ln.split('=')[1])

    # check if all inds contains same number of landmarks
    all_lm_same = all(x == lm[0] for x in lm)
    # if all same change the list into a 3d numpy array
    if all_lm_same:
        coords_array = np.dstack(coords_array)

    # return results in dictionary form
    return {'lm': lm, 'im': im, 'id': ID, 'coords': coords_array}


# ============================== extract contour ==============================

def ocontour(img=None, path=None, bright=True):
    """
    Function to turn organism mask into contour

    Args:
        img (numpy.ndarray): image/ mask (color/image/binary),
        assume background is pure black/ white if it is image
        path (str): alternatively, provide path to the image, assume same
        properties as img

    Returns:
        contour (list): extracted contour
    """
    # alternatively, get image from file
    if path is not None:
        img = cv2.imread(path)

    # change to gray scale if color
    if img.shape > 1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if bright:
        img = np.invert(img)

    # threshold
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (15, 15))

    # contour
    contours = cv2.findContours(thresh, cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if cv2.__version__.startswith("2") else contours[1]
    contours = [x.squeeze() for x in contours]
    return contours


# ======================= main image processing function =======================

def align(tps, img, sep, video = True, text = True,
                pad = 'black', mask = None, mask_pad=None, mask_bright=False):
    """
    Function to warp time-series photos by using landmarks, with options to
    compile the warped photos into time-lapse videos and calculate
    growth/displacement

    Args:
        tps (str): path to tps file containing landmarks for alignments
        img (str): path to the directory containing images to be aligned
        sep (str): separator between individual and time in image name
        video (boolean): whether to compile the time-lapse video
        pad (str): padding color when performing image warping
        # mask, mask_pad, maskbright: optional and developing features,
        # mask is the path to the directory containing masked images, see
        # help(ocontour) for requirements of mask images.

    Returns:
        new sub-directory containing warped images, compiled videos. If mask is
        provided, list of numpy matrices containing the contours will be
        returned

    """

    # read tps file
    tps_read = readtps(tps)
    im = tps_read['im']
    coords = tps_read['coords']
    tps_label = [os.path.splitext(os.path.basename(x))[0] for x in im]

    # determine padding color
    if pad == 'black':
        pad_color = (0, 0, 0)
        text_color = (255, 255, 255)
    elif pad == 'white':
        pad_color = (255, 255, 255)
        text_color = (0, 0, 0)
    else:
        sys.exit('Error: pad should be either "black" or "white"')
    # color for mask padding
    if mask_pad is None:
        mask_pad = pad_color

    # ================= Check if all the image files can be found =================

    # get list of image files from image directory
    img_list = [x for x in os.listdir(img) if
                re.search('(?i)\\.(png|tif?f|jpe?g|bmp)$', x)]  # = which in R

    # strip the extension / get the extension
    img_list_without_ext = [os.path.splitext(x)[0] for x in img_list]
    img_ext = np.array([os.path.splitext(x)[1] for x in img_list])

    # check if all files in TPS exist in img directory
    # following line equal to `im %in% img_list_without_ext` in R
    check_img = [os.path.basename(x) in img_list for x in im]
    if not all(check_img):
        missing_img = im[~np.array(check_img)]  # [~] = [!] in R
        sys.exit('Error: Not all images in TPS file can be found in ' +
                 'image directory (%s is missing)' % (missing_img))

    if mask is not None:
        mask_list = [x for x in os.listdir(mask) if
                    re.search('(?i)\\.(png|tif?f|jpe?g|bmp)$', x)]
        mask_list = [x for x in mask_list if
                    re.findall(r"(?=("+'|'.join(img_list_without_ext)+r"))", x)]
        mask_list_without_ext = [os.path.splitext(x)[0] for x in mask_list]
        mask_ext = np.array([os.path.splitext(x)[1] for x in mask_list])
        check_mask = [x in img_list_without_ext for x in mask_list_without_ext]
        if not all(check_mask):
            sys.exit('mask and image list not matched')

    # ========== Get basic information (ind/time/# of landmarks) ==========

    # get ind and time from label, stored as string numpy arrays
    ind = np.array([x.split(sep)[0] for x in tps_label])
    time = np.array([x.split(sep)[1] for x in tps_label])

    # how many individuals are there?
    unique_ind = set(ind)
    print ('\n%d unique individuals were found in %s. The individuals are: %s.' % (
            len(unique_ind), tps, list(unique_ind)))

    # Determine function (affine/ perpspective) to use based on number of landmarks
    if not isinstance(coords, np.ndarray):  # only accept numpy array
        sys.exit('same number of landmarks across individuals is expected')
    lm_num = coords.shape[0]
    if lm_num == 3:
        mode = ['getAffineTransform', 'warpAffine']
        message = 'affine transformation'
    elif lm_num == 4:
        mode = ['getPerspectiveTransform', 'warpPerspective']
        message = 'perspective transformation'
    else:
        sys.exit('Only 3/4 landmarks are accepted (%d provided)' % (lm_num))
    getMatrix = getattr(cv2, mode[0])
    warpImage = getattr(cv2, mode[1])
    print ('%d landmarks were used, so %s will be performed.\n' % (
            lm_num, message))


    # ================= First level loop starts, individual level =================

    # initialize contours list
    if mask is not None:
        contours = {x: [] for x in unique_ind}

    for i in unique_ind:

        # index for i-th unique ind
        ind_i_idx = np.array([x == i for x in ind])  # boolean
        ind_i_idx = [y for y, x in enumerate(ind_i_idx) if x]  # integer
        # the corresponding time series
        time_i = time[ind_i_idx]
        # if time is digits, convert to integer, for correct sorting
        if all([x.isdigit() for x in time_i]):
            time_i = time_i.astype(np.int)
        # sort time series
        time_i = np.sort(time_i)

        # last image will be used as reference to align each individual series
        last_img_name_i = '%s%s%s' % (i, sep, time_i[-1])
        # extension of the last image, also assume whole series has same extension
        img_ext_i = img_ext[np.array([x == last_img_name_i
                            for x in img_list_without_ext])][0]
        # path to the last image
        last_img_path_i = os.path.join(img, '%s%s'
                                       % (last_img_name_i, img_ext_i))
        # read the last image of i-th individual
        last_img_i = cv2.imread(last_img_path_i)

        # opencv and TPSDig2 has a different coordinate system, so we need to ..
        # ..flip y axis. But first we need to know the yaxis length, last image ..
        # ..is used for this, also assume whole series has the same image size
        img_i_height, img_i_width = last_img_i.shape[0], last_img_i.shape[1]
        coords[:, 1, ind_i_idx] = img_i_height - coords[:, 1, ind_i_idx]

        # corresponding tps, from index of the last img in tps 3d array in z-axis
        last_img_idx = [x == last_img_name_i for x in tps_label]  # boolean
        last_img_idx = [y for y, x in enumerate(last_img_idx) if x][0]  # integer
        lm_ref = coords[:, :, last_img_idx]

        # create directory to store the output
        output_dir_i = os.path.join(img, 'output_%s' % i)
        if not os.path.exists(output_dir_i):
            os.makedirs(output_dir_i)

        # ================= Second level loop starts, time level =================
        # initialize contours list
        if mask is not None:
            contours_i = {x: [] for x in time_i}

        for j_idx, j in enumerate(time_i):

            # name of the i-th ind, j-th time
            img_name_ij = '%s%s%s' % (i, sep, j)
            # get the index of the ij-th landmarks in the tps file
            img_ij_idx = np.array([x == img_name_ij for x in tps_label])  # boolean
            img_ij_idx = [y for y, z in enumerate(img_ij_idx) if z][0]  # integer
            # get the landmarks of the ij-th image, to be rotated against reference
            lm_rot = coords[:, :, img_ij_idx]
            # path to the ij-th image
            img_path_ij = os.path.join(img, '%s%s'
                                       % (img_name_ij, img_ext_i))
            # read the image to be transformed (ij-th image)
            img_ij = cv2.imread(img_path_ij)

            # ------------------------- Warping the image -------------------------

            # calculate transformation matrix
            mat = getMatrix(np.float32(lm_rot), np.float32(lm_ref))
            # warp the photo using transformation matrix
            warped = warpImage(img_ij, mat,
                               (img_i_width, img_i_height),
                                borderValue=pad_color)

            if mask is not None:
                mask_path_ij = os.path.join(mask, '%s%s' % (img_name_ij,
                                                            mask_ext[0]))
                mask_ij = cv2.imread(mask_path_ij)
                warped_mask = warpImage(mask_ij, mat,
                                   (img_i_width, img_i_height),
                                   borderValue=mask_pad)
                contour_ij = ocontour(img=warped_mask, bright=mask_bright)
                contours_i[j] = np.array(contour_ij).squeeze()
                # contours[i].append(contour_ij.squeeze())

            # warped photos saved with tmp file names for easier ffmpeg processing
            new_img_name = os.path.join(output_dir_i,
                                        'tmp_%04d%s' % (j_idx, img_ext_i))

            if text:
                # put text on the photos
                img_label = 'Ind-%s; Time-%s' % (i, j)
                label_font = cv2.FONT_HERSHEY_SIMPLEX
                label_pos = (int(img_i_width * 0.05), int(img_i_height * 0.95))
                cv2.putText(warped, img_label, label_pos, label_font, 3,
                            text_color, 5)

            # save the warped photos
            cv2.imwrite(new_img_name, warped)

            # ---------------------------------------------------------------------

        # ================== Second level loop ends, time level ==================
        if mask is not None:
            contours[i] = contours_i

        # ------------------------- make time lapse video -------------------------
        if video:
            # ffmpeg to compile the time lapse video
            ffmpeg_input = os.path.join(output_dir_i,
                                        'tmp_%%04d%s' % (img_ext_i))
            ffmpeg_output = os.path.join(output_dir_i,
                                        '%s_timelapse.mp4' % (i))
            ffmpeg_option = '-c:v libx264 -vf "fps=25,format=yuv420p"'
            ffmpeg_cmd = 'ffmpeg -r 1 -i %s %s -r 25 %s' % (
                        ffmpeg_input, ffmpeg_option, ffmpeg_output)
            os.system(ffmpeg_cmd)

        # -------------------------------------------------------------------------

        # renaming file names from temporary names to final names
        filelist_i = [x for x in os.listdir(output_dir_i) if
                      x.startswith('tmp_') and x.endswith(img_ext_i)]
        for k_idx, k in enumerate(sorted(filelist_i)):
            os.rename(os.path.join(output_dir_i, k),
                      os.path.join(output_dir_i, 'warped_%s-%s%s' % (
                       i, time_i[k_idx], img_ext_i)))

    # output
    if mask is not None:
        return contours

    # ================== First level loop ends, individual level ==================


# ========================= Functions for calculations =========================

def cent(contour):
    """
    Function to calculate centroids

    Args:
        contours (numpy ndarray): xy(z) coordinates

    Returns:
        centroid (tuple)
    """
    return np.apply_along_axis(np.mean, 0, contour)


def ild(a, b):
    """
    Function to calculate euclidean distance

    Args:
        a (tuple): first xy coords
        b (tuple): second xy coords

    Returns:
        distance
    """
    return np.sqrt(np.sum((np.array(a) - np.array(b))**2))


def vangle(v1, v2, degree = True):
    """
    Returns angle between two vectors

    Args:
        v1 (tuple): vector 1
        v2 (tuple): vector 2
        degree (boolean): return degree is True, else radian

    Returns:
        angle (float)
    """
    # modified from https://stackoverflow.com/questions/2827393/
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    angle = np.arccos(np.clip(np.dot(v1_norm, v2_norm), -1.0, 1.0))
    if degree:
        angle = angle * 180 / np.pi
    return angle


# ========================= Main calculation function =========================

def mov_calc(contours, scale = None):
    """
    Function to calculate contours areas, centroid and translation of the
    centroids

    Args:
        contours (dict): contours as returned by align, nested dictionary
        containing individuals at first level and times at second level
        scale (list): list of scale for diff individuals

    Returns:
        two .csv files. First contains the result of area.
        second contains the result of distance and angle moved by centroids of
        the contours, and the increase in area.
    """

    if scale is not None:
        if len(scale) != len(contours.keys()):
            sys.exit('provided scale does not match no. of ind.')

    for i in contours.keys():  # ind
        cent_list_i, area_list_i = [], []
        time_key = contours[i].keys()
        # open the files for writing
        growth_csv = open('growth-result-%s.csv' % (i), 'w')
        area_csv = open('area-%s.csv' % (i), 'w')
        # write the headers
        area_csv.write('time, area\n')  # by ind
        growth_csv.write('time, distance_moved, area_increase, ' +
                            'area_inc_by_percent, angle\n') # by ind-to-ind
        for j_idx, j in enumerate(time_key):  # time
            # cent(contours[i][j])
            cent_list_i.append(cent(contours[i][j]))
            area_ij = cv2.contourArea(contours[i][j])
            if scale is not None:
                area_ij = area_ij * (scale[i]**2)
            area_list_i.append(area_ij)
            area_csv.write('time-%s, %s\n' % (j, area_ij))
            # calculation for t & t-1
            if j_idx > 0:
                ild_ij = ild(cent_list_i[j_idx], cent_list_i[j_idx - 1])
                angle_ij = vangle(cent_list_i[j_idx], cent_list_i[j_idx - 1])
                if scale is not None:
                    ild_ij = ild_ij * scale[i]
                area_diff_i = area_ij - area_list_i[j_idx-1]
                area_diff_percent = (area_diff_i / area_list_i[j_idx-1]) * 100
                growth_csv.write('time-%s-to-time-%s' % (time_key[j_idx-1], j) +
                                 ',%s, %s, %s, %s\n' % (ild_ij, area_diff_i,
                                    area_diff_percent, angle_ij))
            # last, calculate first and last
            if j_idx == (len(time_key)-1):
                growth_csv.write('time-%s-to-time-%s' % (time_key[0], j) +
                                 ',%s, %s, %s, %s\n' % ((
                                 ild(cent_list_i[0], cent_list_i[j_idx]) * scale[i]),
                                 (area_ij - area_list_i[0]),
                                 ((area_ij - area_list_i[0]) / area_list_i[0] * 100),
                                 vangle(cent_list_i[0], cent_list_i[j_idx])))
        growth_csv.close()
        area_csv.close()


# ========================= For running as standalone =========================



def main(args=None):
    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--tps',
                    help='path to tps file containing landmarks for' +
                         ' alignments')
    ap.add_argument('-i', '--img',
                    help='path to the directory containing images to ' +
                         'be aligned')
    ap.add_argument('-s', '--sep',
                    help='separator between individual and time in image ' +
                    'name. NOTE: use single quote (\') for special character' +
                    ' in Unix systems')
    args = vars(ap.parse_args())
    align(tps=args['tps'], img=args['img'], sep=args['sep'])

if __name__ == "__main__":
    main()
