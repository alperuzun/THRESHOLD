import os
import sys
import csv
import shutil
import subprocess
import matplotlib
import numpy as np
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtGui import QCursor
from threshold_ranking import rank
from threshold_graph import make_file
from threshold_calculate import top50
from threshold_ttest import check_for_statistical_significance
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import PyQt6.QtCore
from threshold_return_path import path as path1

path = path1
global ready
ready = False

def main_reset():
    to_remove = ["cleaned_data.txt","data.txt","graph.txt","ranks.json","removed_genes.txt","stat1.txt","stat2.txt","result_statistics.txt"]

    for item in to_remove:
        if os.path.exists(path+item):
            try:
                os.remove(path+item)
                print(f"{item} deleted.")
            except OSError as e:
                print(f"Error deleting: {e}")
        else:
            print(f"{item} already reset.")   

main_reset()

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(10) 
        layout.setContentsMargins(2, 3, 2, 2)

        info_layout = QHBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.info_button = QPushButton()
        self.info_button.setFixedSize(30, 30)
        self.info_button.setStyleSheet("background-color: transparent; margin-top: -10px;")
        self.info_button.setIcon(QIcon(path+"assets/info.png")) 
        self.info_button.clicked.connect(self.info)

        self.documentation_button = QPushButton()
        self.documentation_button.setFixedSize(30, 30)
        self.documentation_button.setStyleSheet("background-color: transparent; margin-left: -20px; margin-top: -10px;")
        self.documentation_button.setIcon(QIcon(path+"assets/doc.png")) 
        self.documentation_button.clicked.connect(self.documentation)

        info_layout.addWidget(self.info_button)
        info_layout.addWidget(self.documentation_button)

        layout.addLayout(info_layout)

        spacer1 = QSpacerItem(100, 130, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer1)

        svg_widget = QSvgWidget(path+'assets/logo.svg')
        svg_widget.setFixedSize(266, 50)
        layout.addWidget(svg_widget)

        text_label = QLabel('Open a .txt file to begin \n analyzing gene saturation', self)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        text_label.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(text_label)

        button = QPushButton('Open File', self)
        button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        layout.addWidget(button)
        button.clicked.connect(self.open_pdf)
        
        spacer_pg = QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer_pg)

        row_layout1 = QHBoxLayout()
        row_layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pgene_checkbox = QCheckBox()
        self.pgene_checkbox.setStyleSheet("background-color: transparent; margin-right: 0px; margin-left: 5px;")

        self.pg_label = QLabel(f"Include pseudogenes", self)
        self.pg_label.setStyleSheet("font-size: 16px; color: white; margin-left: 0px; background-color: transparent; padding: 0; margin-right: 0;")

        row_layout1.addWidget(self.pgene_checkbox)
        row_layout1.addWidget(self.pg_label)

        layout.addLayout(row_layout1)



        button_stat = QPushButton(' Run Statistical Analysis  ', self)
        button_stat.setIcon(QIcon(path+"assets/stat.png")) 
        button_stat.setStyleSheet("font-size: 14px; color: white; background-color: #325BA9; border: none; font-weight: bold;")
        button_stat.clicked.connect(self.stat_page)

        spacer2 = QSpacerItem(280, 180, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer2)
        
        layout.addWidget(button_stat)

    def info(self):
        text = "   THRESHOLD is a novel gene saturation analysis GUI. THRESHOLD analyzes transcriptomic data across large samples of patients to understand the cohesion of the most upregulated/downregulated genes in a given disease. This lends researchers knowledge to inform network topology analyses or to assess the relative amount of genes influencing a given disease. THRESHOLD offers several features to aid in analysis including user-inputted saturation type, restriction factors, and rank type. The tool outputs an interactive graph of saturation permitting the calculation of specific saturation thresholds and most saturated genes.\n\n   THRESHOLD was developed by Finán Gammell, Jennifer Li, Dr. Jessica Plavicki, Dr. Christopher Elco, and Dr. Alper Uzun in the Uzun Lab at the Brown Center for Biomedical Informatics at Brown University."
        message_box = CustomMessageBox(text, "info", 380, self)
        message_box.setWindowTitle("Info")
        message_box.exec()

    def documentation(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(path+"assets/notes.pdf"))

    def open_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Txt', os.path.expanduser("~"), 'Txt Files (*.txt)')
        if file_path:
            current_path = os.path.dirname(os.path.realpath(__file__))
            new_path = os.path.join(current_path, os.path.basename(file_path))
            
            shutil.copyfile(file_path, new_path)
            
            renamed_path = os.path.join(current_path, "data.txt")
            os.rename(new_path, renamed_path)
            
            if os.path.exists(path+"removed_genes.txt"):
                try:
                    os.remove(path+"removed_genes.txt")
                    print(f"Removed file deleted.")
                except OSError as e:
                    print(f"Error deleting: {e}")
            else:
                pass
            
            if self.pgene_checkbox.isChecked() != True:
                subprocess.run(["java", "-cp", path, "clean2"], check=True)
            else:
                os.rename("data.txt", "cleaned_data.txt")
                with open("removed_genes.txt", "w"):
                    pass
           


            if os.path.exists(path+"removed_genes.txt"):
                with open(path+"removed_genes.txt", "r") as file:
                    lines = file.readlines()
                    non_empty_lines = [line for line in lines if line.strip()]

                with open(path+"removed_genes.txt", "w") as file:
                    file.writelines(non_empty_lines)

                print("Empty rows removed from the file.")
            
            file_name = os.path.basename(file_path)

            if len(file_name) >= 20:
                file_name = file_name[:16] + "....txt"

            Page2.change(file_name)

            self.parent().setCurrentIndex(1)

    def stat_page(self):
        self.parent().setCurrentIndex(3)

class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, reverseV, number, factor):
        super().__init__()
        self.reverseV = reverseV
        self.number = number
        self.factor = factor

    def run(self):
        rank(self.reverseV)
        make_file(self.number, self.factor)
        self.finished.emit()


class Page2(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10) 
        layout.setContentsMargins(2, 3, 2, 2)

        self.back_button = QLabel()
        self.back_button.setStyleSheet("background: transparent;")
        self.back_button.setFixedSize(28, 28)

        svg_widget = QSvgWidget(path+'assets/logo.svg')
        svg_widget.setStyleSheet("margin-bottom: -20px; margin-left: -10px;")
        svg_widget.setFixedSize(160, 30)

        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon(path+"assets/reset.png")) 
        self.reset_button.setStyleSheet("background: transparent; margin-left: 5px;")
        self.reset_button.setFixedSize(30, 30)

        self.reset_button.clicked.connect(self.reset)

        space1 = QSpacerItem(18, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        space2 = QSpacerItem(39, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        row_layout5 = QHBoxLayout()
        row_layout5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        row_layout5.addWidget(self.back_button)
        row_layout5.addItem(space1)

        row_layout5.addWidget(svg_widget)
        row_layout5.addItem(space2)

        row_layout5.addWidget(self.reset_button)

        row_layout5.setContentsMargins(-20,-50,-20,-20)

        layout.addLayout(row_layout5)

        self.progress = QLabel("<i>In progress...</i>")
        self.progress.setStyleSheet("font-size: 18px; color: #325ca9; margin-top: 8px;")
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.addWidget(self.progress)

        label = QLabel('Graph', self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        label.setStyleSheet("font-size: 20px; color: white; font-weight: bold; margin-top: 8px;")
        layout.addWidget(label)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)  
        layout.addLayout(row_layout)

        field1 = QLabel('Calculate Until:<sup>ⓘ</sup>', self)
        field1.setStyleSheet("font-size: 16px; color: white;")
        field1.mousePressEvent = lambda event: self.info_display("cal_unt")
        row_layout.addWidget(field1)

        self.input = QTextEdit(self)
        self.input.setStyleSheet("font-size: 16px; max-width: 200px; max-height: 22px; color: white; border: 1px solid white; background-color: orange;")
        self.input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  
        row_layout.addWidget(self.input)

        radio1layout = QHBoxLayout()
        radio1layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio1layout.setSpacing(0)

        self.radio1 = QRadioButton()
        self.radio1.setText(f'Overall Saturation')
        self.radio1.setStyleSheet("font-size: 16px; color: white; margin-bottom: 0; QRadioButton::indicator:checked { background-color: orange; }")

        self.radio1label = QLabel("<sub>ⓘ</sub>")
        self.radio1label.setStyleSheet("font-size: 16px; color: white; margin-bottom: 0px; margin-left: 25px; margin-top: 5px;")
        self.radio1label.mousePressEvent = lambda event: self.info_display("ove_sat")

        radio1layout.addWidget(self.radio1)
        radio1layout.addWidget(self.radio1label)

        radio2layout = QHBoxLayout()
        radio2layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        radio2layout.setSpacing(0)

        self.radio2 = QRadioButton()
        self.radio2.setText(f'Incremental Saturation')
        self.radio2.setStyleSheet("font-size: 16px; color: white; margin-right: -1px;")

        radio2layout.addWidget(self.radio2)

        sub_layout = QVBoxLayout()
        sub_layout.setSpacing(0)
    
        sub_layout.addLayout(radio1layout)
        sub_layout.addLayout(radio2layout)

        layout.addLayout(sub_layout)

        row_layout2 = QHBoxLayout()
        row_layout2.setSpacing(5) 

        fix_layout = QVBoxLayout()
        fix_layout.setSpacing(4)
        fix_layout.addLayout(row_layout2)

        field2 = QLabel('Restriction Level:<sup>ⓘ</sup> ', self)
        field2.setStyleSheet("font-size: 16px; color: white;")
        field2.mousePressEvent = lambda event: self.info_display("res_lev")
        row_layout2.addWidget(field2)

        self.input2 = QTextEdit(self)
        self.input2.setStyleSheet("font-size: 16px; width: 15px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 0px; margin-right: 3px;")
        self.input2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  
        row_layout2.addWidget(self.input2)
        
        self.checkboxA = QCheckBox()
        self.checkboxA.setStyleSheet("background-color: transparent; margin-right: 0px; margin-left: 5px;")
        row_layout2.addWidget(self.checkboxA)

        self.percentlabel = QLabel(f" (%)", self)
        self.percentlabel.setStyleSheet("font-size: 16px; color: white; margin-left: 0px; background-color: transparent; padding: 0; margin-right: 0;")
        row_layout2.addWidget(self.percentlabel)

        row_layout3 = QHBoxLayout()
        row_layout3.setSpacing(0)

        labelT = QLabel('Reverse Ranking<sup>ⓘ</sup>')
        labelT.setStyleSheet("font-size: 16px; color: white; ")
        labelT.mousePressEvent = lambda event: self.info_display("rev_ran")
        row_layout3.addWidget(labelT)

        self.checkboxT = QCheckBox()
        self.checkboxT.setStyleSheet("background-color: transparent;")
        row_layout3.addWidget(self.checkboxT)

        fix_layout.addLayout(row_layout3)  

        layout.addLayout(fix_layout)        

        button = QPushButton('Generate')
        button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold; min-height: 22px; margin-top: 10px;")
        layout.addWidget(button)

        self.label2 = QLabel("Invalid; must enter number of genes\n(1-10,000), saturation type and level (1-100).")
        self.label2.setStyleSheet("font-size: 14px; color: orange;")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.addWidget(self.label2)

        Page2.importedL = QLabel()
        Page2.importedL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Page2.importedL.setStyleSheet("font-size: 14px; color: white; margin-top: 10px;")
        layout.addWidget(Page2.importedL)

        button.clicked.connect(self.generate)
        self.label2.hide()

        spacer_bottom = QSpacerItem(20, 150)
        layout.addItem(spacer_bottom)

    def info_display(self, element):

        if element == "cal_unt":
            text = "Enter the number of genes you want to calculate saturation for. For example, if you want to rank 100 genes and calculate the saturation at each rank, enter 100.\n\nYou may enter any integer between 1-10,000."
            title =  "Calculate Until"
            height = 120
        if element == "ove_sat":
            text = "This is where you select the saturation type that you would like to view on the graph. Note data from both saturation types can be downloaded in the interface regardless of your selection. \n\nOverall saturation determines the percentage of saturated genes up to including the nth level in each increasing value of n, while incremental saturation considers only the percentage of saturated genes at that specific nth level in each increasing value of n.\n\nSee documentation for more info on how each type of saturation is calculated."
            title = "Saturation Type"
            height = 270
        if element == "res_lev":
            text = "Enter the restriction level where saturation is reached. For example, if you want to consider the second occurence of a gene as saturated, input 2.\n\nAlternatively you can enter a percentage, which will be rounded to a number of genes. Check the '(%)' box if this is the case.\n\nIn either scenario, you may enter any integer between 2-100."
            title = "Restriction Level"
            height = 200
        if element == "rev_ran":
            text = "By checking this box you rank genes from low to high expression as opposed to high to low expression.\n\nThis may be useful to determine saturation of downregulated genes.\n\nYou may leave this box unchecked if you want to rank high to low expression."
            title = "Reverse Rank"
            height = 170
 
        message_box = CustomMessageBox(text, "info", height, self)
        message_box.setWindowTitle(title)
        message_box.exec()

    def change(file_name):
        Page2.importedL.setText(f"'{file_name}' uploaded.")

    def reset(self):
        main_reset()
            
        self.parent().setCurrentIndex(0)

    def generate(self):
        global ready
        ready = False
        try:
            number_of_genes = self.input.toPlainText().replace(",","")

            global factor
            factor = int(self.input2.toPlainText().replace(",",""))

            global number
            number = int(number_of_genes)

            if number >= 1 and number <= 10000:
                global sat_type 
                if self.radio1.isChecked():
                    sat_type = "overall_saturation"
                    ready = True
                elif self.radio2.isChecked():
                    sat_type = "incremental_saturation"
                    ready = True
                else:
                    self.label2.show()
                    ready = False

            if factor < 1:
                self.label2.show()
                ready = False
            if factor > 100:
                self.label2.show()
                ready = False
   
        
            if self.checkboxA.isChecked():
                pass
            else:
                factor = factor + 1


            global reverseV
            if self.checkboxT.isChecked():
                reverseV = False
            else:
                reverseV = True


            if self.checkboxA.isChecked():
                with open(path+"cleaned_data.txt", 'r') as file:
                    columns = len(file.readline().strip().split('\t'))
                columns = columns - 2

                factor = round(factor * columns * 0.01) + 1
                if factor < 2 and factor >= 0:
                    factor = 2

    

                    
        
        except ValueError:
            self.label2.show()
            ready = False
        
        if ready == True:
            self.label2.hide()
            self.progress.setStyleSheet("font-size: 18px; color: white; margin-top: 8px;")
            self.progress.setStyleSheet("font-size: 18px; color: white; margin-top: 8px;")
            QApplication.processEvents() 

            self.worker_thread = WorkerThread(reverseV, number, factor)
            self.worker_thread.finished.connect(self.processing_finished)
            self.worker_thread.start()
    
    def processing_finished(self):
        self.progress.setStyleSheet("font-size: 18px; color: #325ca9; margin-top: 8px;")
        self.parent().widget(2).run()
        self.parent().setCurrentIndex(2) 

class Page3(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0) 

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(path+"assets/back_icon.png")) 
        self.back_button.setStyleSheet("background: transparent;")
        self.back_button.setFixedSize(28, 28)

        self.back_button.clicked.connect(self.back)

        svg_widget = QSvgWidget(path+'assets/logo.svg')
        svg_widget.setStyleSheet("margin-bottom: -20px;")
        svg_widget.setFixedSize(160, 30)

        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon(path+"assets/reset.png")) 
        self.reset_button.setStyleSheet("background: transparent;")
        self.reset_button.setFixedSize(30, 30)

        self.reset_button.clicked.connect(self.reset)

        space1 = QSpacerItem(22, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        space2 = QSpacerItem(39, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        row_layout5 = QHBoxLayout()
        row_layout5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        row_layout5.addWidget(self.back_button)
        row_layout5.addItem(space1)

        row_layout5.addWidget(svg_widget)
        row_layout5.addItem(space2)

        row_layout5.addWidget(self.reset_button)


        layout.addLayout(row_layout5)
    
        row_layout3 = QHBoxLayout()
        self.download_button = QPushButton("Graph", self)
        self.download_button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        row_layout3.addWidget(self.download_button)

        self.download_button.clicked.connect(self.download_figure)

        self.data = QPushButton("Data", self)
        self.data.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        row_layout3.addWidget(self.data)

        self.data.clicked.connect(self.download_data)

        self.pseudog = QPushButton("Removed", self)
        self.pseudog.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        row_layout3.addWidget(self.pseudog)

        self.pseudog.clicked.connect(self.pseudo)

        layout.addLayout(row_layout3)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(0)
        self.checkbox1 = QCheckBox()
        self.checkbox1.setStyleSheet("margin-right: 10px; background-color: transparent;")
        self.checkbox1.clicked.connect(self.run)
        row_layout.addWidget(self.checkbox1)

        spacer_item = QSpacerItem(-40, -40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout.addItem(spacer_item)

        field1 = QLabel('  Find Threshold:<sup>ⓘ</sup>', self)
        field1.setStyleSheet("font-size: 16px; color: white; min-width: 110px; margin-left: 6px;")
        field1.mousePressEvent = lambda event: self.info_display("fin_thr")

        row_layout.addWidget(field1)
        
        self.input1 = QTextEdit(self)
        self.input1.setStyleSheet("font-size: 16px; max-width: 70px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 4px;")
        self.input1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        row_layout.addWidget(self.input1)

        spacer_itemAA = QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout.addItem(spacer_itemAA)

        self.output1 = QLabel("",self)
        self.output1.setStyleSheet("font-size: 16px; color: gray;")
        row_layout.addWidget(self.output1)

        row_layout2 = QHBoxLayout()
        row_layout2.setSpacing(-20) 

        self.checkbox2 = QCheckBox()
        self.checkbox2.setStyleSheet("margin-right: -70x; background-color: transparent;")
        row_layout2.addWidget(self.checkbox2)
        self.checkbox2.clicked.connect(self.run)

        spacer_item = QSpacerItem(-40, -40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout2.addItem(spacer_item)

        field2 = QLabel('  Specific Value:<sup>ⓘ</sup>', self)
        field2.setStyleSheet("font-size: 16px; color: white; min-width: 110px; margin-left: 6px;")
        field2.mousePressEvent = lambda event: self.info_display("spe_val")
        row_layout2.addWidget(field2)

        self.input2 = QTextEdit(self)
        self.input2.setStyleSheet("font-size: 16px; max-width: 70px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 10px;")
        self.input2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        row_layout2.addWidget(self.input2)

        spacer_itemA = QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout2.addItem(spacer_itemA)

        self.output2 = QLabel('', self)
        self.output2.setStyleSheet("font-size: 16px; color: white;")
        row_layout2.addWidget(self.output2)

        row_layout4 = QHBoxLayout()

        self.show_button = QPushButton( "Top x Saturated Genes")
        self.show_button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold; min-width: 165px;")
        row_layout4.addWidget(self.show_button)
        self.show_button.clicked.connect(self.show_message)

        spacer_item2 = QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        row_layout4.addItem(spacer_item2)

        self.field3 = QLabel('x:<sup>ⓘ</sup>', self)
        self.field3.setStyleSheet("font-size: 16px; color: white;")
        self.field3.mousePressEvent = lambda event: self.info_display("top_sat")
        row_layout4.addWidget(self.field3)  

        self.inputX = QTextEdit(self)
        self.inputX.setStyleSheet("font-size: 16px; max-width: 70px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 2px;")
        self.inputX.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        row_layout4.addWidget(self.inputX)

        self.figure = Figure(figsize=(2.7,2.7), dpi=65)
        self.figure.subplots_adjust(right=0.95)
        self.figure.subplots_adjust(top=0.93)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(280, 280)
        layout.addWidget(self.canvas)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        if ready == True:
            self.make_graph(number, sat_type)

        layout2 = QVBoxLayout()
        layout2.addLayout(row_layout)
        layout2.addLayout(row_layout2)
        layout2.addLayout(row_layout4)
        layout.addLayout(layout2)

        layout2.setSpacing(0)

        self.hover_label = QLabel(self) 
        self.hover_label.setStyleSheet("font-size: 12px; color: white; background-color: orange; font-weight: bold; border-radius: 5px; min-width: 108px;")
        self.hover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hover_label.hide()  

        self.input1.textChanged.connect(self.evaluate_threshold)
        self.input2.textChanged.connect(self.evaluate_specific_value)

        layout.setSpacing(8)
    def info_display(self, element):
        if element == "fin_thr":
            text = f"Input the threshold you are trying to evalute. Enter any value between 0-1.\n\nFor example, if you want to determine when 90% saturation is reached input '0.9'. The outputted value is the first value n that saturation value or greater is reached three times in a row.\n\nPress the checkbox to display this threshold on the graph."
            title = "Find Threshold"
            height = 200
        if element == "spe_val":
            text = f"Input the value n you want to evaluate the saturation of. Input any integer between 1 and the the upper limit of your graph.\n\nFor example, if you want to determine the saturation of the 100th rank, enter in 100. The outputted value is the saturation at n.\n\nPress the checkbox to display this value on the graph."
            title = "Specific Value"
            height = 185
        if element == "top_sat":
            text = "To find the most saturated genes in your dataset, enter an integer between 1-1000. The input will determine the number of saturated genes appearing when the 'Top x Saturated Genes' button is pressed.\n\nFor example, if I want to find the top 10 most saturated genes I would enter 10.\n\nThe outputted window will display ranks, genes, and the number of times they appear in your data range, respectively. "
            title = "Top x Saturated Genes"
            height = 220

 
        message_box = CustomMessageBox(text, "info", height, self)
        message_box.setWindowTitle(title)
        message_box.exec()

    def reset(self):
        main_reset()
        self.parent().setCurrentIndex(0)

    def back(self):
        self.parent().setCurrentIndex(1)

    def pseudo(self):
        if os.path.exists(path+"removed_genes.txt"):
            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Data', os.path.expanduser("~"), 'Text Files (*.txt)')
            if save_path:
                shutil.copyfile(path+'removed_genes.txt', save_path)
        else:
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Pseudogenes")
            message_box.setText("No genes removed.")
            message_box.exec()

    def show_message(self):
        try:
            top = int(self.inputX.toPlainText().replace(",",""))
            if top > 0 and top <= 1000:
                text = top50(top)
                message_box = CustomMessageBox(text, "rank", 0, self)
                message_box.setWindowTitle("Top Saturated Genes")
                message_box.exec()
        except ValueError:
            pass

    def run(self):
        self.make_graph(number, sat_type)

    def evaluate_threshold(self):
        if sat_type == "incremental_saturation":
            which = 1
        if sat_type == "overall_saturation":
            which = 2
        try:
            desired = float(self.input1.toPlainText())
            if desired <= 1 and desired >= 0:
                with open(path+'graph.txt', 'r') as file:
                    lines = file.readlines()
                    check = 0
                    for line in lines:
                        try:
                            value = float(line.strip().split('\t')[which])
                            if value >= desired and check < 2:
                                check = check + 1
                                continue
                            if value >= desired and check == 2:
                                final  = str(int(line.strip().split('\t')[0])-2)
                                self.output1.setText(final)
                                self.output1.setStyleSheet("font-size: 16px; color: white;")
                                self.run()
                                break
                            if value < desired and check > 0:
                                check = 0
                                continue
                        except ValueError:
                            pass
            else:
                self.output1.setText("0-1")
                self.output1.setStyleSheet("font-size: 16px; color: gray;")
        except ValueError:
            if self.input1.toPlainText() == "":
                self.output1.setText("")
                self.output1.setStyleSheet("font-size: 16px; color: white")     
            else:
                self.output1.setText("0-1")
                self.output1.setStyleSheet("font-size: 16px; color: gray;")

    def evaluate_specific_value(self):
        if sat_type == "incremental_saturation":
            which = 1
        if sat_type == "overall_saturation":
            which = 2

        value = self.input2.toPlainText()
        if value == "":
            self.output2.setText("")
            self.output2.setStyleSheet("font-size: 16px; color: gray;")
        else:
            try:
                with open(path+'graph.txt', 'r') as file:
                    lines = file.readlines()
                    output = round(float((lines[int(value)].strip().split('\t')[which]))*100)
                    self.output2.setText(f"{output}%")
                    self.output2.setStyleSheet("font-size: 16px; color: white;")
                    self.run()
        
            except (ValueError, IndexError) as e:
                self.output2.setText(f"1-{str(number)}")
                self.output2.setStyleSheet("font-size: 16px; color: gray;")

    def download_figure(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Figure', os.path.expanduser("~"), 'PNG Files (*.png)')
        if save_path:
            self.figure.savefig(save_path, dpi=300)

    def download_data(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Data', os.path.expanduser("~"), 'Text Files (*.txt)')
        if save_path:
            shutil.copyfile(path+'graph.txt', save_path)

    def make_graph(self, elements, saturation_type):
        with open(path+'graph.txt', 'r') as file:
            lines = file.readlines()

        x_array = []
        y_array = []
        for line in lines:
            rows = line.strip().split('\t')
            if rows[0] != "Nth Gene Included":
                x_array.append(float(rows[0]))
            if saturation_type == "incremental_saturation":
                if rows[1] != "Incremental Saturation":
                    y_array.append(float(rows[1]))
            if saturation_type == "overall_saturation":
                if rows[2] != "Overall Saturation":
                    y_array.append(float(rows[2]))

        x = np.array(x_array)
        y = np.array(y_array)

        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.plot(x, y, c='#325BA9', linewidth="1")

        ax.yaxis.set_major_locator(MultipleLocator(0.1))

        if elements < 5:
            x_ticks = np.arange(0.5, elements + (elements / 10), 0.5)
        else:
            x_ticks = np.arange(0, elements + (elements / 10), round((elements / 5)))

        ax.set_xticks(x_ticks)

        if sat_type == "incremental_saturation":
            ax.set_title("Incremental Saturation by nth Gene")
            ax.set_ylabel("Incremental Saturation")
        if sat_type == "overall_saturation":
            ax.set_title("Overall Saturation by nth Gene")
            ax.set_ylabel("Overall Saturation")

        ax.grid(True) 
        ax.set_xlabel("nth Gene")

        global line1
        global line_x
        global line_y

        line1 = self.figure.gca().get_lines()[0]
        line_x = line1.get_xdata()
        line_y = line1.get_ydata()

        if self.checkbox1.isChecked():
            try:
                ax.vlines(x=int(self.output1.text()), ymin = 0, ymax = max(y)+0.1, linestyle='dotted', color='black', linewidth=2.5)
            except ValueError:
                pass

        if self.checkbox2.isChecked():
            
            try:
                ax.axhline(y=(int(str(self.output2.text())[:-1]))/100, linestyle='dotted', color='orange', linewidth=2.5)
                ax.vlines(x=int(self.input2.toPlainText()), ymin = 0, ymax = max(y)+0.1, linestyle='dotted', color='orange', linewidth=2.5)
            except ValueError:
                pass

        ax.set_ylim([0, y.max()+0.1])
        y_ticks = np.arange(0, max(y) + 0.1, 0.1)
        ax.set_yticks(y_ticks)
        self.canvas.draw()  
        plt.show()

    def on_mouse_move(self, event):
        if event.inaxes: 
            closest_index = np.abs(line_x - event.xdata).argmin()
            self.hover_label.setText(f'x: {line_x[closest_index]:.0f}, y: {line_y[closest_index]*100:.0f}%')
            self.hover_label.show()
            cursor_pos = self.canvas.mapFromGlobal(QCursor.pos())
            self.hover_label.move(cursor_pos.x() - 50, cursor_pos.y())
        else:
            self.hover_label.hide()

class Page4(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10) 
        layout.setContentsMargins(2, 3, 2, 2)

        self.back_button = QLabel()
        self.back_button.setStyleSheet("background: transparent;")
        self.back_button.setFixedSize(28, 28)

        svg_widget = QSvgWidget(path+'assets/logo.svg')
        svg_widget.setStyleSheet("margin-bottom: -20px; margin-left: -10px;")
        svg_widget.setFixedSize(160, 30)

        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon(path+"assets/reset.png")) 
        self.reset_button.setStyleSheet("background: transparent; margin-left: 5px;")
        self.reset_button.setFixedSize(30, 30)

        self.reset_button.clicked.connect(self.reset)

        space1 = QSpacerItem(18, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        space2 = QSpacerItem(39, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        row_layout5 = QHBoxLayout()
        row_layout5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        row_layout5.addWidget(self.back_button)
        row_layout5.addItem(space1)

        row_layout5.addWidget(svg_widget)
        row_layout5.addItem(space2)

        row_layout5.addWidget(self.reset_button)

        row_layout5.setContentsMargins(-20,-50,-20,-20)

        layout.addLayout(row_layout5)

        vspacer = QSpacerItem(30, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(vspacer)
        
        text_label = QLabel('Upload saturation data to\nassess significant differences.', self)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        text_label.setStyleSheet("font-size: 16px; color: white;")

        layout.addWidget(text_label)

        row_layout_buttons = QHBoxLayout()
        row_layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button1_lo = QVBoxLayout()
        button1_lo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button1_lo.setSpacing(4)

        button2_lo = QVBoxLayout()
        button2_lo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button2_lo.setSpacing(4)

        Page4.button1 = QPushButton('Upload 1st\nreference (.txt)\n⇧', self)
        Page4.button1.setStyleSheet("font-size: 13px; color: white; background-color: rgba(0, 0, 0, 0.4); font-weight: bold; padding: 14px; margin-right: 4px;")
        Page4.button1.setFixedHeight(160)
        Page4.button1.clicked.connect(self.open_pdf1) 

        Page4.imported1 = QLabel(" ")
        Page4.imported1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Page4.imported1.setStyleSheet("font-size: 14px; color: white;")

        Page4.button2 = QPushButton('Upload 2nd\nreference (.txt)\n⇧', self)
        Page4.button2.setStyleSheet("font-size: 13x; color: white; background-color: rgba(0, 0, 0, 0.4); font-weight: bold; padding: 14px; margin-left: 4px;")
        Page4.button2.setFixedHeight(160)  
        Page4.button2.clicked.connect(self.open_pdf2) 

        Page4.imported2 = QLabel(" ")
        Page4.imported2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Page4.imported2.setStyleSheet("font-size: 14px; color: white;")

        button1_lo.addWidget(Page4.button1)
        button1_lo.addWidget(Page4.imported1)

        button2_lo.addWidget(Page4.button2)
        button2_lo.addWidget(Page4.imported2)

        row_layout_buttons.addLayout(button1_lo)
        row_layout_buttons.addLayout(button2_lo)

        layout.addLayout(row_layout_buttons)

        vspacer1 = QSpacerItem(30, 30, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(vspacer1)

        button = QPushButton('Run Unpaired T-Test', self)
        button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        layout.addWidget(button)
        button.clicked.connect(self.run_test)

        Page4.invalid = QLabel("Error; Please upload two\nfiles in the correct format.")
        Page4.invalid.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        Page4.invalid.setStyleSheet("font-size: 14px; color: #325BA9;")

        layout.addWidget(Page4.invalid)

        vspacer2 = QSpacerItem(74, 74, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(vspacer2)

    def open_pdf1(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Txt', os.path.expanduser("~"), 'Txt Files (*.txt)')
        if file_path:
            current_path = os.path.dirname(os.path.realpath(__file__))
            new_path = os.path.join(current_path, os.path.basename(file_path))
            
            shutil.copyfile(file_path, new_path)
            
            if os.path.exists(path+"stat1.txt"):
                try:
                    os.remove(path+"stat1.txt")
                    print(f"Previous stat1 file deleted.")
                except OSError as e:
                    print(f"Error deleting: {e}")
            else:
                print(f"stat1 file was not present before.")  

            renamed_path = os.path.join(current_path, "stat1.txt")
            os.rename(new_path, renamed_path)
            
            file_name = os.path.basename(file_path)

            if len(file_name) >= 8:
                file_name = file_name[:4] + "....txt"

            Page4.button1.setText('Upload 1st\nreference (.txt)\n')
            Page4.change1(file_name)

    def change1(file_name):
        Page4.imported1.setText(f"'{file_name}'")

    def open_pdf2(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Txt', os.path.expanduser("~"), 'Txt Files (*.txt)')
        if file_path:
            current_path = os.path.dirname(os.path.realpath(__file__))
            new_path = os.path.join(current_path, os.path.basename(file_path))
            
            shutil.copyfile(file_path, new_path)

            if os.path.exists(path+"stat2.txt"):
                try:
                    os.remove(path+"stat2.txt")
                    print(f"Previous stat2 file deleted.")
                except OSError as e:
                    print(f"Error deleting: {e}")
            else:
                print(f"stat2 file was not present before.")  
            
            renamed_path = os.path.join(current_path, "stat2.txt")
            os.rename(new_path, renamed_path)
        
            
            file_name = os.path.basename(file_path)

            if len(file_name) >= 8:
                file_name = file_name[:4] + "....txt"

            Page4.button2.setText('Upload 2nd\nreference (.txt)\n')
            Page4.change2(file_name)

    def change2(file_name):
        Page4.imported2.setText(f"'{file_name}'")

    def run_test(self):
        try:
            Page4.invalid.setStyleSheet("font-size: 14px; color: #325BA9;")
            results = check_for_statistical_significance()
            print(results)
            if results == "Error":
                Page4.invalid.setStyleSheet("font-size: 14px; color: orange;")
            else:
                
                if os.path.exists(path+'result_statistics.txt'):
                    try:
                        os.remove(path+'result_statistics.txt'  )
                        print(f"result_statistics.txt deleted.")
                    except OSError as e:
                        print(f"Error deleting: {e}")
                else:
                    print(f"File does not exist.")   

                def stat_file(file_path, *columns_data):
                    with open(file_path, 'w', newline='') as file:

                        tab_writer = csv.writer(file, delimiter='\t')
                        
                        for row_data in zip(*columns_data):
                            tab_writer.writerow(row_data)

                file_path = 'result_statistics.txt'  
                titles = ["Calculations","Sample Size (n)", "Degrees of Freedom", "Mean Group 1", "Mean Group 2", "SD Group 1", "SD Group 2", "Pooled SD", "Standard Error", "T-Statistic", "P-value","Interpretation"]
                stat_file(file_path, titles, results[0], results[1])

                Page5.interpretation1.setText(f"{results[0][11]}")
                Page5.interpretation2.setText(f"{results[1][11]}")
                Page5.meandiff1.setText(f"Sample Means: A = {round(float(results[0][3]),3)}\t B = {round(float(results[0][3]),3)}")
                Page5.meandiff2.setText(f"Sample Means: A = {round(float(results[1][4]),3)}\t B = {round(float(results[1][4]),3)}")
                Page5.sd1.setText(f"Sample SDs:     A = {round(float(results[0][5]),3)}\t B = {round(float(results[0][5]),3)}")
                Page5.sd2.setText(f"Sample SDs:     A = {round(float(results[1][6]),3)}\t B = {round(float(results[1][6]),3)}")
                Page5.tstat1.setText(f"T-Statistic: {round(float(results[0][9]),4)}")
                Page5.tstat2.setText(f"T-Statistic: {round(float(results[1][9]),4)}")
                Page5.p1.setText(f"p-value: {round(float(results[0][10]),12)}")
                Page5.p2.setText(f"p-value: {round(float(results[1][10]),12)}")

                self.parent().setCurrentIndex(4)

        except:
            Page4.invalid.setStyleSheet("font-size: 14px; color: orange;")

    def reset(self):
        main_reset()
        
        Page4.button1.setText('Upload 1st\nreference (.txt)\n⇧')
        Page4.button2.setText("Upload 2nd\nreference (.txt)\n⇧")

        Page4.imported1.setText(" ")
        Page4.imported2.setText(" ")

        Page4.invalid.setStyleSheet("font-size: 14px; color: #325BA9;")

        self.parent().setCurrentIndex(0)

class Page5(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8) 
        layout.setContentsMargins(2, 3, 2, 2)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(path+"assets/back_icon.png")) 
        self.back_button.setStyleSheet("background: transparent; margin-right: 10px;")
        self.back_button.setFixedSize(28, 28)

        self.back_button.clicked.connect(self.back)

        svg_widget = QSvgWidget(path+'assets/logo.svg')
        svg_widget.setStyleSheet("margin-bottom: -20px; margin-left: 10px;")
        svg_widget.setFixedSize(160, 30)

        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon(path+"assets/reset.png")) 
        self.reset_button.setStyleSheet("background: transparent; margin-left: 4px;")
        self.reset_button.setFixedSize(30, 30)

        self.reset_button.clicked.connect(self.reset)

        space1 = QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        space2 = QSpacerItem(44, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        row_layout5 = QHBoxLayout()
        row_layout5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        row_layout5.addWidget(self.back_button)
        row_layout5.addItem(space1)

        row_layout5.addWidget(svg_widget)
        row_layout5.addItem(space2)

        row_layout5.addWidget(self.reset_button)

        row_layout5.setContentsMargins(-20,-50,-20,-20)

        layout.addLayout(row_layout5)

        def extract_columns(file_path, column):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                sat_column = [(line.strip().split('\t')[column]) for line in lines[1:]]
                return sat_column


        title = QLabel("Two-Tailed Unpaired T-Test")
        title.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)


        title1 = QLabel("Incremental Saturation:")
        title1.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        layout.addWidget(title1)

        Page5.interpretation1 = QLabel("")
        Page5.interpretation1.setWordWrap(True)
        Page5.interpretation1.setStyleSheet("font-size: 16px; color: white; background-color: orange; text-align: center; border: 2px solid white; padding: 4px;")
        layout.addWidget(Page5.interpretation1)

        Page5.meandiff1 = QLabel("")
        Page5.meandiff1.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.meandiff1)

        Page5.sd1 = QLabel("")
        Page5.sd1.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.sd1)

        Page5.tstat1 = QLabel("")
        Page5.tstat1.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.tstat1)

        Page5.p1 = QLabel("")
        Page5.p1.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.p1)

        title2 = QLabel("Overall Saturation:")
        title2.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        layout.addWidget(title2)

        Page5.interpretation2 = QLabel("")
        Page5.interpretation2.setWordWrap(True)
        Page5.interpretation2.setStyleSheet("font-size: 16px; color: white; background-color: orange; text-align: center; border: 2px solid white; padding: 4px;")
        layout.addWidget(Page5.interpretation2)

        Page5.meandiff2 = QLabel("")
        Page5.meandiff2.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.meandiff2)

        Page5.sd2 = QLabel("")
        Page5.sd2.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.sd2)

        Page5.tstat2 = QLabel("")
        Page5.tstat2.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.tstat2)

        Page5.p2 = QLabel("")
        Page5.p2.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(Page5.p2)

        button = QPushButton('Download Full Report', self)
        button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        layout.addWidget(button)
        button.clicked.connect(self.download)

    def download(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Analysis', os.path.expanduser("~"), 'Text Files (*.txt)')
        if save_path:
            shutil.copyfile(path+'result_statistics.txt', save_path)

    def reset(self):
        main_reset() 

        Page4.button1.setText('Upload 1st\nreference (.txt)\n⇧')
        Page4.button2.setText("Upload 2nd\nreference (.txt)\n⇧")

        Page4.imported1.setText(" ")
        Page4.imported2.setText(" ")

        Page4.invalid.setStyleSheet("font-size: 14px; color: #325BA9;")

        self.parent().setCurrentIndex(0)
    
    def back(self):
        self.parent().setCurrentIndex(3)

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('THRESHOLD')

    def initUI(self):
        self.setGeometry(250, 200, 400, 300)
        self.setFixedSize(300, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #325BA9;")

        stack = QStackedWidget()
        stack.addWidget(Page1())
        stack.addWidget(Page2())
        stack.addWidget(Page3())
        stack.addWidget(Page4())
        stack.addWidget(Page5())

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stack)

class CustomMessageBox(QDialog):
    def __init__(self, text, type, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Message Box")

        self.setStyleSheet("background-color: #F5F5F5; border: none;")
        self.setWindowOpacity(0.90) 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8) 

        self.text_browser = QTextBrowser(self)
        self.text_browser.setPlainText(text)

        if type == "rank":
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.text_browser.setStyleSheet("color: #325ba9; border: none; font-weight: bold;")
        if type == "info":
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.text_browser.setStyleSheet("color: black; border: none; font-weight: normal;")
            self.resize(300, height)

        layout.addWidget(self.text_browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())