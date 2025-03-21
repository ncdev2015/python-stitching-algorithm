import cv2
import numpy as np
import matplotlib.pyplot as plt

def stitch_images(images):
    """
    Stitch multiple images together to create a panorama

    Parameters:
    images (list): List of image file paths to stitch

    Returns:
    numpy.ndarray: Stitched panorama image
    """
    # Read all images
    imgs = []
    for img_path in images:
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Could not read image: {img_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
        imgs.append(img)

    print(f"Stitching {len(imgs)} images...")

    # Create a stitcher object
    stitcher = cv2.Stitcher_create()

    # Perform stitching
    status, panorama = stitcher.stitch(imgs)

    if status != cv2.Stitcher_OK:
        error_messages = {
            cv2.Stitcher_ERR_NEED_MORE_IMGS: "Not enough images for stitching",
            cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Homography estimation failed",
            cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Camera parameter adjustment failed"
        }
        error_msg = error_messages.get(status, f"Unknown error (code: {status})")
        raise Exception(f"Stitching failed: {error_msg}")

    return panorama

def display_result(original_images, panorama):
    """
    Display original images and the resulting panorama
    """
    plt.figure(figsize=(20, 10))

    # Display original images
    for i, img_path in enumerate(original_images):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(2, len(original_images), i + 1)
        plt.imshow(img)
        plt.title(f"Image {i+1}")
        plt.axis('off')

    # Display panorama
    plt.subplot(2, 1, 2)
    plt.imshow(panorama)
    plt.title("Panorama")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def main():
    # Example usage
    image_files = [
        "image1.jpg",
        "image2.jpg",
        "image3.jpg",
        "image4.jpg",
        "image5.jpg",
        "image6.jpg",
        "image7.jpg",
    ]

    try:
        # Stitch images
        panorama = stitch_images(image_files)

        # Display results
        display_result(image_files, panorama)

        # Save the result
        cv2.imwrite("panorama.jpg", cv2.cvtColor(panorama, cv2.COLOR_RGB2BGR))
        print("Panorama saved as 'panorama.jpg'")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()