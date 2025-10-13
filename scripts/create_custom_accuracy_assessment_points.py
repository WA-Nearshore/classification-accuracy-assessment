# Generate accuracy assessment points with minimum points per class
# For BINARY classification products
# Uses multinomial distribution described in Congalton & Green 2019

import arcpy
from scipy.stats import chi2

class LicenseError(Exception):
    pass

arcpy.env.overwriteOutput = True

# Define main function
def create_acc_points(inputRaster, 
                      inputMinPointsPerClass,
                      inputConfidence, 
                      outputPointFeatures):
    # Calculate minimum points required to meet confidence interval 
    arcpy.AddMessage("Calculating minimum points required...")
    count0 = 0
    count1 = 0

    try:
        # Check if a raster attribute table (RAT) exists
        raster = arcpy.Raster(inputRaster)
        if not raster.hasRAT:
            arcpy.AddMessage("Raster attribute table does not exist.")
            arcpy.AddMessage("Calculating raster attribute table...")
            # Build the RAT if it does not exist
            arcpy.BuildRasterAttributeTable_management(inputRaster, "Overwrite")

        # Use a SearchCursor to read the VALUE and COUNT fields
        with arcpy.da.SearchCursor(inputRaster, ["VALUE", "COUNT"]) as cursor:
            for value,count in cursor:
                if value == 0:
                    count0 = count
                elif value == 1:
                    count1 = count

    except arcpy.ExecuteError:
        arcpy.AddMessage(arcpy.GetMessages(2))
    except Exception as e:
        arcpy.AddMessage(f"An error occurred: {e}")

    ## Calculate class coverage 
    cov0 = count0 / (count0 + count1)
    cov1 = count1 / (count0 + count1)

    arcpy.AddMessage(f"This raster is {round(cov0*100)}% class0 and {round(cov1*100)}% class1")

    ## Calculate Π * (1-Π)
    pi_var = max([cov0, cov1]) * (1 - max([cov0, cov1]))

    ## Calculate B 
    B = chi2.isf(((1 - inputConfidence/100) / 2), 1)

    ## Calculate n
    n = B*pi_var/(((100-inputConfidence)/100) ** 2)

    arcpy.AddMessage(f"Sample Points Required: {round(n)}")

    arcpy.AddMessage("Checking Spatial Analyst license availability...")
    try:
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise LicenseError

    except LicenseError:
        arcpy.AddMessage("3D Analyst license is unavailable")
    except arcpy.ExecuteError:
        arcpy.AddMessage(arcpy.GetMessages(2))

    # Create accuracy assessment points for MinPoints
    arcpy.AddMessage("Creating Accuracy Assessment Points...")
    if inputMinPointsPerClass > 0:
        arcpy.sa.CreateAccuracyAssessmentPoints(in_class_data=inputRaster,
                                                out_points="memory\points1",
                                                target_field="CLASSIFIED",
                                                num_random_points=(inputMinPointsPerClass*2),
                                                sampling="EQUALIZED_STRATIFIED_RANDOM")

    # Create accuracy assessment points by proportionally distributing the rest
    arcpy.sa.CreateAccuracyAssessmentPoints(in_class_data=inputRaster,
                                            out_points="memory\points2",
                                            target_field="CLASSIFIED",
                                            num_random_points=(round(n-(2*inputMinPointsPerClass))),
                                            sampling="EQUALIZED_STRATIFIED_RANDOM")

    # Merge the classes and write output
    arcpy.management.Merge(
        ["memory\points1", "memory\points2"],
        outputPointFeatures
    )

    arcpy.management.Delete("memory\points1")
    arcpy.management.Delete("memory\points2")

    arcpy.AddMessage(f"Tool complete. Output points written to {outputPointFeatures}")

# Inputs: raster, target field, confidence interval, min number of points per class 
inputRaster = arcpy.GetParameterAsText(0)
inputMinPointsPerClass = int(arcpy.GetParameterAsText(1))
inputConfidence = float(arcpy.GetParameterAsText(2))

# Output: the sample points
outputPointFeatures = arcpy.GetParameterAsText(3)

create_acc_points(inputRaster=inputRaster, inputMinPointsPerClass=inputMinPointsPerClass,
                  inputConfidence=inputConfidence, outputPointFeatures=outputPointFeatures)
