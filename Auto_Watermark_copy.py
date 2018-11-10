#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import collections
import sys
# import time
# import psutil

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from PIL import Image as im
# from PIL import ImageQt


class DataBase:

    URL_START = r"file:///"

    FILE_TYPE = (".jpg", ".png", ".tga", ".tif")

    # MAX_CMD_RENDER_LOCATION = r"C:\Program Files\Autodesk\3ds Max 2014\3dsmaxcmd.exe"

    # PHOTOSHOP_LOCATION = r"C:\Program Files\Adobe\Adobe Photoshop CS6 (64 Bit)\Photoshop.exe"

    # WATER_MARK_LOCATION = r"T:\Digicom\RESOURSE\09_Scripts\PsAtnAiGroupWaterMark"
    # WATER_MARK_NAME_START = r"AiGroupPreviewWaterMark_1280_"
    WATER_MARK_LOCATION = r"water_mark_source_image"
    WATER_MARK_TYPE = ("Horzontal4_3", "Horzontal16_9", "Square1_1", "Vertical3_4", "Vertical9_16", "Folder")
    WATER_MARK_SIZE = ((1280, 960), (1280, 720), (1280, 1280), (960, 1280), (720, 1280), (0, 0))
    WATER_MARK_TOLERANCE = 5
    WATER_MARK_PROCESS_PROGRAM = r"water_mark_process.py" # python version
    # WATER_MARK_PROCESS_PROGRAM = r"go_process.exe" # go version
    WATER_MARK_BACKUP = os.path.join(os.getenv("TEMP"), "Auto_Water_Mark_Backup")

    WATER_MARK_RATIO = ((1280 / 960, (1280 - WATER_MARK_TOLERANCE) / 960, 1280 / (960 - WATER_MARK_TOLERANCE)),
                        (1280 / 720, (1280 - WATER_MARK_TOLERANCE) / 720, 1280 / (720 - WATER_MARK_TOLERANCE)),
                        (1280 / 1280, (1280 - WATER_MARK_TOLERANCE) / 1280, 1280 / (1280 - WATER_MARK_TOLERANCE)),
                        (960 / 1280, (960 - WATER_MARK_TOLERANCE) / 1280, 960 / (1280 - WATER_MARK_TOLERANCE)),
                        (720 / 1280, (720 - WATER_MARK_TOLERANCE) / 1280, 720 / (1280 - WATER_MARK_TOLERANCE)),
                        (0, 0, 0))

    auto_shade_collection = collections.namedtuple("auto_shade_group", "day night brighter")

    # AUTO_SHADING_HARD_COMMAND = r"T:\Digicom\RESOURSE\09_Scripts\PsAtnAutoShading\AutoShadingHard.exe"
    # AUTO_SHADING_HARD_COMMAND = r"F:\programming\auto_shade_sample\AutoShadingHard.exe"
    AUTO_SHADING_LOCATION = r"ps_auto_shading"
    AUTO_SHADING_HARD_COMMAND = r"AutoShadingHard.exe"
    AUTO_SHADING_DARK_COMMAND = r"AutoShadingNight.exe"
    AUTO_SHADING_BRIGHTER_COMMAND = r"AutoShadingBright.exe"

    # END_PHOTOSHOP_COMMAND = ["taskkill", "/im", "Photoshop.exe"]

    FOLDER_ICON = r"Folder-Icon.png"

    ICON_START_SIZE = 100
    ICON_MINIMUM = 100
    ICON_MAXIMUM = 300

    AUTO_SHADE_HISTOGRAM_EVALUATION_THRESHOLD = 128
    AUTO_SHADE_HISTOGRAM_DIFFERENCE_THRESHOLD = auto_shade_collection(0.115, 0.115, 0.3)
    # Bright Ratio of TTPC_KIT_C1_20150626_0003 = 153296.33333333334 / 768303.6666666666 = 0.166...
    # Bright Ratio of TTPC_STR_C1_20150622_0000 = 65811.66666666667 / 855788.3333333334 = 0.0714....
    # Bright Ratio of HSYM_KIT_20140710_0000 = 690999.3333333334 / 947400.6666666666 = 0.42175...

    AUTO_SHADE_TYPE = auto_shade_collection("day", "night", "brighter")
    AUTO_SHADE_COMMAND = auto_shade_collection(AUTO_SHADING_HARD_COMMAND, AUTO_SHADING_DARK_COMMAND,
                                               AUTO_SHADING_BRIGHTER_COMMAND)

    GO_SERVER = r"go_server.exe"
    END_GO_SERVER_COMMAND = ["taskkill", "/im", "go_server.exe"]


class MainUI(qw.QDialog):

    def __init__(self):

        super(MainUI, self).__init__()

        # self.setObjectName("self")
        # self.resize(820, 975)

        font = qg.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.setObjectName("self")
        self.resize(900, 1000)
        self.verticalLayout_2 = qw.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # self.setStyleSheet("background: rgb(75, 75, 75);"
        #                    "color: rgb(235, 235, 235);")

        self.text_raw_render_output = qw.QPlainTextEdit(self)
        self.text_raw_render_output.setMinimumSize(qc.QSize(0, 0))
        self.text_raw_render_output.setMaximumSize(qc.QSize(16777215, 40))
        self.text_raw_render_output.setObjectName("plainTextEdit")
        self.text_raw_render_output.setPlaceholderText("The Output Path of Rendering")
        self.text_raw_render_output.setFont(font)
        self.text_raw_render_output.setEnabled(False)
        self.verticalLayout_2.addWidget(self.text_raw_render_output)

        self.text_final_output = qw.QPlainTextEdit(self)
        self.text_final_output.setMaximumSize(qc.QSize(16777215, 40))
        self.text_final_output.setObjectName("plainTextEdit_2")
        self.text_final_output.setPlaceholderText("Path to store the water-marked and auto-shaded image")
        self.text_final_output.setFont(font)
        self.text_final_output.setEnabled(False)
        self.verticalLayout_2.addWidget(self.text_final_output)

        self.widget = qw.QWidget(self)
        self.widget.setMinimumSize(qc.QSize(0, 30))
        self.widget.setMaximumSize(qc.QSize(16777215, 50))
        self.widget.setObjectName("widget")

        self.horizontalLayout_2 = qw.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.check_render_and_comp = qw.QCheckBox(self.widget)
        self.check_render_and_comp.setMinimumSize(qc.QSize(0, 10))
        self.check_render_and_comp.setFont(font)
        self.check_render_and_comp.setObjectName("checkBox_6")
        self.check_render_and_comp.setText("Render and Comp")
        self.horizontalLayout_2.addWidget(self.check_render_and_comp)

        self.check_render_and_comp.clicked.connect(self.render_comp_check)

        self.vertical_line_render_comp = qw.QFrame(self.widget)
        self.vertical_line_render_comp.setFrameShape(qw.QFrame.VLine)
        self.vertical_line_render_comp.setFrameShadow(qw.QFrame.Sunken)
        self.vertical_line_render_comp.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.vertical_line_render_comp)

        self.check_server_mode = qw.QCheckBox(self.widget)
        self.check_server_mode.setMinimumSize(qc.QSize(0, 10))
        self.check_server_mode.setFont(font)
        self.check_server_mode.setObjectName("checkBox_5")
        self.check_server_mode.setText("Server Mode")
        self.check_server_mode.setEnabled(False)
        self.horizontalLayout_2.addWidget(self.check_server_mode)
        self.verticalLayout_2.addWidget(self.widget)

        self.check_server_mode.setChecked(True)
        self.check_server_mode.clicked.connect(self.server_mode_check)

        self.check_duplicate_original = qw.QCheckBox(self.widget)
        self.check_duplicate_original.setMinimumSize(qc.QSize(0, 10))
        self.check_duplicate_original.setFont(font)
        self.check_duplicate_original.setObjectName("checkBox_7")
        self.check_duplicate_original.setText("Duplicate Original File")
        self.check_duplicate_original.setEnabled(False)
        self.check_duplicate_original.setChecked(True)
        self.horizontalLayout_2.addWidget(self.check_duplicate_original)
        self.verticalLayout_2.addWidget(self.widget)

        self.button_run = qw.QPushButton(self)
        self.button_run.setEnabled(True)
        self.button_run.setMinimumSize(qc.QSize(0, 40))
        self.button_run.setFont(font)
        self.button_run.setObjectName("pushButton")
        self.button_run.setText("Run!!")
        self.button_run.setEnabled(False)
        self.verticalLayout_2.addWidget(self.button_run)

        self.button_run.clicked.connect(self.run_button_click)

        self.verticalLayout = qw.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontal_line = qw.QFrame(self)
        self.horizontal_line.setFrameShape(qw.QFrame.HLine)
        self.horizontal_line.setFrameShadow(qw.QFrame.Sunken)
        self.horizontal_line.setObjectName("line")
        self.verticalLayout.addWidget(self.horizontal_line)

        self.label_file_list = qw.QLabel(self)
        self.label_file_list.setFont(font)
        self.label_file_list.setObjectName("label_3")
        self.label_file_list.setText("File List")
        self.verticalLayout.addWidget(self.label_file_list)

        self.file_list = NameList(self)
        self.file_list.setObjectName("listWidget")
        self.file_list.setFont(font)
        self.verticalLayout.addWidget(self.file_list)

        self.slider = qw.QSlider(self)
        self.slider.setMinimumSize(qc.QSize(0, 30))
        self.slider.setOrientation(qc.Qt.Horizontal)
        self.slider.setObjectName("horizontalSlider")
        self.slider.setMinimum(DataBase.ICON_MINIMUM)
        self.slider.setMaximum(DataBase.ICON_MAXIMUM)
        self.slider.setValue(DataBase.ICON_START_SIZE)
        self.verticalLayout.addWidget(self.slider)

        self.slider.valueChanged.connect(lambda: self.file_list.slider_change_icon_size(self.slider.value()))

        self.button_clear = qw.QPushButton(self)
        self.button_clear.setMinimumSize(qc.QSize(0, 30))
        self.button_clear.setFont(font)
        self.button_clear.setObjectName("pushButton_3")
        self.button_clear.setText("Clear")
        self.verticalLayout.addWidget(self.button_clear)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.button_clear.clicked.connect(self.file_list.clear_button_event)

        self.verticalLayout_3 = qw.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.horizontalLayout = qw.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.check_water_mark = qw.QCheckBox(self)
        self.check_water_mark.setFont(font)
        self.check_water_mark.setObjectName("checkBox")
        self.check_water_mark.setText("Water Mark")
        self.check_water_mark.setChecked(True)
        self.horizontalLayout.addWidget(self.check_water_mark)

        self.check_auto_curve = qw.QCheckBox(self)
        self.check_auto_curve.setFont(font)
        self.check_auto_curve.setObjectName("checkBox_2")
        self.check_auto_curve.setText("Auto Shade")
        self.check_auto_curve.setChecked(False)
        self.horizontalLayout.addWidget(self.check_auto_curve)

        self.vertical_line = qw.QFrame(self)
        self.vertical_line.setFrameShape(qw.QFrame.VLine)
        self.vertical_line.setFrameShadow(qw.QFrame.Sunken)
        self.vertical_line.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.vertical_line)

        # self.check_ufo_ratio = qw.QCheckBox(self)
        # self.check_ufo_ratio.setMinimumSize(qc.QSize(0, 35))
        # self.check_ufo_ratio.setFont(font)
        # self.check_ufo_ratio.setObjectName("checkBox_3")
        # self.check_ufo_ratio.setText("UFO Auto Detect")
        # self.horizontalLayout.addWidget(self.check_ufo_ratio)

        self.check_recursive = qw.QCheckBox(self)
        self.check_recursive.setFont(font)
        self.check_recursive.setObjectName("checkBox_4")
        self.check_recursive.setText("Recursive")
        self.horizontalLayout.addWidget(self.check_recursive)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.button_go = qw.QPushButton(self)
        self.button_go.setMinimumSize(qc.QSize(0, 40))
        self.button_go.setFont(font)
        self.button_go.setObjectName("pushButton_2")
        self.button_go.setText("Go!!")
        self.verticalLayout_3.addWidget(self.button_go)

        self.button_go.clicked.connect(self.go_button_clicked)

        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.ufo_ratio = set()

        self.output_dict = {}
        self.output_dict_renew()

        self.auto_shade_dict = {}
        self.auto_shade_dict_renew()
        self.server_running = False
        # self.go_button_running = False

        self.check_auto_curve.setEnabled(False)
        # self.check_render_and_comp.setEnabled(False)

    def run_button_click(self):

        if self.server_running is False:

            raw_render = self.text_raw_render_output.toPlainText().replace(DataBase.URL_START, "")
            final_path = self.text_final_output.toPlainText().replace(DataBase.URL_START, "")

            if not raw_render or not os.path.isdir(raw_render):
                qw.QMessageBox.information(qw.QMessageBox(), "Information", "Please specify the path of render output")
                return

            if not final_path or not os.path.isdir(final_path):
                qw.QMessageBox.information(qw.QMessageBox(), "Information",
                                           "Please specify the path to store the final output")
                return

            subprocess.Popen([DataBase.GO_SERVER, raw_render, final_path])
            self.button_run.setText("Program is Running")
            self.button_run.setStyleSheet("color: red")
            self.server_running = True

        else:
            subprocess.Popen(DataBase.END_GO_SERVER_COMMAND)
            self.button_run.setText("Run!!")
            self.button_run.setStyleSheet("color: black")
            self.server_running = False

    def auto_shade_dict_renew(self):

        for i in DataBase.AUTO_SHADE_TYPE:
            self.auto_shade_dict[i] = []

    def output_dict_renew(self):

        for i in DataBase.WATER_MARK_TYPE:
            self.output_dict[i] = []

    def render_comp_check(self):

        if self.check_server_mode.isChecked():
            self.check_duplicate_original.setEnabled(not self.check_duplicate_original.isEnabled())

        self.text_raw_render_output.setEnabled(not self.text_raw_render_output.isEnabled())
        self.text_final_output.setEnabled(not self.text_final_output.isEnabled())
        self.check_server_mode.setEnabled(not self.check_server_mode.isEnabled())
        self.button_run.setEnabled(not self.button_run.isEnabled())

    def server_mode_check(self):

        self.check_duplicate_original.setEnabled(self.check_server_mode.isChecked())

        if self.check_server_mode.isChecked():
            self.text_final_output.setPlaceholderText("Alternative Path to store the water_marked image")

        else:
            self.text_final_output.setPlaceholderText("Folder Path for Render Output")

    @staticmethod
    def image_size_dict_distribution(file, func, output, ufo, shade):

        if os.path.splitext(file)[-1].lower() not in DataBase.FILE_TYPE:
            return

        image = im.open(file)
        x, y = image.size

        histogram = image.histogram()
        red = histogram[0:256]
        green = histogram[256:256*2]
        blue = histogram[256 * 2:256 * 3]

        red_dark = 0
        green_dark = 0
        blue_dark = 0

        red_btight = 0
        green_bright = 0
        blue_bright = 0

        for i in range(0, 256):

            if i <= DataBase.AUTO_SHADE_HISTOGRAM_EVALUATION_THRESHOLD:
                red_dark += red[i]
                green_dark += green[i]
                blue_dark += blue[i]

            else:
                red_btight += red[i]
                green_bright += green[i]
                blue_bright += blue[i]

#####

        dark_luminance_average = (red_dark + green_dark + blue_dark) / 3
        bright_luminance_average = (red_btight + green_bright + blue_bright) / 3
        # print("bright_average: {0}".format(bright_luminance_average))
        # print("dark_average: {0}".format(dark_luminance_average))

        bright_ratio = bright_luminance_average / (bright_luminance_average + dark_luminance_average)

        if bright_ratio > DataBase.AUTO_SHADE_HISTOGRAM_DIFFERENCE_THRESHOLD.brighter:
            shade[DataBase.AUTO_SHADE_TYPE.brighter].append(os.path.basename(file))

        elif bright_ratio > DataBase.AUTO_SHADE_HISTOGRAM_DIFFERENCE_THRESHOLD.day:
            shade[DataBase.AUTO_SHADE_TYPE.day].append(os.path.basename(file))

        else:
            shade[DataBase.AUTO_SHADE_TYPE.night].append(os.path.basename(file))
#####

        if (x, y) not in DataBase.WATER_MARK_SIZE:
                ufo.add(file)

        else:
            for j in range(len(DataBase.WATER_MARK_SIZE)):
                # func(5, (x, y), DataBase.WATER_MARK_SIZE[j], output[DataBase.WATER_MARK_TYPE[j]], file)
                func((x, y), DataBase.WATER_MARK_RATIO[j], output[DataBase.WATER_MARK_TYPE[j]], file)

        image.close()

    @staticmethod
    def image_size_check_ratio(input_parm, compare_parm, output_item, output_append_item):

        if compare_parm[1] <= input_parm[0] / input_parm[1] <= compare_parm[2]:
            output_item.append(output_append_item)

    @staticmethod
    def image_size_check_pixel(tolerance, input_parm, compare_parm, output_item, output_append_item):

        if compare_parm[0] - tolerance <= input_parm[0] <= compare_parm[0] + tolerance:
            if compare_parm[1] - tolerance <= input_parm[1] <= compare_parm[1] + tolerance:
                output_item.append(output_append_item)

    def go_button_clicked(self):

        if not self.check_water_mark.isChecked() and not self.check_auto_curve.isChecked():
            qw.QMessageBox.information(qw.QMessageBox(), "Information",
                                       "Please at least select one operation to perform")
            return

        if not self.file_list.contain:
            qw.QMessageBox.information(qw.QMessageBox(), "Information", "There is no item in the list!")
            return

        self.button_go.setText("Program is Running!!")
        self.button_go.setStyleSheet("color: red")

        if not os.path.exists(DataBase.WATER_MARK_BACKUP):
            os.mkdir(DataBase.WATER_MARK_BACKUP)

        if os.listdir(DataBase.WATER_MARK_BACKUP):

            for i in os.listdir(DataBase.WATER_MARK_BACKUP):
                os.remove(os.path.join(DataBase.WATER_MARK_BACKUP, i))

        for i in self.file_list.contain:
            print("Distribution: {0}".format(i))

            if os.path.isfile(i):
                self.image_size_dict_distribution(i, self.image_size_check_ratio, self.output_dict,
                                                  self.ufo_ratio, self.auto_shade_dict)

            # if os.path.isfile(i):
            #     image = im.open(i)
            #     x, y = image.size
            #
            #     if (x, y) not in DataBase.WATER_MARK_SIZE:
            #             self.ufo_ratio.add(i)
            #
            #     else:
            #         for j in range(len(DataBase.WATER_MARK_SIZE)):
            #             self.image_size_check(5, (x, y), DataBase.WATER_MARK_SIZE[j],
            #                                   self.output_dict[DataBase.WATER_MARK_TYPE[j]], i)
            #     image.close()

            if os.path.isdir(i):

                if not self.check_recursive.isChecked():

                    for j in os.listdir(i):
                        file_path = os.path.join(i, j)

                        if os.path.isfile(file_path):
                            print("Distribution: {0}".format(file_path))
                            self.image_size_dict_distribution(file_path, self.image_size_check_ratio,
                                                              self.output_dict, self.ufo_ratio, self.auto_shade_dict)

                else:

                    for roots, dirs, files in os.walk(i):

                        for j in files:
                            file_path = os.path.join(roots, j)

                            if os.path.isfile(file_path):
                                print("Distribution: {0}".format(file_path))
                                self.image_size_dict_distribution(file_path, self.image_size_check_ratio,
                                                                  self.output_dict, self.ufo_ratio,
                                                                  self.auto_shade_dict)

        for i in self.output_dict:

            if self.output_dict[i]:

                for j in self.output_dict[i]:

                    self.process_command(i, j)

                    # water_mark_command = []
                    # water_mark_command_path = os.path.join(DataBase.WATER_MARK_LOCATION,
                    #                                        DataBase.WATER_MARK_NAME_START + i + ".exe")
                    #
                    # water_mark_command.append(water_mark_command_path)
                    # file_path = os.path.abspath(j)
                    # water_mark_command.append(file_path)
                    #
                    # if self.check_auto_curve.isChecked():
                    #     subprocess.Popen([DataBase.AUTO_CURVE_COMMAND, file_path])
                    #
                    # if self.check_water_mark.isChecked():
                    #     subprocess.Popen(water_mark_command)

            # try:
            #     for process in psutil.process_iter():
            #         if process.name() == DataBase.END_PHOTOSHOP_COMMAND[2]:
            #             subprocess.call(DataBase.END_PHOTOSHOP_COMMAND)
            #
            # except psutil.Error as err:
            #     # print(err)
            #     pass

        # if execution:
        #     subprocess.call(DataBase.END_PHOTOSHOP_COMMAND)
            # subprocess.Popen(DataBase.END_PHOTOSHOP_COMMAND)
        # process = subprocess.Popen(DataBase.PHOTOSHOP_LOCATION)
        # process.terminate()

        self.file_list.clear()
        self.file_list.contain.clear()
        self.output_dict_renew()
        self.button_go.setText("Go!!")
        self.button_go.setStyleSheet("color: black")

    def process_command(self, ratio_key, value_element):

        water_mark_command = []
        # water_mark_template_path = os.path.join(DataBase.WATER_MARK_LOCATION,
        #                                        DataBase.WATER_MARK_NAME_START + ratio_key + ".exe")
        water_mark_template_path = os.path.join(DataBase.WATER_MARK_LOCATION, ratio_key + ".png")

        water_mark_command.append(sys.executable) # python version
        water_mark_command.append(DataBase.WATER_MARK_PROCESS_PROGRAM)

        water_mark_command.append(water_mark_template_path)
        file_path = os.path.abspath(value_element)
        water_mark_command.append(file_path)

        if self.check_auto_curve.isChecked():
            auto_shade_command = []
            # print(self.auto_shade_dict)

            if os.path.basename(file_path) in self.auto_shade_dict[DataBase.AUTO_SHADE_TYPE.brighter]:
                auto_shade_command.append(os.path.join(DataBase.AUTO_SHADING_LOCATION,
                                                       DataBase.AUTO_SHADE_COMMAND.brighter))

            elif os.path.basename(file_path) in self.auto_shade_dict[DataBase.AUTO_SHADE_TYPE.day]:
                auto_shade_command.append(os.path.join(DataBase.AUTO_SHADING_LOCATION,
                                                       DataBase.AUTO_SHADE_COMMAND.day))

            else:
                auto_shade_command.append(os.path.join(DataBase.AUTO_SHADING_LOCATION,
                                                       DataBase.AUTO_SHADE_COMMAND.night))

            auto_shade_command.append(file_path)
            # print("{0}: {1}".format(file_path, auto_shade_command[0]))

            subprocess.call(auto_shade_command)
            # subprocess.Popen([DataBase.AUTO_CURVE_COMMAND, file_path])
            # subprocess.call([DataBase.AUTO_CURVE_COMMAND, file_path])

        if self.check_water_mark.isChecked():
            subprocess.Popen(water_mark_command)
            # subprocess.call(water_mark_command)


class NameList(qw.QListWidget):

    def __init__(self, dialog):

        super(NameList, self).__init__(dialog)

        self.setAcceptDrops(True)
        self.setDragDropMode(qw.QAbstractItemView.DropOnly)
        self.setDefaultDropAction(qc.Qt.CopyAction)
        self.setSelectionMode(qw.QAbstractItemView.ExtendedSelection)
        self.setIconSize(qc.QSize(DataBase.ICON_START_SIZE, DataBase.ICON_START_SIZE))

        self.contain = set()
        # self.output_dict = {}
        # self.ufo_ratio = set()

        # for i in DataBase.WATER_MARK_TYPE:
        #     self.output_dict[i] = []
        #
        # self.output_dict["Folder"] = []
        # print(self.output_dict.keys())
    # def mouseReleaseEvent(self, *args, **kwargs):
    #     self.clearSelection()

    # def add_item_from_contain_set(self):
    #
    #     for i in self.contain:
    #
    #         if os.path.isfile(i):
    #             icon = qg.QIcon(i)
    #
    #         elif os.path.isdir(i):
    #             icon = qg.QIcon(DataBase.FOLDER_ICON)
    #
    #         item = qw.QListWidgetItem(os.path.basename(i), self)
    #         item.setIcon(icon)
    #         self.addItem(item)

    def slider_change_icon_size(self, size):

        self.setIconSize(qc.QSize(size, size))

    def clear_button_event(self):

        if self.selectedItems():

            for i in self.selectedItems():
                self.takeItem(self.row(i))
                temp_set = set()

                for j in self.contain:

                    if i.text() in j:
                        temp_set.add(j)

                self.contain.difference_update(temp_set)

        else:
            return

    # @staticmethod
    # def image_size_check(tolerance, input_parm, compare_parm, output_item, output_append_item):
    #
    #     if compare_parm[0] - tolerance <= input_parm[0] <= compare_parm[0] + tolerance:
    #         if compare_parm[1] - tolerance <= input_parm[1] <= compare_parm[1] + tolerance:
    #             output_item.append(output_append_item)

    def dragEnterEvent(self, event):

        self.clear()
        event.setDropAction(qc.Qt.CopyAction)
        event.accept()
        # print(event.mimeData().urls()[0].toLocalFile())
        # print(event.mimeData().urls()[0].toString())

        for file in event.mimeData().urls():
            url = file.toLocalFile()
            self.contain.add(url)

            # image = im.open(r"Folder-Icon.png")
            # print(image.size)
            # url = r"Folder-Icon.png"

        # self.add_item_from_contain_set()

        for i in self.contain:

            if os.path.isfile(i):
                icon = qg.QIcon(i)

                # image = im.open(i)
                # x, y = image.size
                # # print(x, y)
                #
                # if (x, y) not in DataBase.WATER_MARK_SIZE:
                #         self.ufo_ratio.add(i)
                #
                # else:
                #
                #     for j in range(len(DataBase.WATER_MARK_SIZE)):
                #         # print(DataBase.WATER_MARK_SIZE[j])
                #
                #         self.image_size_check(5, (x, y), DataBase.WATER_MARK_SIZE[j],
                #                               self.output_dict[DataBase.WATER_MARK_TYPE[j]], i)
                #
                # image.close()

            elif os.path.isdir(i):
                icon = qg.QIcon(DataBase.FOLDER_ICON)
                # self.output_dict[DataBase.WATER_MARK_TYPE[5]].append(i)

            item = qw.QListWidgetItem(os.path.basename(i), self)
            item.setIcon(icon)
            self.addItem(item)

        # print(self.output_dict)

        # print(self.unidentified_ratio)

        # pixel_map = icon.pixmap(150, 150)
        # icon = qg.QIcon(pixel_map)
        # picture = Image.open(url)
        # picture.thumbnail((150, 150), Image.ANTIALIAS)
        # icon = qg.QIcon(qg.QPixmap.fromImage(ImageQt.ImageQt(picture)))
        # item.setText("test")
        # item.setStatusTip(url)

    def dragMoveEvent(self, event):

        event.setDropAction(qc.Qt.CopyAction)
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(qc.Qt.IgnoreAction)
        event.ignore()

    # def picture_dropped(self, l):
    #     # for url in l:
    #     # if os.path.exists(url):
    #     url = r"E:\桌面背景\1.jpg"
    #     picture = Image.open(url)
    #     picture.thumbnail((72, 72), Image.ANTIALIAS)
    #     icon = qg.QIcon(qg.QPixmap.fromImage(ImageQt.ImageQt(picture)))
    #     item = qw.QListWidgetItem(self)
    #     item.setStatusTip(url)
    #     item.setIcon(icon)


if __name__ == '__main__':
    # print(DataBase.WATER_MARK_TYPE.h14_3)
    app = qw.QApplication(sys.argv)
    di = MainUI()
    di.show()
    sys.exit(app.exec_())
    # print(os.path.splitext(DataBase.AUTO_SHADING_HARD_COMMAND)[-1])


