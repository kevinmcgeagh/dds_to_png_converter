# DDS to 16-bit PNG Converter

This project provides a graphical user interface (GUI) application for batch converting DDS (DirectDraw Surface) files to 16-bit PNG format. It uses multiple libraries and methods to ensure the highest possible success rate in conversion.

## Features

- Batch conversion of DDS files to 16-bit PNG format
- User-friendly GUI for selecting source and destination folders
- Multiple conversion methods (Pillow, ImageIO, OpenCV, PyGame, DirectXTex)
- Progress bar and estimated time of arrival (ETA) display
- Live log of conversion process
- Image preview of converted files

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- Pillow
- NumPy
- ImageIO
- OpenCV (cv2)
- PyGame
- DirectXTex (texconv.exe should be in the system PATH)

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages:

```
pip install pillow numpy imageio opencv-python pygame
```

3. Ensure that `texconv.exe` from DirectXTex is installed and added to your system PATH.

## Usage

1. Run the script:

```
python Main.py
```

2. Use the "Browse" buttons to select the source folder containing DDS files and the destination folder for the converted PNG files.
3. Click "Start Conversion" to begin the batch conversion process.
4. Monitor the progress through the progress bar, ETA, and log messages.
5. Once completed, a message box will appear to confirm the successful conversion.

## How it works

The converter attempts to convert DDS files using multiple methods in the following order:

1. Pillow
2. ImageIO
3. OpenCV
4. PyGame
5. DirectXTex (via texconv.exe)

If one method fails, it moves on to the next until successful conversion or all methods are exhausted.

## Notes

- The application preserves the folder structure from the source directory in the destination directory.
- Converted images are displayed in a preview window during the conversion process.
- If a conversion fails with all methods, an error message is logged, and the process continues with the next file.

## Contributing

Contributions to improve the converter or add new features are welcome. Please feel free to submit pull requests or open issues on the GitLab repository.

## License

This project is licensed under the Apache License, Version 2.0. You may obtain a copy of the license at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Troubleshooting

If you encounter any issues:

1. Ensure all required libraries are correctly installed.
2. Check that `texconv.exe` is properly installed and accessible from your system PATH.
3. Make sure you have read and write permissions in both source and destination folders.
4. For specific errors, check the application log for more details.

If problems persist, please open an issue on the GitLab repository with a detailed description of the error and your system configuration.
