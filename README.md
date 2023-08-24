# THRESHOLD

THRESHOLD is a novel gene saturation analysis GUI. THRESHOLD analyzes transcriptomic data across large samples of patients to understand the cohesion of the most upregulated/downregulated genes in a given disease. This lends researchers knowledge to inform network topology analyses or to assess the relative amount of genes influencing a given disease. THRESHOLD offers several features to aid in analysis including user-inputted saturation type, restriction factors, and rank type. The tool outputs an interactive graph of saturation permitting the calculation of specific saturation thresholds and most saturated genes. 

## Table of contents

- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Running the Application](#running-the-application)  
  - [File Format](#file-format) 
- [Navigation](#navigation)
- [Output](#output)

## Installation

To install `THRESHOLD` simply click the installation link below.

LINK

## Getting Started

### Running the Application

Once you have downloaded the above folder, open the entire folder in a `VScode IDE`. Ensure the `Python` and `Java` extensions are added. When ready, simply navigate to the `threshold.gui` file and press run to begin. A window should appear, prompting the input of a file. 

### File Format

`THRESHOLD` requires the input of a file of patient transcriptomic data with gene expression zscores ideally compared with a control population. 

The inputted `.txt` file must be formatted as such:

```
Hugo_Symbol     Entrez_Gene_Id      {Patient1ID}    {Patient2ID}...
   ...               ...              zscores...       zscores...
   ...               ...              zscores...       zscores... 
```

* The Entrez_Gene_Id column is never actually used; it is a placeholder. As long as there is a space between the Hugo_Symbol and {Patient1ID} column it will run.

* Note the first heading MUST be called Hugo_Symbol

* The columns must be separated by a tab `'\t'`

## Navigation

### Page 1 | Uploading a File
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/page1.png?raw=true" alt="Page 1 Image" style= "max-height: 100px;">
To begin the analysis, simply upload a .txt file in the appropriate [file format](#file-format) by clicking on the upload file button.

To view info and documentation of the tool, press the appropriate icons in the GUI toolbar.
### Page 2 | Calculating Saturation

### Page 3 | Data Output

## Output

## Authors

This project was developed by Finán Gammell with support from Jennifer Li and Dr. Alper Uzun in the Uzun Lab at Brown University. 

## License 

The MIT License (MIT)

Copyright (c) 2023 Finán Gammell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
