import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

# Directory containing the .bil files
input_dir = r"C:\Users\jt4ha\Dark Sky Data Dropbox\JT Turner\Downloads\databil\yeet"

# Use glob to get a list of all .bil files in the directory
bil_files = glob.glob(os.path.join(input_dir, "*.bil"))
prj_files = glob.glob(os.path.join(input_dir, "*.prj"))

# Directory to save the PNG files
output_dir = r"C:\Users\jt4ha\Dark Sky Data Dropbox\JT Turner\Downloads\Starter_Code(13)\Project3-Climate-Change\png_maps"
os.makedirs(output_dir, exist_ok=True)

# Create a dictionary to map .bil files to their corresponding .prj files
prj_file_map = {os.path.splitext(os.path.basename(prj))[0]: prj for prj in prj_files}

# Set the normalization range for all graphs so that it matches the data that was given on the prisim cite
norm_min = 0
norm_max = 170

# Process each .bil file
for bil_file in bil_files:
    bil_base_name = os.path.splitext(os.path.basename(bil_file))[0]
    
    # Extract the year from the file name (assuming the year is the 5th part when split by "_")
    year = bil_base_name.split('_')[4]  # Extract year from file name
    matching_prj = prj_file_map.get(bil_base_name)
    
    if matching_prj:
        print(f"Found matching .prj for {bil_file}: {matching_prj}")
        with open(matching_prj, 'r') as prj_file:
            prj_content = prj_file.read()
            print(f"Projection info from {matching_prj}: {prj_content}")
    
    with rasterio.open(bil_file) as src:
      
        data = src.read(1)
        
        # Get the CRS from the .bil metadata, if available crs/.prj is the actual data to be placed over the projection
        crs = src.crs
        
        if crs is None and matching_prj: # data is not constent about crs incoporation into the bil file so use prj instead
            print(f"Manually applying CRS from .prj file for {bil_file}")
            crs = prj_content  # Placeholder - In practice, you'd convert this to a valid CRS format.
        elif crs is None:
            print(f"Warning: No CRS found or .prj file available for {bil_file}")
        
        # Normalize the data to fit between 0 and 170 inches
        # Normalize data by scaling it to fit within the range [0, 170]
        data_min = np.min(data)
        data_max = np.max(data)
        data = (data - data_min) / (data_max - data_min) * (norm_max - norm_min)
        
        # Generate the output PNG file path
        base_name = os.path.basename(bil_file).replace('.bil', '.png')
        output_png = os.path.join(output_dir, base_name)
        
        plt.imshow(data, cmap='plasma', vmin=norm_min, vmax=norm_max) 
        
        # Add title with the year and CRS info
        plt.title(f"Year: {year}")
        
        
        cbar = plt.colorbar()
        cbar.set_label('Precipitation (inches)')  
        
     
        plt.axis('off')  # Hide the axis
        
        # Save the plot as PNG
        plt.savefig(output_png, bbox_inches='tight', pad_inches=0)
        plt.close()

    print(f"Converted {bil_file} to {output_png}")
