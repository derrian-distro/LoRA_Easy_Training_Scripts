import argparse

import popup_modules
import sd_scripts.tools.resize_images_to_resolution as resize
import os


def main():
    parser = argparse.ArgumentParser(
        description='Resize images in a folder to a specified max resolution(s) / '
                    '指定されたフォルダ内の画像を指定した最大画像サイズ（面積）以下にアスペクト比を維持したままリサイズします')
    parser.add_argument('src_img_folder', type=str, help='Source folder containing the images / 元画像のフォルダ')
    parser.add_argument('dst_img_folder', type=str,
                        help='Destination folder to save the resized images / リサイズ後の画像を保存するフォルダ')
    parser.add_argument('--max_resolution', type=str,
                        help='Maximum resolution(s) in the format "512x512,384x384, etc, etc" / 最大画像サイズをカンマ区切りで指定 ("512x512,384x384, etc, etc" など)',
                        default="512x512,384x384,256x256,128x128")
    parser.add_argument('--divisible_by', type=int,
                        help='Ensure new dimensions are divisible by this value / リサイズ後の画像のサイズをこの値で割り切れるようにします',
                        default=1)
    parser.add_argument('--interpolation', type=str, choices=['area', 'cubic', 'lanczos4'],
                        default='area', help='Interpolation method for resizing / リサイズ時の補完方法')
    parser.add_argument('--save_as_png', action='store_true', help='Save as png format / png形式で保存')
    parser.add_argument('--copy_associated_files', action='store_true',
                        help='Copy files with same base name to images (captions etc) / 画像と同じファイル名（拡張子を除く）のファイルもコピーする')

    args = ["--save_as_png", "--copy_associated_files", "--divisible_by=64"]
    args.insert(0, popup_modules.ask_dir("Select your source image folder"))
    args.insert(1, popup_modules.ask_dir("select your output image folder"))
    check = popup_modules.CheckBox("Select the sizes you want to resize to",
                                   ["832x832", "768x768", "512x512", "384x384", "256x256", "128x128"],
                                   "Closing this window will set the values to the defaults of: "
                                   "512x512,384x384,256x256,128x128\nDo you want to cancel?")
    sizes: list[str] = []
    if not check.no_select:
        sizes += check.get_values()
    else:
        sizes += ["512x512", "384x384", "256x256", "128x128"]
    rad = popup_modules.RadioBox("Select which Interpolation method you want to use ot resize the images",
                                 ["area", "cubic", "lanczos4"], "Closing this window will set the value to the "
                                                                "default of lanczos4\nDo you want to cancel?")
    if rad.get_value() == "":
        args.append(f"--interpolation=lanczos4")
    else:
        args.append(f"--interpolation={rad.get_value()}")
    args = parser.parse_args(args)
    for size in sizes:
        if not os.path.exists(os.path.join(args.dst_img_folder, size)):
            os.makedirs(os.path.join(args.dst_img_folder, size))
        resize.resize_images(args.src_img_folder, os.path.join(args.dst_img_folder, size), size,
                             args.divisible_by, args.interpolation, args.save_as_png, args.copy_associated_files)


if __name__ == "__main__":
    main()
