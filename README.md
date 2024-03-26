# THRESHOLD
Gene expression serves as one of the foundational elements in molecular biology, elucidating the functional state of a cell and providing insights into physiological and pathological processes. Variations in gene expression are most likely indicative of disease states and can be vital in understanding cellular responses, disease progression, and therapeutic susceptibilities. To effectively investigate these expression patterns, especially in large datasets, a robust and precise analysis tool is crucial. Comprehensive analyses of upregulated and downregulated genes can shed light on potential pathways and therapeutic targets. The field of genomics is currently undergoing a transformative phase, with gene expression analysis being a critical determinant of this transformation. The patterns in which genes are expressed can unveil significant insights into disease mechanisms, guide therapeutic responses, and help demystify intricate biological interactions.  

We present THRESHOLD: a novel gene saturation analysis GUI. THRESHOLD analyzes transcriptomic data across large samples of patients to understand the cohesion of the most upregulated/downregulated genes in a given disease. This lends researchers knowledge to inform network topology analyses or to assess the relative amount of genes influencing a given disease. THRESHOLD offers several features to aid in analysis including user-inputted saturation type, restriction factors, and rank type. The tool outputs an interactive graph of saturation permitting the calculation of specific saturation thresholds and most saturated genes. 

The overarching aim of "THRESHOLD" isn't only about gene identification; it seeks to deepen our understanding of the multifaceted genomic landscape. To that end, it plays a pivotal role in several key domains: (1) Disease Differentiation: Beyond simply classifying diseases according to observable symptoms, "Threshold" offers a molecular perspective, pinpointing unique genetic markers within different patient groups, facilitating a more refined and precise disease categorization. (2) Exploring Genetic Markers: In the quest for new therapeutic targets, "THRESHOLD" emerges as a potentially, spotlighting genes that consistently manifest high expression levels across diverse patients. This is particularly significant when those genes are intrinsically linked to disease pathways. (3) Early Detection: In conditions such as cancer, where prompt diagnosis is crucial, "THRESHOLD" offers valuable assistance. It helps researchers identify genes that are frequently overexpressed, suggesting their possible role as indicators of disease and aiding in the development of early detection methods. Enhancing its analytical capabilities, "THRESHOLD" includes two distinct features: "Incremental Saturation" and "Overall Saturation". The first feature focuses on unraveling the step-by-step changes in gene expression patterns, whereas the second offers a comprehensive view, encompassing the full spectrum of gene expression activity up to a specific threshold.

In summary, the "THRESHOLD" tool serves as a useful addition to genomics research. It provides insights into disease mechanisms and supports developments in personalized medicine, contributing positively to healthcare advancements.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Running the Application](#running-the-application)  
  - [File Format](#file-format) 
- [Navigation](#navigation)
  - [Uploading a File](#uploading-a-file)
  - [Calculating Saturation](#calculating-saturation)
  - [Data Output](#data-output)
  - [Run Unpaired T-Test](#run-unpaired-t-test)
  - [Assess Significance](#assess-significance)
- [Documentation](#documentation)
- [Authors](#authors)
- [Contact](#contact)
- [License](#license)

## Installation

To install `THRESHOLD` simply click the installation link below.

[MacOS Download](https://drive.google.com/file/d/17UkAbJQHSt2Yj9sFFznFbUiRfAhF1EAX/view?usp=sharing)

## Getting Started

### Running the Application

Once you have downloaded the above folder, open the entire folder in a `VScode IDE`. Ensure the `Python` and `Java` extensions are added. When ready, simply navigate to the `threshold.gui` file and press run to begin. A window should appear, prompting the input of a file. 

### File Format

`THRESHOLD` requires the input of a file of patient transcriptomic data with gene expression data in the form of zscores or percentiles comparing expression against a control population, or ranked relatively within an individual patient’s expression. 

The inputted `.txt` file must be formatted as such:

```
Hugo_Symbol        {Blank}           {Patient1ID}           {Patient2ID}...
   ...               ...         zscores/percentile...   zscores/percentile...    
   ...               ...         zscores/percentile...   zscores/percentile...    

```

* The Blank column is never actually used; it is a placeholder. Given space between the Hugo_Symbol and {Patient1ID} column, THRESHOLD will run.

* Note the first heading MUST be called Hugo_Symbol

* The columns must be separated by a tab `'\t'`

## Navigation

### Uploading a File
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page1.png?raw=true" alt="Page 1 Image" height= 240 align = "left" >

To begin the analysis, simply upload a `.txt` file in the appropriate [file format](#file-format) by clicking on the `Open File` button. 

Once the button is clicked, about 5 seconds while the pseudogenes are removed and you will automatically move to the next page.

To view `info` and `documentation` of the tool, press the appropriate icons in the `GUI` toolbar.

<br clear="left"/>

### Calculating Saturation
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page2.png?raw=true" alt="Page 2 Image" height= 240 align = "left"  >

Confirm your file is uploaded with the dialog below the `Generate` button.

Input the parameters according to your desired analyses. Clicking on the `ⓘ` icons will provide a detailed explanation of the parameter's domains and purpose.

Once satisfied with your inputs, press `Generate`. If the inputted file is formatted correctly, and the inputs accurate, an `In progress...` text dialog will appear. For a dataset of about 400 patients, you will need to wait about 2 minutes for the calculations to be made.

If you would like to restart your analyses with a different file, press the restart button in the top right corner. 
<br clear="left"/>

### Data Output
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page3.png?raw=true" alt="Page 3 Image" height= 240 align = "left" style = "margin-bottom: 20px" >

A saturation curve will appear indicating `saturation type` by `nth ranked gene`. See documentation for methods.

Hover over the graph to find specific saturation values. Alternatively, use the `Find Threshold` input to find when a certain saturation level is reached and the `Specific Value` input to evaluate the saturation of a specific `nth gene`. Clicking on the `ⓘ` icons will provide a detailed explanation of the parameter's domains and purpose.

Additionally, you can find the most saturated genes with the `Top x Saturated Genes` button. Simply enter the number of top genes you want to find in the `x:` parameter and press the button. 

To export a `.png` file of the Graph, a `.txt` file of the Data or a `.txt` file of removed pseudogenes, press the corresponding buttons above the graph.

To begin a new analysis with the same file, press the back button. If you would like to restart your analysis entirely, press the restart button.

### Run Unpaired T Test
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page4.png?raw=true" alt="Page 4 Image" height= 240 align = "left" style = "margin-bottom: 20px" >

`THRESHOLD` facilitates the statistical comparison between two saturation data sets to assess whether there are statistically significant differences between samples to provide additional insights in user analyses. 

Upload the two `saturation files` you would like to compare by clicking on the black fields.

Ensure the files are in the proper, standard format `(.txt)` as exported by the `THRESHOLD` tool. The files should have three columns, `“Nth Gene Included,”` `“Incremental Saturation,”` and `“Overall Saturation.”` The file should be the same size; ie, the same number of rows.

To run the test, simply press the `Run Unpaired-T-Test` button.

To navigate back home, simply press restart in the top right corner. 

### Assess Significance
<img src="https://github.com/alperuzun/THRESHOLD/blob/main/threshold/assets/page5.png?raw=true" alt="Page 5 Image" height= 240 align = "left" style = "margin-bottom: 20px" >

This page simply outlines the result of your analyses, describing whether the differences between the saturation types in each data set yielded `statistically significant` differences. 

This result is outlined in the orange box. Additional relevant statistical measures, including the calculated `p-value`, are also listed.

To download a more detailed description of the statistical analyses, press `“Download Full Report”` to export a `(.txt)` file of relevant calculated statistical measures for each of the saturation types.

To begin a new statistical analysis, press the back button. If you would like to restart entirely and navigate back home, press the back button. 

## Documentation
To view the workflow of `THRESHOLD` in addition to a more in-depth analysis of standardization options and validation of calculations click the link to the `.pdf` file below.

[THRESHOLD Documentation](https://drive.google.com/file/d/17UkAbJQHSt2Yj9sFFznFbUiRfAhF1EAX/view?usp=sharing)

## Authors

This project was developed by `Finán Gammell`, `Jennifer Li`, `Christopher Elco`, `Jessica Plavicki`, and `Dr. Alper Uzun` in the Uzun Lab at Brown University. 

## Contact
Reach out to alper_uzun@brown.edu with any questions.

## License 

`The MIT License (MIT)`

Copyright (c) 2023 Finán Gammell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
