"""
This program was created to assist bioinformatics workers and significantly reduce their workload by allowing them to run FASTQC locally and compare the results of sequencing data.

Before running the code, make sure to install FASTQC on your computer and copy the path to the FASTQC function in the code where indicated "Copy path to your local FASTQC". Additionally, edit the file paths in the code to match your desired locations on your computer.

When you run the code, a window will pop up for you to select a directory. Please choose the folder containing the FASTQ files you want to analyze. The code will create a folder named "fastqc_results" to store the FASTQC results and generate an HTML report called "my_report," which will provide a comparison between the outputs uploaded to the program. It will also include a quick link to run BLAST, which helps find similar sequences at various levels.

You will find an example of how to run the program, as well as a ZIP folder containing sample files needed for uploading.

I hope you find this tool useful and effective. Good luck!

"""
import os
import glob
import sys
from PyQt6.QtWidgets import QApplication,  QFileDialog, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from pathlib import Path
import subprocess
import time

########################################
#PyQt Window for Directory Selection

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt File Dialog')
        self.setGeometry(200, 200, 400, 200)

        layout = QGridLayout()
        self.setLayout(layout)

        # directory selection
        dir_btn = QPushButton('Browse')
        dir_btn.clicked.connect(self.open_dir_dialog)
        self.dir_name_edit = QLineEdit()

        layout.addWidget(QLabel('Directory:'), 1, 0)
        layout.addWidget(self.dir_name_edit, 1, 1)
        layout.addWidget(dir_btn, 1, 2)

        # Submit button
        submit_btn = QPushButton('Submit')
        submit_btn.clicked.connect(self.submit_directory_name)
        layout.addWidget(submit_btn, 2, 2)

        self.show()

    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.dir_name_edit.setText(str(path))

    def submit_directory_name(self):
        directory_name = self.dir_name_edit.text()
        if directory_name:
            print(f"Submitting directory name: {directory_name}")
            # Call functions for FASTQC and HTML generation
            run_fastqc_and_generate_html(directory_name)

            # Close the window after submission
            self.close()  # This will close the main window

# Function to extract FASTQ files from a directory

def extract_fastq_files(directory):

    fastq_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.fq.gz'):
            fastq_files.append(os.path.join(directory, filename))
    return fastq_files

# Function to run FastQC on a given FASTQ file
def run_fastqc(fastq_file):
    fastqc_script_path = 'fastqc'
    file_name = os.path.basename(fastq_file)
    output_dir = os.path.join('C:/Users/hadar.LAPTOP-O4I2H8EK/Desktop/python_lab_project/fastqc_results', file_name + '_Results')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Command to run FastQC
    command = ['perl', fastqc_script_path, fastq_file, '-o', output_dir, '-extract']
    try:
        result = subprocess.call(command, cwd='C:/Users/Hadar/FastQC/FastQC', shell=True) #Copy path to your local FATQC
        print(f"FastQC analysis completed for {fastq_file}. Results are saved in {output_dir}.")

    except subprocess.CalledProcessError as e:
        print(f"Error running FastQC: {e}")
    except PermissionError as pe:
        print(f"Permission Error: {pe}")

#####################################################################
#Creating HTML

# Function to search and extract specific strings from a FASTQC data file
def search_and_print_without_string(file_path, search_strings):
    results = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                for search_string in search_strings:
                    if search_string in line:
                        modified_line = line.replace(search_string, '').strip()
                        results[search_string] = modified_line
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except UnicodeDecodeError:
        print(f"Error decoding file {file_path}. The file may not be in UTF-8 format.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return results

# Function to extract FASTQC data from a directory
def extract_fastqc_data(directory, search_strings):
    data = []
    print(f"Extracting FASTQC data from directory: {directory}")
    for folder in glob.glob(f"{directory}/*/*/"):
        print(f"Checking folder: {folder}")
        fastqc_file = os.path.join(folder, 'fastqc_data.txt')
        if os.path.exists(fastqc_file):
            print(f"Found file: {fastqc_file}")
            results = search_and_print_without_string(fastqc_file, search_strings)
            if results:
                data.append({
                    'Folder': os.path.basename(os.path.dirname(fastqc_file)),
                    'Sequence length': results.get('Sequence length', 'N/A'),
                    'Total Sequences': results.get('Total Sequences', 'N/A'),
                    '%GC': results.get('%GC', 'N/A')
                })
                print(f"Added data: {data[-1]}")
        else:
            print(f"File not found: {fastqc_file}")
    if not data:
        print("No data found in the directory.")
    return data

# Function to extract overrepresented sequences from FASTQC data
def extract_overrepresented_sequences(directory):
    overrepresented_data = []
    print(f"Extracting overrepresented sequences from directory: {directory}")
    for folder in glob.glob(f"{directory}/*/*/"):
        fastqc_file = os.path.join(folder, 'fastqc_data.txt')
        if os.path.exists(fastqc_file):
            print(f"Processing file: {fastqc_file}")
            with open(fastqc_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                in_table = False
                for line in lines:
                    if line.startswith(">>Overrepresented sequences"):
                        in_table = True
                        continue
                    if in_table and line.startswith("#"):
                        continue
                    if in_table and not line.strip():
                        break
                    if in_table:
                        parts = line.strip().split('\t')
                        if len(parts) >= 4:
                            overrepresented_data.append({
                                'Folder': os.path.basename(os.path.dirname(fastqc_file)),
                                'Sequence': parts[0],
                                'Count': parts[1],
                                'Percentage': parts[2],
                                'Possible Source': parts[3]
                            })
                        break  # We only want the first line of the table
        else:
            print(f"File not found for overrepresented sequences: {fastqc_file}")
    if not overrepresented_data:
        print("No overrepresented sequences found in the directory.")
    return overrepresented_data


# Function to create an HTML table from extracted data
def create_html_table(data):
    table_html = '<table border="1" align="center" style="margin:auto" border:solid cellpadding="10px">\n'
    table_html += '  <tr>\n'
    for header in data[0].keys():
        table_html += f'    <th>{header}</th>\n'
    table_html += '  </tr >\n'
    for row in data:
        table_html += '  <tr>\n'
        for value in row.values():
            table_html += f'    <td style="text-align:center ">{value}</td>\n'
        table_html += '  </tr>\n'
    table_html += '</table >\n'
    return table_html

# Function to create a table for overrepresented sequences with BLAST links
def create_overrepresented_sequences_table(data):
    table_html = '<table border="1" align="center" style="margin:auto" border:solid cellpadding="10px">\n'
    table_html += '  <tr>\n'
    for header in data[0].keys():
        table_html += f'    <th>{header}</th>\n'
    table_html += '    <th>BLAST</th>\n'  # Add a header for the BLAST column
    table_html += '  </tr>\n'
    for row in data:
        table_html += '  <tr>\n'
        for value in row.values():
            table_html += f'    <td style="text-align:center ">{value}</td>\n'
        # Add a button for BLAST analysis
        sequence = row['Sequence']
        blast_url = f'https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&QUERY={sequence}'
        table_html += f'    <td style="text-align:center"><a href="{blast_url}" target="_blank">BLAST</a></td>\n'
        table_html += '  </tr>\n'
    table_html += '</table>\n'
    return table_html

# Function to append content to an existing HTML file
def append_to_existing_html(file_path, content_html, title=None):
    with open(file_path, 'a', encoding='utf-8') as file:
        if title:
            file.write(f'<h3 style="text-align: center;">{title}</h3>\n')
        file.write('<br><br>\n')
        file.write(content_html)

def write_empty_file(fn):
    with open(fn, 'w') as fh:
        fh.write('<br></br>')
        fh.write('<h1 style="text-align: center;">NGS data QC wrapper</h1>\n')
        fh.close()

def createTabulatedImages(out_fn, section_title, image_fn_pattern, directory):
    with open(out_fn, 'a') as fh:
        fh.write('<html>\n<head>\n<style>\n')
        fh.write('body { font-family: "Roboto", sans-serif; }\n')
        fh.write('h3 { text-align: center; }\n')
        fh.write('table { border-collapse: collapse; width: 50%; margin: auto; }\n')
        fh.write('th, td { border: 1px solid black; text-align: center; padding: 8px; }\n')
        fh.write('</style>\n</head>\n<body>\n')
        fh.write('<h3>' + section_title + '</h3>\n')
        fh.write('<table>\n<tr>\n')

        folders = glob.glob(f"{directory}/*/*/")
        i = 0
        for folder in folders:
            folder_name = os.path.basename(os.path.dirname(folder))
            image_fns = glob.glob(os.path.join(folder, 'Images', os.path.basename(image_fn_pattern)))
            for fn in image_fns:
                i += 1
                fh.write(
                    '<th><div style="text-align: center;">' + folder_name + '<br><img src="' + fn + '" width="350"></div></th>\n')
                if i % 2 == 0:
                    fh.write('</tr><tr>\n')
        fh.write('</tr>\n</table>\n')

############################################
# Main function to run FastQC and generate HTML report
def run_fastqc_and_generate_html(directory):
    # Run FASTQC on all FASTQ files in the directory
    fastq_files = extract_fastq_files(directory)
    print(f"Found fastq files: {fastq_files}")

    fastq_files_concat=" ".join(fastq_files)
    # run_fastqc(fastq_files_concat)
    for fastq_file in fastq_files:
        run_fastqc(fastq_file)



    time.sleep(8) #Pause a program for a few seconds so that it has time to create all the FASTQC folders before continuing to run the program
    directory = 'C:/Users/hadar.LAPTOP-O4I2H8EK/Desktop/python_lab_project/fastqc_results'
    search_strings = ['Sequence length', 'Total Sequences', '%GC']

    # Generate HTML report
    html_file_path = 'my_report.html'
    write_empty_file(html_file_path)

    # Extract FASTQC data
    data = extract_fastqc_data(directory, search_strings)
    if data:
        table_html = create_html_table(data)
        append_to_existing_html(html_file_path, table_html)

    # Create tabulated images in HTML
    createTabulatedImages(out_fn=html_file_path, section_title='Per base quality',
                          image_fn_pattern='per_base_quality.png', directory=directory)
    createTabulatedImages(out_fn=html_file_path, section_title='Adapter Content',
                          image_fn_pattern='adapter_content.png', directory=directory)
    createTabulatedImages(out_fn=html_file_path, section_title='per_sequence_gc_content',
                          image_fn_pattern='per_sequence_gc_content.png', directory=directory)
    createTabulatedImages(out_fn=html_file_path, section_title='sequence_length_distribution',
                          image_fn_pattern='sequence_length_distribution.png', directory=directory)

    # Extract overrepresented sequences data
    overrepresented_data = extract_overrepresented_sequences(directory)
    print(overrepresented_data)
    if overrepresented_data:
        overrepresented_table_html = create_overrepresented_sequences_table(overrepresented_data)
        append_to_existing_html(html_file_path, overrepresented_table_html, title="Overrepresented sequences")

    # Close HTML tags
    with open(html_file_path, 'a') as fh:
        fh.write('</body>\n</html>\n')

    print(f"HTML report generated: {html_file_path}")



# Main execution logic to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())




