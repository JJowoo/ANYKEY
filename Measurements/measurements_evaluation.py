import sys
from math import sqrt, pow
from numpy import diff

"""
This script evaluates and prints the accuracy of given position estimations in a .txt document.
The document must have been created by the related LocationApp for Android in order to comply with the algorithm implemented below.
"""

def print_no_document_found_error():
    print("ERROR: No .txt document found.")
    print("Please add a .txt document as first argument when calling this script.")
    print("Note that this document has had to be created by the related \"LocationApp\" for Android.")
    print("Usage: python3 measurements_evaluation.py <your_doc.txt>")
    print("Exiting")

# Returns the amount of samples collected - necessary for mean and standard deviation calculations
def get_sample_count(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def distance_between_two_points2D(sample_point, reference_point):
    return sqrt(pow(sample_point[0] - reference_point[0], 2) + pow(sample_point[1] - reference_point[1], 2))

def distance_between_two_points3D(sample_point, reference_point):
    return sqrt(pow(sample_point[0] - reference_point[0], 2) + pow(sample_point[1] - reference_point[1], 2) + pow(sample_point[2] - reference_point[2], 2))

def standard_deviation(samples, samples_mean, samples_count):
    l = []
    for s in samples:
        squared = pow(s - samples_mean, 2)
        l.append(squared)
    std = sqrt(sum(l) / samples_count)
    return std

def evaluate_data(filename, reference_point):
    ''' Local variables '''
    # Variables making up the average coordinate
    sample_x_center = 0.0
    sample_y_center = 0.0
    sample_z_center = 0.0

    # Lists holding all coordinates on axis
    # sample_x_coords = []
    # sample_y_coords = []
    # sample_z_coords = []

    # List holding all sample points
    sample_points = []

    # Lists holding distances on each axis of a sample to reference point
    # distances_x = []
    # distances_y = []
    # distances_z = []

    # Lists holding all distances from sample points to reference point
    distances_to_ref_point_2D = []
    distances_to_ref_point_3D = []

    # Lists holding all distances from sample points to mean point
    distances_to_samples_center_point_2D = []
    distances_to_samples_center_point_3D = []
    
    # Experimental
    # Lists holding all distance differences from positions to their next one
    delta_distances_2D = []
    delta_distances_3D = []

    ''' Go! '''
    # Get amount of samples collected
    sample_count = get_sample_count(filename)

    # Go through samples
    with open(filename) as file:
        for line in file:
            # Extract x, y and z coordinates out of each line
            x = float(line.split(',')[0])
            y = float(line.split(',')[1])
            z = float(line.split(',')[2])
            
            # Add individual coordinates to coord's means (necessary for later standard deviation calculation)
            sample_x_center += x
            sample_y_center += y
            sample_z_center += z

            # Add individual coordinates to coord's lists (necessary for later standard deviation calculation)
            # sample_x_coords.append(x)
            # sample_y_coords.append(y)
            # sample_z_coords.append(z)

            # Calculate distances on each axis
            # axis_distance_x = x - reference_point[0]
            # axis_distance_y = y - reference_point[1]
            # axis_distance_z = z - reference_point[2]
            # distances_x.append(axis_distance_x)
            # distances_y.append(axis_distance_y)
            # distances_z.append(axis_distance_z)

            # Make up coordinate and add to list
            sample_point = [x, y, z]
            sample_points.append(sample_point)

            # Calculate distance of sample point to reference point in 2D and 3D and add to distances lists
            distance_to_ref_point_2D = distance_between_two_points2D(sample_point, reference_point)
            distances_to_ref_point_2D.append(distance_to_ref_point_2D)
            distance_to_ref_point_3D = distance_between_two_points3D(sample_point, reference_point)
            distances_to_ref_point_3D.append(distance_to_ref_point_3D)

    '''#############################################################
    #################### ACCURACY EVALUATION ####################
    #############################################################'''
    # Get sample mean distance on each axis
    # Variant 1
    # sample_x_mean_distance1 = sample_x_mean - reference_point[0]
    # sample_y_mean_distance1 = sample_y_mean - reference_point[1]
    # sample_z_mean_distance1 = sample_z_mean - reference_point[2]
    # Variant 2
    # sample_x_mean_distance2 = sum(distances_x) / sample_count
    # sample_y_mean_distance2 = sum(distances_y) / sample_count
    # sample_z_mean_distance2 = sum(distances_z) / sample_count

    # Calculate average, min and max distance of samples to reference point
    average_distance_to_ref_point_2D = sum(distances_to_ref_point_2D) / sample_count
    average_distance_to_ref_point_3D = sum(distances_to_ref_point_3D) / sample_count
    min_distance_to_ref_point_2D = min(distances_to_ref_point_2D)
    min_distance_to_ref_point_3D = min(distances_to_ref_point_3D)
    max_distance_to_ref_point_2D = max(distances_to_ref_point_2D)
    max_distance_to_ref_point_3D = max(distances_to_ref_point_3D)
    
    # Get standard deviation of samples on each axis x, y and z
    # sample_x_std = standard_deviation(sample_x_coords, sample_x_mean, sample_count)
    # sample_y_std = standard_deviation(sample_y_coords, sample_y_mean, sample_count)
    # sample_z_std = standard_deviation(sample_z_coords, sample_z_mean, sample_count)
    
    # Get distance standard deviations of distance to reference point
    std_2D_distances_to_ref_point = standard_deviation(distances_to_ref_point_2D, average_distance_to_ref_point_2D, sample_count)
    std_3D_distances_to_ref_point = standard_deviation(distances_to_ref_point_3D, average_distance_to_ref_point_3D, sample_count)
    
    '''#############################################################
    #################### PRECISION EVALUATION ###################
    #############################################################'''
    # Get samples center coordinates
    sample_x_center /= sample_count
    sample_y_center /= sample_count
    sample_z_center /= sample_count
    samples_center_point = [sample_x_center, sample_y_center, sample_z_center]

    # Calculate distance of each sample point to samples center point
    for sample_point in sample_points:
        distance_to_sample_center_point_2D = distance_between_two_points2D(sample_point, samples_center_point)
        distances_to_samples_center_point_2D.append(distance_to_sample_center_point_2D)
        distance_to_sample_center_point_3D = distance_between_two_points3D(sample_point, samples_center_point)
        distances_to_samples_center_point_3D.append(distance_to_sample_center_point_3D)
    
    # Calculate average, min and max distance of samples to samples center point
    average_distance_to_samples_center_point_2D = sum(distances_to_samples_center_point_2D) / sample_count
    average_distance_to_samples_center_point_3D = sum(distances_to_samples_center_point_3D) / sample_count
    min_distance_to_samples_center_point_2D = min(distances_to_samples_center_point_2D)
    min_distance_to_samples_center_point_3D = min(distances_to_samples_center_point_3D)
    max_distance_to_samples_center_point_2D = max(distances_to_samples_center_point_2D)
    max_distance_to_samples_center_point_3D = max(distances_to_samples_center_point_3D)

    # Calculate distance standard deviations of distance to samples center point
    std_2D_distances_to_samples_center_point = standard_deviation(distances_to_samples_center_point_2D, average_distance_to_samples_center_point_2D, sample_count)
    std_3D_distances_to_samples_center_point = standard_deviation(distances_to_samples_center_point_3D, average_distance_to_samples_center_point_3D, sample_count)

    # Calculate distances from samples center point to reference point
    distance_samples_center_point_to_ref_point_2D = distance_between_two_points2D(samples_center_point, reference_point)
    distance_samples_center_point_to_ref_point_3D = distance_between_two_points3D(samples_center_point, reference_point)

    # Experimental
    '''###################################################################
    #################### MOTION SICKNESS EVALUATION ###################
    ###################################################################'''
    # 2D Get mean, min and max distance differences from samples to their next ones
    delta_distances_2D = diff(distances_to_ref_point_2D)
    delta_distances_2D =  [abs(n) for n in delta_distances_2D]
    average_delta_distance_2D = sum(delta_distances_2D) / (sample_count - 1)
    min_delta_distance_2D = min(delta_distances_2D)
    max_delta_distance_2D = max(delta_distances_2D)

    # 3D Get mean, min and max distance differences from samples to their next ones
    delta_distances_3D = diff(distances_to_ref_point_3D)
    delta_distances_3D = [abs(n) for n in delta_distances_3D]
    average_delta_distance_3D = sum(delta_distances_3D) / (sample_count - 1)
    min_delta_distance_3D = min(delta_distances_3D)
    max_delta_distance_3D = max(delta_distances_3D)
    
    return sample_count, sample_x_center, sample_y_center, sample_z_center, average_distance_to_ref_point_2D, average_distance_to_ref_point_3D, min_distance_to_ref_point_2D, min_distance_to_ref_point_3D, max_distance_to_ref_point_2D, max_distance_to_ref_point_3D, std_2D_distances_to_ref_point, std_3D_distances_to_ref_point, average_distance_to_samples_center_point_2D, average_distance_to_samples_center_point_3D, min_distance_to_samples_center_point_2D, min_distance_to_samples_center_point_3D, max_distance_to_samples_center_point_2D, max_distance_to_samples_center_point_3D, std_2D_distances_to_samples_center_point, std_3D_distances_to_samples_center_point, average_delta_distance_2D, average_delta_distance_3D, min_delta_distance_2D, min_delta_distance_3D, max_delta_distance_2D, max_delta_distance_3D
        
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        print_no_document_found_error()
        sys.exit(1)
    
    direction = filename.split('(')[0]
    x_reference = float((filename.split('(')[1].split(')')[0].split('_')[0]).replace(',', '.'))
    y_reference = float((filename.split('(')[1].split(')')[0].split('_')[1]).replace(',', '.'))
    z_reference = float((filename.split('(')[1].split(')')[0].split('_')[2]).replace(',', '.'))
    reference_point = [x_reference, y_reference, z_reference]
    
    sample_count, sample_x_center, sample_y_center, sample_z_center, average_distance_to_ref_point_2D, average_distance_to_ref_point_3D, min_distance_to_ref_point_2D, min_distance_to_ref_point_3D, max_distance_to_ref_point_2D, max_distance_to_ref_point_3D, std_2D_distances_to_ref_point, std_3D_distances_to_ref_point, average_distance_to_samples_center_point_2D, average_distance_to_samples_center_point_3D, min_distance_to_samples_center_point_2D, min_distance_to_samples_center_point_3D, max_distance_to_samples_center_point_2D, max_distance_to_samples_center_point_3D, std_2D_distances_to_samples_center_point, std_3D_distances_to_samples_center_point, average_delta_distance_2D, average_delta_distance_3D, min_delta_distance_2D, min_delta_distance_3D, max_delta_distance_2D, max_delta_distance_3D = evaluate_data(filename, reference_point)
    print("\n")
    print("GENERAL INFORMATION")
    print("Direction: {}, Sample Count: {}".format(direction, sample_count))
    print("X Reference: {}, Y Reference: {}, Z Reference: {}".format(x_reference, y_reference, z_reference))
    print("X Mean: {:.3f}, Y Mean: {:.3f}, Z Mean: {:.3f}".format(sample_x_center, sample_y_center, sample_z_center))
    print("\n")
    print("ACCURACY RESULTS")
    print("Average distance to reference point 2D/3D: {:.3f}m / {:.3f}m".format(average_distance_to_ref_point_2D, average_distance_to_ref_point_3D))
    print("Min distance to reference point 2D/3D: {:.3f}m / {:.3f}m".format(min_distance_to_ref_point_2D, min_distance_to_ref_point_3D))
    print("Max distance to reference point 2D/3D: {:.3f}m / {:.3f}m".format(max_distance_to_ref_point_2D, max_distance_to_ref_point_3D))
    print("Standard deviation of distances to reference point 2D/3D: {:.3f}m / {:.3f}m".format(std_2D_distances_to_ref_point, std_3D_distances_to_ref_point))
    print("\n")
    print("PRECISION RESULTS")
    print("Average distance to samples center point 2D/3D: {:.3f}m / {:.3f}m".format(average_distance_to_samples_center_point_2D, average_distance_to_samples_center_point_3D))
    print("Min distance to samples center point 2D/3D: {:.3f}m / {:.3f}m".format(min_distance_to_samples_center_point_2D, min_distance_to_samples_center_point_3D))
    print("Max distance to samples center point 2D/3D: {:.3f}m / {:.3f}m".format(max_distance_to_samples_center_point_2D, max_distance_to_samples_center_point_3D))
    print("Standard deviation of distances to samples center point 2D/3D: {:.3f}m / {:.3f}m".format(std_2D_distances_to_samples_center_point, std_3D_distances_to_samples_center_point))
    print("\n")
    print("MOTION SICKNESS RESULTS")
    print("Average delta distance 2D/3D: {:.3f}m / {:.3f}m".format(average_delta_distance_2D, average_delta_distance_3D))
    print("Min delta distance 2D/3D: {:.3f}m / {:.3f}m".format(min_delta_distance_2D, min_delta_distance_3D))
    print("Max delta distance 2D/3D: {:.3f}m / {:.3f}m".format(max_delta_distance_2D, max_delta_distance_3D))
    print("\n")
