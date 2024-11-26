from PIL import Image
import os

def create_collage(image_paths, output_path, output_format):
    try:
        # Check if exactly 4 images are provided
        if len(image_paths) != 4:
            print("Error: Please provide exactly 4 image paths.")
            return

        # Verify all image paths and load images
        images = []
        for path in image_paths:
            if not os.path.exists(path):
                print(f"Error: File not found - {path}")
                return
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                print(f"Error: Unable to load image '{path}'. Reason: {e}")
                return

        # Resize images to the smallest dimensions among them
        min_width = min(img.width for img in images)
        min_height = min(img.height for img in images)
        resized_images = [img.resize((min_width, min_height)) for img in images]

        # Create a blank canvas for the collage
        collage_width = min_width * 2
        collage_height = min_height * 2
        collage = Image.new("RGB", (collage_width, collage_height))

        # Arrange images in a 2x2 grid
        positions = [
            (0, 0),  # Top-left
            (min_width, 0),  # Top-right
            (0, min_height),  # Bottom-left
            (min_width, min_height),  # Bottom-right
        ]
        for img, pos in zip(resized_images, positions):
            collage.paste(img, pos)

        # Map common aliases like 'jpg' to 'JPEG'
        format_mapping = {"jpg": "JPEG", "png": "PNG", "bmp": "BMP", "tiff": "TIFF"}
        output_format = format_mapping.get(output_format.lower(), output_format.upper())

        # Save the collage
        collage.save(output_path, format=output_format)
        print(f"Collage saved successfully as '{output_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Please enter the paths for the 4 images to create a 2x2 collage.")
    image_paths = [
        input("Path for Image 1: ").strip(),
        input("Path for Image 2: ").strip(),
        input("Path for Image 3: ").strip(),
        input("Path for Image 4: ").strip(),
    ]
    output_format = input("Please specify the output file format (jpg, png, bmp, tiff): ").strip().lower()
    output_name = input("Enter the name of the output file (without extension): ").strip()

    # Append format extension to the output file
    output_file = f"{output_name}.{output_format}"
    create_collage(image_paths, output_file, output_format)
