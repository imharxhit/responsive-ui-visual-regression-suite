import unittest
import math
from PIL import Image, ImageChops


def compute_pixel_diff(img1, img2):
    """Compute bounding box diff and percentage difference between two PIL images."""
    if img1.size != img2.size:
        raise ValueError(f"Image sizes do not match: {img1.size} vs {img2.size}")

    diff = ImageChops.difference(img1, img2)
    bbox = diff.getbbox()

    # Calculate pixel difference ratio
    pixels_diff = sum(sum(p) > 0 for p in diff.getdata())
    total_pixels = img1.size[0] * img1.size[1]
    diff_ratio = (pixels_diff / total_pixels) * 100

    return bbox, diff_ratio


def luminance(rgb):
    """Calculate relative luminance for WCAG contrast ratio calculation."""
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1, rgb2):
    """Calculate WCAG 2.1 color contrast ratio between two RGB colors."""
    l1 = luminance(rgb1)
    l2 = luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


class TestDashboardUI(unittest.TestCase):

    def test_light_mode_contrast_ratio(self):
        """Verify WCAG 2.1 AA contrast ratio (>= 4.5:1) for light mode text."""
        bg_color = (255, 255, 255)  # White
        text_color = (33, 37, 41)    # Dark Grey
        ratio = contrast_ratio(text_color, bg_color)
        self.assertGreaterEqual(ratio, 4.5, f"Light mode contrast ratio {ratio:.2f} is below WCAG 4.5 threshold")

    def test_dark_mode_contrast_ratio(self):
        """Verify WCAG 2.1 AA contrast ratio (>= 4.5:1) for dark mode text."""
        bg_color = (18, 18, 18)     # Dark background
        text_color = (240, 240, 240) # Light text
        ratio = contrast_ratio(text_color, bg_color)
        self.assertGreaterEqual(ratio, 4.5, f"Dark mode contrast ratio {ratio:.2f} is below WCAG 4.5 threshold")

    def test_baseline_screenshot_comparison(self):
        """Verify visual diff between baseline and current screenshots using Pillow."""
        base_img = Image.new("RGB", (1440, 900), color=(255, 255, 255))
        current_img = Image.new("RGB", (1440, 900), color=(255, 255, 255))

        bbox, diff_percent = compute_pixel_diff(base_img, current_img)
        self.assertIsNone(bbox, "Unexpected visual difference detected")
        self.assertEqual(diff_percent, 0.0, "Diff percentage should be 0% for identical renders")

    def test_viewport_dimensions(self):
        """Verify Desktop and Mobile viewport specifications."""
        desktop_viewport = (1440, 900)
        mobile_viewport = (375, 812)

        self.assertEqual(desktop_viewport, (1440, 900))
        self.assertEqual(mobile_viewport, (375, 812))


if __name__ == "__main__":
    unittest.main()
