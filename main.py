from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
import gzip

pixel_size = 1


def bytes_to_decimal(bytes_obj):
    decimal_list = [b for b in bytes_obj]
    padded_length = len(decimal_list) + (3 - (len(decimal_list) % 3)) % 3
    padded_decimal_list = decimal_list + [0] * (padded_length - len(decimal_list))
    chunked_list = [padded_decimal_list[i:i + 3] for i in range(0, len(padded_decimal_list), 3)]
    return chunked_list


def open_file():
    # Reset the progress bar
    progress_bar['value'] = 0
    # Open the file dialog
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as f:
            # Compress the file data
            compressed_data = gzip.compress(f.read())
            rgb_array = bytes_to_decimal(compressed_data)

        # Create a list of images
        images = []
        current_offset = (0, 0)
        for i, rgb in enumerate(rgb_array):
            # Get the RGB values from the list
            red, green, blue = rgb
            # Create a new image with a single pixel
            img = Image.new('RGB', (pixel_size, pixel_size), color=(red, green, blue))
            # Update the offset of the image
            offset = (current_offset[0] + (i % 25) * pixel_size, current_offset[1] + (i // 25) * pixel_size)
            img.offset = offset
            # Add the image to the list
            images.append(img)

        # Calculate the final size of the image
        num_rows = (len(images) + 24) // 25
        final_size = (25 * pixel_size, num_rows * pixel_size)

        # Create the final image
        result_image = Image.new('RGB', final_size)

        # Add each image to the final image
        for i, img in enumerate(images):
            result_image.paste(img, img.offset)
            progress_bar['value'] = int((i + 1) / len(images) * 100)
            root.update_idletasks()

        # Save the image to a file
        result_image.save('result.jpeg')
        # Show a message box when done
        messagebox.showinfo("File Saved", "The result image has been saved as 'result.jpeg'.")


root = Tk()
root.title("File Chooser")

# Choose File Button
choose_file_button = Button(root, text="Choose File", command=open_file)
choose_file_button.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)

root.mainloop()
