import rasterio #new package that 
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import pdb
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

# Process each .bil file
for bil_file in bil_files:
    bil_base_name = os.path.splitext(os.path.basename(bil_file))[0]
    
    # Check if the matching .prj file exists
    matching_prj = prj_file_map.get(bil_base_name)
    
    if matching_prj:
        print(f"Found matching .prj for {bil_file}: {matching_prj}")
        with open(matching_prj, 'r') as prj_file:
            prj_content = prj_file.read()
            print(f"Projection info from {matching_prj}: {prj_content}")
    
    with rasterio.open(bil_file) as src:
        # Read the data from the first band of the .bil file
        data = src.read(1)  # Assuming single-band data
        
        # Get the CRS from the .bil metadata, if available
        crs = src.crs
        
        if crs is None and matching_prj:
            print(f"Manually applying CRS from .prj file for {bil_file}")
            crs = prj_content  # Placeholder - In practice, you'd convert this to a valid CRS format.
        elif crs is None:
            print(f"Warning: No CRS found or .prj file available for {bil_file}")
        
        # Optionally, apply some scaling or normalization to the data
        data = np.clip(data, np.percentile(data, 2), np.percentile(data, 98))  # Clip outliers
        data = (data - data.min()) / (data.max() - data.min())  # Normalize data to 0-1
        
        # Generate the output PNG file path
        base_name = os.path.basename(bil_file).replace('.bil', '.png')
        output_png = os.path.join(output_dir, base_name)
        
        # Apply a colormap to the data (e.g., 'viridis', 'plasma', 'inferno', etc.)
        plt.imshow(data, cmap='viridis')  # Change colormap here
        plt.title(f"Projection: {crs}")  # Add the CRS info in the title (optional)
        plt.axis('off')  # Hide the axis
        
        # Save the plot as PNG
        plt.savefig(output_png, bbox_inches='tight', pad_inches=0)
        plt.close()

    print(f"Converted {bil_file} to {output_png}")