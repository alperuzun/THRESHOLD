import os
import sys
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

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10) 

        svg_widget = QSvgWidget(path+'assets/logo.svg')
        svg_widget.setFixedSize(266, 50)
        layout.addWidget(svg_widget)

        text_label = QLabel('Open a .txt file to begin \n analyzing gene saturation', self)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        text_label.setStyleSheet("font-size: 18px; color: white;")
        font = QFont("Proxima Nova", 18)
        text_label.setFont(font)
        layout.addWidget(text_label)

        button = QPushButton('Open File', self)
        font = QFont("Proxima Nova", 14)
        button.setFont(font)
        button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold;")
        layout.addWidget(button)
        button.clicked.connect(self.open_pdf)

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
                print(f"Removed file does not exist.")   

            subprocess.call(["java", path + "clean2.java"])
            file_path = "your_file.txt"

            if os.path.exists(path+"removed_genes.txt"):
                with open(path+"removed_genes.txt", "r") as file:
                    lines = file.readlines()
                    non_empty_lines = [line for line in lines if line.strip()]

                with open(path+"removed_genes.txt", "w") as file:
                    file.writelines(non_empty_lines)

                print("Empty rows removed from the file.")
            
            self.parent().setCurrentIndex(1)

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

        label = QLabel('Graph', self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        label.setStyleSheet("font-size: px; color: white; font-weight: bold; margin-top: 50px;")
        font = QFont("Proxima Nova", 20)
        label.setFont(font)
        layout.addWidget(label)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)  
        layout.addLayout(row_layout)

        field1 = QLabel('Number of Genes:', self)
        field1.setStyleSheet("font-size: 16px; color: white;")
        font = QFont("Proxima Nova", 16)
        field1.setFont(font)
        row_layout.addWidget(field1)

        self.input = QTextEdit(self)
        self.input.setStyleSheet("font-size: 16px; max-width: 200px; max-height: 22px; color: white; border: 1px solid white; background-color: orange;")
        self.input.setFont(font)
        self.input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  
        row_layout.addWidget(self.input)

        self.radio1 = QRadioButton('Overall Saturation')
        self.radio1.setStyleSheet("font-size: 16px; color: white; margin-bottom: 0;")
        self.radio1.setFont(font)

        self.radio2 = QRadioButton('Incremental Saturation')
        self.radio2.setStyleSheet("font-size: 16px; color: white;")
        self.radio2.setFont(font)

        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)

        row_layout2 = QHBoxLayout()
        row_layout2.setSpacing(5) 

        fix_layout = QVBoxLayout()
        fix_layout.setSpacing(4)
        fix_layout.addLayout(row_layout2)

        field2 = QLabel('Saturation Level: ', self)
        field2.setStyleSheet("font-size: 16px; color: white;")
        field2.setFont(font)
        row_layout2.addWidget(field2)

        self.input2 = QTextEdit(self)
        self.input2.setStyleSheet("font-size: 16px; width: 15px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 0px; margin-right: 3px;")
        self.input2.setFont(font)
        self.input2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  
        row_layout2.addWidget(self.input2)
        
        self.checkboxA = QCheckBox()
        self.checkboxA.setStyleSheet("background-color: transparent; margin-right: -2px; margin-left: 5px;")
        row_layout2.addWidget(self.checkboxA)

        self.percentlabel = QLabel(" (%?)", self)
        self.percentlabel.setStyleSheet("font-size: 14px; color: white; margin-left: -2px; background-color: transparent; padding: 0; margin-right: 0;")
        row_layout2.addWidget(self.percentlabel)

        row_layout3 = QHBoxLayout()
        row_layout3.setSpacing(0)

        labelT = QLabel('Reverse Ranking')
        labelT.setFont(font)
        labelT.setStyleSheet("font-size: 16px; color: white; ")
        row_layout3.addWidget(labelT)

        self.checkboxT = QCheckBox()
        self.checkboxT.setStyleSheet("background-color: transparent;")
        row_layout3.addWidget(self.checkboxT)

        fix_layout.addLayout(row_layout3)  

        layout.addLayout(fix_layout)        

        button = QPushButton('Generate')
        button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold; min-height: 22px; margin-top: 20px;")
        button.setFont(font)
        layout.addWidget(button)

        self.label2 = QLabel("Invalid; must enter number of genes\n(1-10,000), saturation type and level (2-100).")
        self.label2.setStyleSheet("font-size: 14px; color: orange;")
        self.label2.setFont(font)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.addWidget(self.label2)

        button.clicked.connect(self.generate)
        self.label2.hide()

        spacer_bottom = QSpacerItem(20, 200)
        layout.addItem(spacer_bottom)

    def reset(self):
        to_remove = ["cleaned_data.txt","data.txt","graph.txt","ranks.json","removed_genes.txt"]

        for item in to_remove:
            print(item)
            if os.path.exists(path+item):
                try:
                    os.remove(path+item)
                    print(f"{item} deleted.")
                except OSError as e:
                    print(f"Error deleting: {e}")
            else:
                print(f"File does not exist.")  
                continue 
            
        self.parent().setCurrentIndex(0)

    def generate(self):
        global ready
        ready = False
        try:
            number_of_genes = self.input.toPlainText().replace(",","")

            global factor
            factor = int(self.input2.toPlainText().replace(",",""))

            

            global reverseV
            if self.checkboxT.isChecked():
                reverseV = False
            else:
                reverseV = True

            if self.checkboxA.isChecked():
                with open(path+"cleaned_data.txt", 'r') as file:
                    columns = len(file.readline().strip().split('\t'))
                columns = columns - 2

                if factor >= 2 and factor <= 100:
                    factor = round(factor * columns * 0.01)

                    if factor < 2 and factor >= 0:
                        factor = 2
            print(factor)
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
                    
            if factor <= 1 or factor > 100:
                self.label2.show()
                print(factor)
                ready = False
        except ValueError:
            self.label2.show()
            ready = False
        
        if ready == True:
            print(factor)
            print(reverseV)
            rank(reverseV)
            make_file(number, factor)
            self.parent().widget(2).run()
            self.parent().setCurrentIndex(2) 
            self.label2.hide()


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
        self.checkbox1.setStyleSheet("margin-right: 0px; background-color: transparent;")
        self.checkbox1.clicked.connect(self.run)
        row_layout.addWidget(self.checkbox1)

        spacer_item = QSpacerItem(-40, -40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout.addItem(spacer_item)

        field1 = QLabel(' Find Threshold:', self)
        field1.setStyleSheet("font-size: 16px; color: white; min-width: 110px; margin-left: 0px;")
        font = QFont("Proxima Nova", 16)
        field1.setFont(font)

        row_layout.addWidget(field1)
        
        self.input1 = QTextEdit(self)
        self.input1.setStyleSheet("font-size: 16px; max-width: 70px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 9px;")
        font = QFont("Proxima Nova", 16)
        self.input1.setFont(font)
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
        self.checkbox2.setStyleSheet("margin-right: -80px; background-color: transparent;")
        row_layout2.addWidget(self.checkbox2)
        self.checkbox2.clicked.connect(self.run)

        spacer_item = QSpacerItem(-40, -40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout2.addItem(spacer_item)

        field2 = QLabel(' Specific Value:', self)
        field2.setStyleSheet("font-size: 16px; color: white; min-width: 110px;")
        font = QFont("Proxima Nova", 16)
        field2.setFont(font)
        row_layout2.addWidget(field2)

        self.input2 = QTextEdit(self)
        self.input2.setStyleSheet("font-size: 16px; max-width: 70px; max-height: 22px; color: white; border: 1px solid white; background-color: orange; margin-left: 12px;")
        font = QFont("Proxima Nova", 16)
        self.input2.setFont(font)
        self.input2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        row_layout2.addWidget(self.input2)

        spacer_itemA = QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        row_layout2.addItem(spacer_itemA)

        self.output2 = QLabel('', self)
        self.output2.setStyleSheet("font-size: 16px; color: white;")
        row_layout2.addWidget(self.output2)

        row_layout4 = QHBoxLayout()

        self.show_button = QPushButton("Top x Saturated Genes")
        font = QFont("Proxima Nova", 14)
        self.show_button.setFont(font)
        self.show_button.setStyleSheet("font-size: 14px; color: #325BA9; background-color: white; font-weight: bold; min-width: 170px;")
        row_layout4.addWidget(self.show_button)
        self.show_button.clicked.connect(self.show_message)

        spacer_item2 = QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        row_layout4.addItem(spacer_item2)

        self.field3 = QLabel('x: ', self)
        self.field3.setStyleSheet("font-size: 16px; color: white;")
        self.field3.setFont(font)
        row_layout4.addWidget(self.field3)  

        self.inputX = QTextEdit(self)
        self.inputX.setStyleSheet("font-size: 16px; max-width: 70px; max-height: 22px; color: white; border: 1px solid white; background-color: orange;")
        self.inputX.setFont(font)
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

    def reset(self):
        to_remove = ["cleaned_data.txt","data.txt","graph.txt","ranks.json","removed_genes.txt"]

        for item in to_remove:
            if os.path.exists(path+item):
                try:
                    os.remove(path+item)
                    print(f"{item} deleted.")
                except OSError as e:
                    print(f"Error deleting: {e}")
            else:
                print(f"File does not exist.")   
            
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
                message_box = CustomMessageBox(text, self)
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

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('ThresHold')

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

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stack)

class CustomMessageBox(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Message Box")

        self.resize(220,300)
        self.setStyleSheet("background-color: #D3D3D3; border: none;")
        self.setWindowOpacity(0.9)  # Adjust the opacity value as needed

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_browser = QTextBrowser(self)
        self.text_browser.setPlainText(text)
        font = QFont("Proxima Nova", 18)
        self.text_browser.setFont(font)
        self.text_browser.setStyleSheet("color: #325ba9; border: none; font-weight: bold;")
        layout.addWidget(self.text_browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())