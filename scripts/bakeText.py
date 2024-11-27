import os
import logging
import argparse

from PIL import Image, ImageDraw, ImageFont

FONTPATH = "/usr/share/fonts/noto/NotoSerif-Bold.ttf"
PADDING = 0.05  # 5%
SPEED_MULTIPLER = 6


def create_scrolling_text_gif(text, width, height, color, output_file="output.gif"):
    # Font setup
    try:
        font = ImageFont.truetype(FONTPATH, height - (height * PADDING))
    except IOError:
        font = ImageFont.load_default()
        logging.warning("Didn't find font!")

    # Calculate text dimensions using getbbox
    _text_bbox = font.getbbox(text)
    text_width = _text_bbox[2] - _text_bbox[0]
    text_height = _text_bbox[3] - _text_bbox[1]
    total_frames = int((text_width + width) / SPEED_MULTIPLER)

    frames = []
    for offset in range(total_frames):
        # Create a new frame
        frame = Image.new("RGB", (width, height), color=color)
        draw = ImageDraw.Draw(frame)

        # Draw the text with scrolling offset
        x_position = width - (offset * SPEED_MULTIPLER)
        y_position = -height * (2 * PADDING)
        draw.text((x_position, y_position), text, fill="black", font=font)

        # Convert frame to RGBA and append
        frames.append(frame)

    # Save as gif
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # Frame duration in milliseconds
        loop=0,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate a simple test gif with scrolling text"
    )
    parser.add_argument("-t", "--text", required=True, help="Text to scroll")
    parser.add_argument("-w", "--width", type=int, required=True, help="GIF Width")
    parser.add_argument("-H", "--height", type=int, required=True, help="Gif Height")
    parser.add_argument(
        "-c", "--color", default="white", help="Background color (default: white)"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.gif",
        help="Output GIF filename (default: output.gif)",
    )

    args = parser.parse_args()

    # Validate and create the GIF
    create_scrolling_text_gif(
        args.text, args.width, args.height, args.color, args.output
    )
    print(f"GIF saved as {args.output}")


if __name__ == "__main__":
    main()
