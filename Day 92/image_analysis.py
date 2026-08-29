"""
Day 92 — Personal Portfolio Project: Image Analysis Dashboard
Combines Image Processing (Pillow) with Data Science (Pandas/Matplotlib) —
scans a folder of images, extracts stats (dimensions, file size, average
brightness, dominant color), and visualizes patterns across the whole set.

Run: python image_analysis.py [folder_path]
Defaults to "sample_images" if no folder is given.
"""

import os
import sys
from pathlib import Path

from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_dominant_color(img: Image.Image, resize_to=50) -> tuple:
    """Downscale the image for speed, then find the most common RGB color."""
    small_img = img.convert("RGB").resize((resize_to, resize_to))
    pixels = np.array(small_img).reshape(-1, 3)
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    most_common = colors[np.argmax(counts)]
    return tuple(int(c) for c in most_common)


def get_average_brightness(img: Image.Image) -> float:
    """Convert to grayscale and return the mean pixel value (0=black, 255=white)."""
    grayscale = np.array(img.convert("L"))
    return float(grayscale.mean())


def analyze_image(filepath: Path) -> dict:
    """Extract all stats for a single image file."""
    with Image.open(filepath) as img:
        width, height = img.size
        dominant_color = get_dominant_color(img)
        brightness = get_average_brightness(img)

    return {
        "filename": filepath.name,
        "width": width,
        "height": height,
        "aspect_ratio": round(width / height, 2),
        "megapixels": round((width * height) / 1_000_000, 2),
        "file_size_kb": round(filepath.stat().st_size / 1024, 1),
        "brightness": round(brightness, 1),
        "dominant_r": dominant_color[0],
        "dominant_g": dominant_color[1],
        "dominant_b": dominant_color[2],
    }


def analyze_folder(folder_path: str) -> pd.DataFrame:
    """Analyze every supported image in a folder and return a DataFrame."""
    folder = Path(folder_path)
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    records = []
    for filepath in sorted(folder.iterdir()):
        if filepath.suffix.lower() in valid_extensions:
            try:
                records.append(analyze_image(filepath))
            except Exception as e:
                print(f"⚠️  Skipped {filepath.name}: {e}")

    return pd.DataFrame(records)


def print_summary(df: pd.DataFrame):
    print("=" * 60)
    print(f"IMAGE ANALYSIS SUMMARY — {len(df)} images")
    print("=" * 60)
    print(df[["filename", "width", "height", "megapixels", "file_size_kb", "brightness"]]
          .to_string(index=False))

    print("\n" + "=" * 60)
    print("AGGREGATE STATS")
    print("=" * 60)
    print(f"Average resolution:    {df['width'].mean():.0f} x {df['height'].mean():.0f}")
    print(f"Average file size:     {df['file_size_kb'].mean():.1f} KB")
    print(f"Average brightness:    {df['brightness'].mean():.1f} / 255")
    print(f"Brightest image:       {df.loc[df['brightness'].idxmax(), 'filename']} "
          f"({df['brightness'].max():.1f})")
    print(f"Darkest image:         {df.loc[df['brightness'].idxmin(), 'filename']} "
          f"({df['brightness'].min():.1f})")
    print(f"Largest file:          {df.loc[df['file_size_kb'].idxmax(), 'filename']} "
          f"({df['file_size_kb'].max():.1f} KB)")


def plot_brightness_chart(df: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    colors = [f"#{int(r):02x}{int(g):02x}{int(b):02x}"
              for r, g, b in zip(df["dominant_r"], df["dominant_g"], df["dominant_b"])]
    sorted_df = df.sort_values("brightness")
    plt.barh(sorted_df["filename"], sorted_df["brightness"],
              color=[colors[i] for i in sorted_df.index])
    plt.xlabel("Average Brightness (0-255)")
    plt.title("Image Brightness Comparison (bar color = dominant color)")
    plt.tight_layout()
    plt.savefig("chart_1_brightness.png")
    plt.close()
    print("\n✅ Saved chart_1_brightness.png")


def plot_dominant_color_swatches(df: pd.DataFrame):
    fig, axes = plt.subplots(1, len(df), figsize=(2 * len(df), 2.5))
    if len(df) == 1:
        axes = [axes]
    for ax, (_, row) in zip(axes, df.iterrows()):
        color = (row["dominant_r"] / 255, row["dominant_g"] / 255, row["dominant_b"] / 255)
        ax.imshow([[color]])
        ax.set_title(row["filename"], fontsize=7, rotation=0)
        ax.axis("off")
    plt.suptitle("Dominant Color per Image")
    plt.tight_layout()
    plt.savefig("chart_2_dominant_colors.png")
    plt.close()
    print("✅ Saved chart_2_dominant_colors.png")


def plot_resolution_scatter(df: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    plt.scatter(df["width"], df["height"], s=df["file_size_kb"] * 3, alpha=0.6, color="#2A9D8F")
    for _, row in df.iterrows():
        plt.annotate(row["filename"], (row["width"], row["height"]), fontsize=7,
                     xytext=(5, 5), textcoords="offset points")
    plt.xlabel("Width (px)")
    plt.ylabel("Height (px)")
    plt.title("Image Resolutions (bubble size = file size)")
    plt.tight_layout()
    plt.savefig("chart_3_resolution_scatter.png")
    plt.close()
    print("✅ Saved chart_3_resolution_scatter.png")


if __name__ == "__main__":
    target_folder = sys.argv[1] if len(sys.argv) > 1 else "sample_images"

    df = analyze_folder(target_folder)

    if df.empty:
        print(f"No supported images found in '{target_folder}'.")
        sys.exit(0)

    print_summary(df)
    plot_brightness_chart(df)
    plot_dominant_color_swatches(df)
    plot_resolution_scatter(df)

    df.to_csv("image_analysis_results.csv", index=False)
    print("✅ Saved image_analysis_results.csv")
    print("\nAll steps completed successfully.")
