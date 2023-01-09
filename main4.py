import sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
    QProgressBar


class FileInputWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Create labels and line edits for the input file locations
        input_file_label1 = QLabel("Enter the location of the first input file:")
        self.input_file_edit1 = QLineEdit()

        # Create a label and line edit for the output file location
        output_file_label = QLabel("Enter the location for the output file:")
        self.output_file_edit = QLineEdit()

        # Create a button to generate the output file
        generate_button = QPushButton("Generate Output File")
        generate_button.clicked.connect(self.generate_output)

        # Create a progress bar
        self.progress_bar = QProgressBar()

        # Create a vertical layout to hold the widgets
        v_layout = QVBoxLayout()
        v_layout.addWidget(input_file_label1)
        v_layout.addWidget(self.input_file_edit1)
        v_layout.addWidget(output_file_label)
        v_layout.addWidget(self.output_file_edit)
        v_layout.addWidget(self.progress_bar)
        v_layout.addWidget(generate_button)

        # Set the layout for the widget
        self.setLayout(v_layout)

    def generate_output(self):
        # Get the locations of the input files and the output file from the line edits
        input_file1 = self.input_file_edit1.text()
        output_file = self.output_file_edit.text()

        # Set the progress bar to be indeterminate (showing an animation)
        self.progress_bar.setRange(0, 0)

        """Compressor"""

        def get_size(i):
            width, height = i.size
            return width, height

        """Compress Function"""

        def compress(input_image, c_file):
            i_image = Image.open(input_image, 'r')
            c_list = []
            px = i_image.getdata()
            pp = None
            x = 0
            for p in px:
                if p == pp:
                    x += 1
                else:
                    if pp is not None:
                        pvalue = 0 if pp == 0 else 1
                        c_list.append((x, pvalue))
                    pp = p
                    x = 1
            with open(c_file, 'w+') as f:
                w = get_size(i_image)[0]
                h = get_size(i_image)[1]
                f.write('P1\n')
                f.write('#Compressão Manual\n')
                f.write('%s %s\n' % (w, h))
                for v in range(3):
                    for z, pvalue in c_list:
                        f.write(str(z))
                        f.write(str(','))
            return c_list

        def descomprimido(ficheiro):
            l1 = []
            l2 = []
            for v in range(3):
                with open(ficheiro, 'r') as f:
                    for x in f:
                        l1 = x.split(',')
                        l1.pop()
            for a in range(len(l1)):
                l1[a] = int(l1[a])
            i = 0
            for z in l1:
                for v in range(z):
                    l2.append(i)
                i = (i + 1) % 2

            with open(output_file, 'w+') as f2:
                with open(ficheiro, 'r') as f:
                    c = 0
                    for linhas in f:
                        if c == 1:
                            f2.write("#Descompressão Manual\n")
                        if c != 1 and c < 3:
                            f2.write(linhas)
                        c = c + 1
                c = 0
                for v2 in l2:
                    if c <= 70:
                        f2.write(str(v2))
                        c = c + 1
                    if c == 70:
                        f2.write('\n')
                        c = 0
            return

        # Open the image and compress it
        compress(input_file1, 'Compressed File.txt')
        descomprimido('Compressed File.txt')

        # Create a message box to show a notification that the output file was generated
        QMessageBox.information(self, "Output Generated", "The output file has been generated.")
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_input_widget = FileInputWidget()
    file_input_widget.show()
    sys.exit(app.exec_())
