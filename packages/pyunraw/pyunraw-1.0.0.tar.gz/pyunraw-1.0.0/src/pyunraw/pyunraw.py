# -*- coding: utf-8 -*-

# pyunraw.py  ******************************************************************
#
# Copyright (C) 2017 Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
#
# This file is part of the pyunraw distribution.
#
# pyunraw is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.
#
# pyunraw is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#
# Maintainer: Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
# Doc: http://pyunraw.readthedocs.io/en/latest/
#
# ******************************************************************************

import sys
import os
from datetime import datetime
import imghdr
import json
import pickle
from threading import Thread

import _pyunraw

version = (1, 0, 0)
__version__ = ".".join([str(i) for i in version])
__dcraw_version__ = _pyunraw.PyUnraw("").dcraw_version

class PgmSizeError(TypeError):
    """Exception raised when the dark frame has not the same size of the 
    raw image.

    Attribute:
    values -- the size of the pgm file and the size of the raw file
    """
    def __init__(self, values):
        self.values = values

    def __str__(self):
        return "The dark frame must have the same size as the raw image, "\
               "(%s x %s) -> (%s x %s)"  % self.values

class PgmEncodingError(TypeError):
    """Exception raised when the dark frame is not a 16 bits image.

    """
    def __init__(self):
        pass

    def __str__(self):
        return "The dark frame must be a 16 bits image"

class PyUnraw:
    def __init__(self, filename=""):
        """Initialise the class PyUnraw with the raw file name.

        Args:
        filename -- the path/name.ext of the raw file, optionnal

        Raises a ValueError if the file doesn't exists
        Raises a TypeError if the file is clearly identified as a non-raw format,
        (jpeg, tiff, ppm, ...)
        """
        self.date_time = None
        self.out_filename = None
        self.raw = False
        self.read_error = None
        self.profile = {}
        self.reset = False
        self.preview = False
        self.tasks = []
        self.callback = False
        if filename:
            self.reset = True
            self.set_source_file(filename)

    def set_source_file(self, filename):
        """Set a new RAW source file.

        This doesn't reset the unrawing parameters previously fixed. This method
        is intended to unraw a list of raw files with the same parameters.

        Args:
        filename -- absolute path of RAW source file
        """
        self.filename = filename
        self.data = {}
        self.is_raw = False
        self.check_file()
        self.identify()

    def identify(self):
        """Identify the raw file.

        If the format of the file is supported the attribute PyUnraw.is_raw 
        become True, otherwise its value is False.

        The properties of the image can be read with the method
        PyUnraw.get_file_properties().

        If a reading error occur, the attribute PyUnraw.read_error contains
        perhaps the reason of the error.
        """
        try:
            self.raw = _pyunraw.PyUnraw(self.filename)
            if self.reset:
                self.reset_profile()

            self.reset = False
        except Exception as why:
            self.read_error = why
            return

        self.data = self.raw.properties
        if self.data is not None:
            if self.data['image_count']:
                self.is_raw = True
                if self.data["time"]:
                    try:
                        self.data["date_time"] = datetime.fromtimestamp(
                                                    self.data["time"])
                    except Exception as why:
                        # bad formating ?
                        pass

                self.data["color_space"] = 1
                self.data["icc_profil"] = None
                self.data["white_adjust"] = None
                self.data["template_wb"] = None
                self.data["color_matrice"] = True

    def get_file_properties(self):
        """Return the image properties as a dictionnary.

        """
        if self.is_raw:
            return self.data

    def reset_profile(self):
        """Reset all parameters to the default values.

        The profile will be emptyed.
        """
        if self.raw:
            self.raw.reset()
            self.profile = {}

    def set_white_balance(self, red, green, blue, green1=0):
        """Set the value of the white balance.

        To reset the white balance to the default values use 0 for each value.

        Args:
        red -- the red value
        green -- the green value
        blue -- the blue value
        green1 -- the second green value, if 0 the value of green will be used
        """
        red, green, blue, green1 = map(float, [red, green, blue, green1])
        green1 = green1 or green
        if not sum((red, green, blue, green1)):
            self.profile.pop("white_balance", None)

        else:
            self.profile["white_balance"] = [red, green, blue, green1]

        self.raw.set_white_balance(red, green, blue, green1)

    def ignore_white_balance(self):
        """Use a fixed white level, ignoring the camera parameters.

        """
        self.raw.set_white_balance(0.0, 0.0, 0.0, 0.0)
        self.profile["white_balance"] = False
        self.raw.ignore_white_balance(1)

    def set_gamma_curve(self, power, toe_sloop=0):
        """Set the gamma curve values.

        Use PyUnraw.set_gamma_curve(0) to reset to the default values BT.709 
        (2.222 4.5).

        Args:
        power -- the value of the power
        toe_sloop -- the value of the sloop
        """
        # https://en.wikipedia.org/wiki/Gamma_correction
        if not power:
            power = 1
            if not toe_sloop:
                # set to default value (BT.709)
                self.raw.set_gamma_curve(2.222, 4.5)
                self.profile.pop("gamma", None)
                return

        self.profile["gamma"] = [power, toe_sloop]
        self.raw.set_gamma_curve(power, toe_sloop)

    def stretch_red_blue_layers(self, red, blue=0):
        """Fix the chromatic aberration.

        Strech the raw red and blue layers by the given factors, typically 
        0.999 to 1.001.

        Use PyUnraw.stretch_red_blue_layers(0) to reset to default values.

        Args:
        red -- the red factor
        blue -- the blue factor
        """
        if not red:
            red = 1
            if not blue:
                self.raw.fix_chromatic_aberration(1.0, 1.0)
                self.profile.pop("chrom_aber", None)
                return

        self.profile["chrom_aber"] = [red, blue]
        self.raw.fix_chromatic_aberration(1/red, 1/blue)

    def set_color_space(self, space):
        """Define the output color space.

        This cancel a previously ICC profile defined.

        Use PyUnraw.set_color_space(1) to reset to default value (sRGB D65).

        Args:
        space -- index of the color space
                0   Raw color (unique to each camera)
                1   sRGB D65 (default)
                2   Adobe RGB (1998) D65
                3   Wide Gamut RGB D65
                4   Kodak ProPhoto RGB D65
                5   XYZ
                6   ACES
        """
        if not isinstance(space, int):
            raise TypeError("Color space arg must be int, got %s" 
                            % type(space))

        space = min(space, 6)
        self.profile["color_space"] = space
        self.profile.pop("ICC", None)
        self.raw.set_color_space(space)

    def set_ICC_profile(self, profile, output=""):
        """Apply an ICC profile to the image.

        The ICC profile can be embeded into the camera, that can be checked 
        with PyUnraw.data["embeded_icc"].

        Args:
        profile -- False: Don't apply an ICC profile
                   True: Apply the embeded ICC profile
                   "path/camera.icm": Use this file as ICC profile
        output -- "path/camera.icm": File name to write the embeded ICC profile
        """
        if not profile:
            self.profile.pop("ICC", None)
            self.raw.set_embedded_icc(0)
            return

        elif isinstance(profile, str):
            if not os.path.isfile(profile):
                raise ValueError("No such file: %s" % profile)

            self.raw.set_custom_icc(profile)

        else:
            self.raw.set_embedded_icc(1)

        self.profile["ICC"] = profile
        if output:
            self.raw.set_output_icc(output)

    def set_noise_threshold(self, threshold):
        """Fix the noise threshold limit.

        The best value should be somewhere between 100 and 1000.

        Use PyUnraw.set_noise_threshold(0) to reset the parameter.

        Args:
        threshold -- the value of the threshold limit
        """
        if not isinstance(threshold, (int, float)):
            raise TypeError("Threshold value must be int or float, got %s" 
                            % type(threshold))

        if not threshold:
            self.profile.pop("noise_threshold", None)

        else:
            self.profile["noise_threshold"] = threshold

        self.raw.reduce_noise(float(threshold))

    def set_highlights(self, level):
        """Set the highlights level.

        Use PyUnraw.set_highlights(0) to reset the parameter.

        Args:
        level -- the level of highlights, the value must be in range(10)
                0   Clip all highlights to solid white (default).
                1   Leave highlights unclipped in various shades of pink.
                2   Blend clipped and unclipped values together for a gradual 
                    fade to white.
                3~9 Reconstruct highlights.  Low numbers favor whites; high 
                    numbers favor colors.  Try 5 as a compromise.
        """
        if not isinstance(level, int):
            raise TypeError("Highlights level must be int, got %s" 
                            % type(level))

        if level < 0 or level > 9:
            raise ValueError("Highlights level must be in range(10)")

        if not level:
            self.profile.pop("highlight", None)

        else:
            self.profile["highlight"] = level

        self.raw.set_highlights_level(level)

    def find_white_balance(self, x=0, y=0, w=0, h=0):
        """Use a rectangular area to compute the white balance.

        The parameters calculated will be applyed automatically.

        Use PyUnraw.find_white_balance() to cancel this method.

        Args:
        x -- the left side of the area
        y -- the top side of the area
        w -- the width of the area
        h -- the height of the area
        """
        auto = 1
        if w:
            self.check_area(x, y, w, h)
            auto = 0

        else:
            self.profile.pop("auto_wb", None)

        self.profile["auto_wb"] = (x, y, w, h)
        self.raw.compute_white_balance(auto, x, y, w, h)

    def set_interpolation_method(self, method):
        """Set the interpolation method.

        Args:
        method -- the index of the method
            0   Use high-speed, low-quality bilinear interpolation.
            1   Use Variable Number of Gradients (VNG) interpolation.
            2   Use Patterned Pixel Grouping (PPG) interpolation.
            3   Use Adaptive Homogeneity-Directed (AHD) interpolation.
            4   Interpolate RGB as four colors.
            5   Show the raw data as a grayscale image with no interpolation.
            6   Same as #5, but with the original unscaled pixel values.
            7   Same as #6, but masked pixels are not cropped.
            8   Output a half-size color image.  Twice as fast as #0.
        """
        if not isinstance(method, int):
            raise TypeError("Interpolation method must be int, got %s" 
                            % type(method))

        if method < 0:
            raise ValueError("Interpolation method must be in range(9)")

        method = min(method, 8)
        self.profile["interpolation"] = method
        self.raw.set_interpolation(method)

    def clean_artifacts(self, passes):
        """set the number of passes for the artifacts cleaning.

        Args:
        passes -- the number of passes
        """
        if not isinstance(passes, int):
            raise TypeError("Cleaning artifacts argument must be int, got %s" 
                            % type(passes))

        self.profile["clean_artifacts"] = passes
        self.raw.clean_artifacts(passes)

    def set_darkness(self, level):
        """Set the level of darkness.

        Args:
        level -- the level of darkness
        """ 
        if not isinstance(level, int):
            raise TypeError("Darkness level must be int, got %s" 
                            % type(level))

        if not level:
            self.profile.pop("darkness", None)

        else:
            level = -1
            self.profile["darkness"] = level

        self.raw.set_darkness(level)

    def set_saturation(self, level):
        """Set the level of saturation.

        Args:
        level -- the level of saturation
        """ 
        if not isinstance(level, int):
            raise TypeError("Saturation level must be int, got %s" 
                            % type(level))

        if not level:
            level = -1
            self.profile.pop("saturation", None)

        else:
            self.profile["saturation"] = level

        self.raw.set_saturation(level)

    def set_brightness(self, factor):
        """Divide the white level by this number, 1.0 by default.

        Args:
        factor -- the value to divide the white level
        """
        if not isinstance(factor, float):
            raise TypeError("Brightness factor must be float, got %s"
                            % type(factor))

        if not factor:
            self.profile.pop("brightness", None)
            factor = 1

        else:
            self.profile["brightness"] = factor

        self.raw.set_brightness(factor)

    def write_sixteen_bits(self, apply_, linear=False):
        """Write sixteen bits per sample.

        Args:
        apply_ -- boolean: apply 16 bits if True
        linear -- boolean: apply 16 bits linear if True
        """
        if not apply_:
            self.profile.pop("16_bits", None)
            self.raw.write_sixteen_bits(8, 0)
            self.set_gamma_curve(0)

        else:
            self.profile["16_bits"] = (apply_, linear)
            if not linear:
                self.raw.write_sixteen_bits(16, 0)
                self.set_gamma_curve(0)

            else:
                self.raw.write_sixteen_bits(16, 1)

    def set_output_format(self, use_tiff=True):
        """Use the tiff format with metadata instead of ppm, pgm or pam.

        Args:
        use_tiff -- boolean: use tiff format if True (default), otherwise,
                 depending of the source file, the format pgm, ppm or pam will
                 be choosed
        """
        if use_tiff:
            self.profile.pop("write_tiff", None)
            tiff = 1

        else:
            self.profile["write_tiff"] = False
            tiff = 0

        self.raw.force_tiff(tiff)

    def set_orientation(self, orientation):
        """Set the orientation of the decoded image.

        Args:
        orientation -- integer which define the orientation
                       The integer must be in (-1, 0, 3, 5, 6, 90, 180, 270)
                        -1: apply the orientation found into the metadata
                         0: no rotation
                         3 or 180: rotate 180°
                         5 or 270: rotate 270°
                         6 or 90:  rotate  90°

        """
        if not isinstance(orientation, int):
            raise TypeError("Orientation must be int, got: %s" 
                            % type(orientation))

        if not orientation in (-1, 0, 3, 5, 6, 90, 180, 270):
            raise ValueError("Bad orientation: %s" % orientation)

        if not orientation:
            self.profile.pop("orientation", None)

        else:
            self.profile["orientation"] = orientation

        self.raw.set_orientation(orientation)

    def rotate_fuji(self, rotate):
        """Rotate the decoded image to 45°.

        For  Fuji Super CCD  cameras where the image are tilted 45 degrees.

        Args:
        rotate -- boolean: True, apply the rotation (default)
                           False, show the image tilted 45 degrees
        """
        if rotate:
            self.profile.pop("fuji_rotate", None)
            

        else:
            self.profile["fuji_rotate"] = False

        r = (0, 1)[rotate]
        self.raw.rotate_fuji(r)

    @property
    def has_preview(self):
        return self.data["preview"]

    def get_preview(self, dest=""):
        """Extract a preview embeded into the raw file.

        The attribute PyUnraw.has_preview define if there's at least one
        preview in the raw file.
        After writing the preview on disk, the attribute PyUnraw.preview define  
        the file name or None if the process failed.

        Args:
        dest -- the absolute destination file name.  If not provided, the name 
                of the preview is build with the name of the file source and the 
                suffix `_thumb' i.e. DSC0786.NEF --> DSC0786_thumb.jpg.
        """
        if self.has_preview:
            if not dest:
                target = os.path.splitext(self.filename)[0] + "_thumb"

            else:
                target = os.path.splitext(dest)[0]

            self.preview = self.raw.get_thumbnail(target)

    def set_black_layer(self, filename=None):
        """Set the name of the dark frame.

        If the file is already a .pgm file the file is checked for validity.
        If the file is yet a raw file it will be converted into a valid .pgm

        Args:
        filename -- absolute path of the file

        Raises PgmSizeError if the size of the frame is not the same size of the 
        source file.

        Raises PgmEncodingError if the .pgm is not encoded in 16 bits.
        """
        if filename is None:
            self.black_layer = None
            self.profile.pop("dark", None)
            self.raw.set_dark_frame("")
            return

        if not os.path.isfile(filename):
            raise ValueError("No such file: %s" % filename)

        if os.path.splitext(filename)[1] == '.pgm':
            if self.valid_pgm(filename):
                self.profile["dark"] = filename
                self.raw.set_dark_frame(filename)

        else:
            try:
                raw = _pyunraw.PyUnraw(filename)
            except Exception as why:
                print("PyUnaw read error: %s" % why)
                return

            props = raw.properties
            if props is not None:
                if props['image_count']:
                    size = props['image_size']
                    if size != self.data["image_size"]:
                        s = (size[0], size[1], self.data["image_size"][0], 
                             self.data["image_size"][1])
                        raise PgmSizeError(s)

                    pgm = self.unraw_dark(filename)
                    # Need to remove the unraw params of the dark and apply
                    # the profile of the original raw image
                    self.raw.reset()
                    self.apply_new_profile(self.profile)
                    if pgm:
                        self.set_black_layer(pgm)

                else:
                    print("No image found in %s" % filename)
                    return

            else:
                print("Can't decode %s" % filename)
                return

    def fix_dead_pixels(self, fname=""):
        """Fix the dead pixels given with the file fname.

        Args:
        fname -- absolute path of the file
        """
        if not fname:
            self.profile.pop("dead_pixels", None)

        else:
            if not os.path.isfile(fname):
                raise ValueError("No such file: %s" % fname)

            self.profile["dead_pixels"] = fname

        self.raw.fix_dead_pixels(fname)

    def unraw(self, index=0, dest=""):
        """Run the demosaication process.

        Args:
        index -- the index of the image or "all" if there's more than one image
                 into the file
        dest -- the absolute file name for the image decoded.  If a file with 
                the same name already exists, it will be overwritten.

        Raises IndexError if index >= self.image_count
        """
        if not self.is_raw:
            fname = os.path.basename(self.filename)
            raise TypeError("RAW file %s not supported!" % fname)

        if not dest:
            dest = self.filename

        target = os.path.splitext(dest)[0]
        if index == "all":
            indexes = list(range(self.data["image_count"]))
            
        else:
            if index >= self.data["image_count"]:
                raise IndexError("Index of image %s out of range(%s)" 
                                 %(index, self.data["image_count"]))

            indexes = [index]

        multi = len(indexes) > 1
        for index in indexes:
            dest = target
            if multi:
                dest = target + "_%s" % index

            self.raw.demosaicate(index, dest)
            self.out_filename = self.raw.out_file

    def unraw_dark(self, filename, dest=""):
        """Decode a raw image as a dark.

        Args:
        filename -- absolute path of raw file
        dest -- absolute path of destination, if not provided the pgm file
                will be named wit the raw file name

        Return the path of the pgm file or None if failed
        """
        try:
            dark = _pyunraw.PyUnraw(filename)
            dark.reset()
        except Exception as why:
            print("PyUnaw read error: %s" % why)
            return

        props = dark.properties
        if props is not None:
            if props['image_count']:
                dark.set_interpolation(6) 
                dark.write_sixteen_bits(16, 1) 
                dark.set_orientation(0)
                dark.rotate_fuji(0)
                if not dest:
                    dest = filename

                target = os.path.splitext(dest)[0]
                res = dark.demosaicate(0, 0, target)
                return dark.out_file

    def get_unraw_parameters(self):
        """Return the parameters used for the demosaication.

        """
        return self.raw.get_parameters()

    def check_file(self, path=""):
        """Check the raw source file.

        Args:
        path -- the path of the raw image file, if not provided the current 
                image file is checked
        """
        if not path:
            path = self.filename

        if not os.path.isfile(path):
            raise ValueError("No such file: %s" % path)

        ext = os.path.splitext(path)[1]
        type_ = imghdr.what(path)
        if type_:
            # imghdr return 'tiff' also for raw image
            if type_ == 'tiff' and ext.lower() not in ['.tiff', '.tif']:
                return

            raise TypeError("Can decode only RAW file not '%s' file" % type_)

    def validate(self, filename):
        """Return True if the file is a valid RAW image supported by dcraw.

        Args:
        path -- the path of the raw image file, if not provided the current 
                image file is checked
        """
        self.is_raw = False
        try:
            self.check_file(filename)
        except TypeError:
            return False

        self.filename = filename
        self.identify()
        return self.is_raw

    def check_area(self, left, top, width, height):
        """Check the size of the area used for the white balance computing.

        """
        for i in (left, top, width, height):
            if i < 0:
                raise ValueError("Coordinates must be positives")

        if not width * height:
            raise ValueError("Size can't be null")

        w, h = self.data["image_size"]
        if left + width > w or top + height > h:
            raise ValueError("Area selected too big for the image")

    def valid_pgm(self, filename):
        """Check the validity of a pgm file used as dark frame.

        Args:
        filename -- absolute path of the pgm file
        """
        try:
            with open(filename, 'rb') as infile:
                block = list(infile.read(32))

            if block.pop(0) == ord(b'P') and block.pop(0) in b'25':
                values = []
                num = []
                for i in range(10):
                    c = block.pop(0)
                    if chr(c).isdigit():
                        num.append(chr(c))
                        while len(values) < 3:
                            c = block.pop(0)
                            if chr(c).isdigit():
                                num.append(chr(c))
                            else:
                                if num:
                                    values.append(int(''.join(num)))
                                    num = []
                        break
            else:
                return False
        except Exception as why:
            print("Pgm read error: ", why)
            raise

        if not (values[0], values[1]) == self.data["image_size"]:
            s = (values[0], values[1], self.data["image_size"][0], 
                 self.data["image_size"][0])
            raise PgmSizeError(s)

        if not values[2] == 65535:
            raise PgmEncodingError()

        return True

    def save_profile(self, fname, pickle_=False):
        """Save the profile on disk.

        Args:
        fname -- absolute path of the file to save the profile
        pickle_ -- if False (default) the profile will be saved as a json file, 
                   if True it will be pickled
        """
        with open(fname, 'wb') as outfile:
            if pickle_:
                pickle.dump(self.profile, outfile)

            else:
                jsn = json.dumps(self.profile, sort_keys=True, indent=4, 
                                 separators=(',', ': '), ensure_ascii=False)
                outfile.write(jsn.encode('utf-8', 'replace'))

    def read_profile(self, fname):
        """Read a profile from a file.

        The file must be pickled or write as a json file.

        Args:
        fname -- absolute path of the file
        """
        dic = False
        with open(fname, 'rb') as infile:
            try:
                dic = pickle.load(infile)
            except pickle.PickleError:
                # Try json
                cnt = infile.read()
                dic = json.loads(cnt)

        self.apply_new_profile(dic)

    def apply_new_profile(self, profile):
        """Apply a profile.

        Args:
        profile -- dict
        """
        for k, v in profile.items():
            print("%s\t%s" %(k, v))

        self.reset_profile()
        k = "white_balance"
        if k in profile:
            v = profile[k]
            if not v:
                self.ignore_white_balance()
            else:
                r1 = 0
                if len(v) == 3:
                    r, g, b = v
                else:
                    r, g, b, r1 = v
                self.set_white_balance(r, g, b, r1)

        k = "gamma"
        if k in profile:
            p, s = profile[k]
            self.set_gamma_curve(p, s)

        k = "chrom_aber"
        if k in profile:
            r, b = profile[k]
            self.enlarge_red_blue_layers(r, b)

        if "color_space" in profile:
            self.set_color_space(profile["color_space"])

        if "ICC" in profile:
            self.set_ICC_profile(profile["ICC"])

        if "noise_threshold" in profile:
            self.set_noise_threshold(profile["noise_threshold"])

        if "highlight" in profile:
            self.set_highlights(profile["highlight"])

        if "auto_wb"  in profile:
            x, y, w, h = profile["auto_wb"]
            self.find_white_balance(x, y, w, h)

        if "interpolation" in profile:
            self.set_interpolation_method(profile["interpolation"])

        if "clean_artifacts" in profile:
            self.clean_artifacts(profile["clean_artifacts"])

        if "darkness" in profile:
            self.set_darkness(profile["darkness"])

        if "saturation" in profile:
            self.set_saturation(profile["saturation"])

        if "brightness" in profile:
            self.set_brightness(profile["brightness"])

        if "16_bits" in profile:
            a, l = profile["16_bits"]
            self.write_sixteen_bits(a, l)

        if "write_tiff" in profile:
            self.set_output_format(False)

        if "orientation" in profile:
            self.set_orientation(profile["orientation"])

        if "fuji_rotate" in profile:
            self.rotate_fuji(False)

        if "dead_pixels" in profile:
            self.fix_dead_pixels(profile["dead_pixels"])

        if "dark" in profile:
            self.set_black_layer(profile["dark"])

        self.profile = profile
        
                
                

