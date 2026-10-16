# responsive-ui-visual-regression-suite

Automated UI tests for responsive viewports, dark mode CSS properties, WCAG contrast, and visual diffing.

## Overview

This repository contains an automated UI test suite built with Python's unittest and Pillow (PIL) for responsive visual regression and accessibility compliance testing.

## Key Test Coverage

- Viewport Responsive Checks: Validates dashboard layouts across standard Desktop (1440x900) and Mobile (375x812) viewports.
- Dark Mode Verification: Validates dark mode theme CSS properties including background and text color rgb() tuples.
- WCAG 2.1 AA Accessibility: Calculates color contrast ratios ensuring a minimum compliance threshold of >= 4.5:1 for normal text elements.
- Visual Image Comparison: Utilizes Pillow (ImageChops.difference) to compute bounding box pixel differences between current screenshot renders and baseline images.

## Setup and Test Execution

1. Install dependencies:
pip install pillow

2. Run test suite:
python -m unittest test_ui_layout.py -v
