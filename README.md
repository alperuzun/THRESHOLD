# THRESHOLD

THRESHOLD is a novel gene saturation analysis GUI. THRESHOLD analyzes transcriptomic data across large samples of patients to understand the cohesion of the most upregulated/downregulated genes in a given disease. This lends researchers knowledge to inform network topology analyses or to assess the relative amount of genes influencing a given disease. THRESHOLD offers several features to aid in analysis including user-inputted saturation type, restriction factors, and rank type. The tool outputs an interactive graph of saturation permitting the calculation of specific saturation thresholds and most saturated genes. 

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Running the Application](#running-the-application)  
  - [File Format](#file-format) 
- [Navigation](#navigation)
  - [Page 1 Uploading a File](#page-1-uploading-a-file)
  - [Page 2 Calculating Saturation](#page-2-calculating-saturation)
  - [Page 3 Data Output](#page-3-data-output)
- [Documentation](#documentation)
- [Authors](#authors)
- [License](#license)

## Installation

To install `THRESHOLD` simply click the installation link below.

[MacOS Download](https://drive.google.com/file/d/18cO7RbVLj3etOX_sD0buZmvnxIPaHjb6/view?usp=sharing){:target="_blank"}

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

### Page 1 Uploading a File
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page1.png?raw=true" alt="Page 1 Image" height= 220 align = "left" >

To begin the analysis, simply upload a `.txt` file in the appropriate [file format](#file-format) by clicking on the `Open File` button. Wait about 5 seconds while the pseudogenes are removed, and you will automatically move to the next page.

To view `info` and `documentation` of the tool, press the appropriate icons in the `GUI` toolbar.

<br clear="left"/>

### Page 2 Calculating Saturation
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page2.png?raw=true" alt="Page 2 Image" height= 220 align = "left"  >

Confirm your file is uploaded with the dialog below the `Generate` button.

Input the parameters according to your desired analyses. Clicking on the `ⓘ` icons will provide a detailed explanation of the parameter's domains and purpose.

Once satisfied with your inputs, press `Generate`. If the inputted file is formatted correctly, and the inputs accurate, an `In progress...` text dialog will appear. For a dataset of about 400 patients, you will need to wait about 2 minutes for the calculations to be made.

If you would like to restart your analyses with a different file, press the restart button in the top right corner. 
<br clear="left"/>
### Page 3 Data Output
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page3.png?raw=true" alt="Page 3 Image" height= 220 align = "left" style = "margin-bottom: 20px" >

A saturation curve will appear indicating `saturation type` by `nth ranked gene`. See documentation for methods.

Hover over the graph to find specific saturation values. Alternatively, use the `Find Threshold` input to find when a certain saturation level is reached and the `Specific Value` input to evaluate the saturation of a specific `nth gene`. Clicking on the `ⓘ` icons will provide a detailed explanation of the parameter's domains and purpose.

Additionally, you can find the most saturated genes with the `Top x Saturated Genes` button. Simply enter the number of top genes you want to find in the `x:` parameter and press the button. 

To export a `.png` file of the Graph, a `.txt` file of the Data or a `.txt` file of removed pseudogenes, press the corresponding buttons above the graph.

To begin a new analysis with the same file, press the back button. If you would like to restart your analysis entirely, press the restart button.

## Documentation
To view the workflow of `THRESHOLD` in addition to a more in-depth analysis of standardization options and validation of calculations click the link to the '.pdf' file below.

[THRESHOLD Documentation](https://docs.google.com/document/d/1NeoYF399lZUFfhjw6PwqiMv5RLBK1n9e/edit?usp=sharing&ouid=103062979408675113645&rtpof=true&sd=true){:target="_blank"}

## Authors

This project was developed by `Finán Gammell`, `Jennifer Li` and `Dr. Alper Uzun` in the Uzun Lab at Brown University. 

## License 

`The MIT License (MIT)`

Copyright (c) 2023 Finán Gammell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
