# Create Custom Accuracy Assessment Points
## Gray McKenna | WA DNR Nearshore Habitat Program

### Overview
This tool calculates the minimum number of accuracy assessment sample points required to meet the user-specified confidence (95% recommended), based on the equation described in Congalton & Green 2019. It is for **binary** (2-class) classification products ONLY. Optionally, the user can specify a minimum number of points per class (50 recommended). These points will be distributed using an equal stratified random approach, and the remaining points will be distributed proportionally according to class cover using a stratified random approach. This points distribution method is appropriate when the producer is primarily interested in the lowest cover class. This was designed for accuracy assessments of floating kelp classification products. **Spatial Analyst license extension required.**

### How to Use this Tool
Download the .atbx file from this repository and add it to your Pro project by right-clicking Toolboxes in your Catalog pane, selecting Add New Toolbox, and navigate to wherever you saved the .atbx file. Once you add it to your project, you can open it, right click on the script tool, and click "Open."

### Min Number of Points
The minimum number of points required (𝑛) is based on the user-specified confidence and the proportional coverage of the classes, using the equation derived from Congalton & Green 2019: 

### 𝑛=𝐵∗Π(1−Π)/𝛽^2

Where:
- Π = proportion of coverage of class closest to 50%
- 𝐵 = 𝜒_((1,𝑦))   𝑤ℎ𝑒𝑟𝑒 𝑦=1− 𝛼/𝑘 
    - 𝜒_((1,𝑦)) is the inverse of the right-tailed chi-squared distribution
    - 𝛼 is the confidence expressed as a proportion (e.g. 0.95 for 95)
    - 𝑘 is the number of classes (always 2 in this case)
- 𝛽 = the margin of error (precision), calculated here as (100-confidence)/100 

For more info, see Congalton, R. G., & Green, K. (2019). Assessing the Accuracy of Remotely Sensed Data: Principles and Practices. CRC Press.