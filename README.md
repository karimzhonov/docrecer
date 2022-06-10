# documet_recognizer

> Module for recognize documents
>
> Supports documents: Passport, patent, snils and migartion card
>
> Support countries: Tajikistan, Uzbekistan, Russia
>
User guide for single file:

```python
from docrecer import file_recognizer, Config
from docrecer.conf import OCRS

# Config for Yandex ocr
config = Config(ocr_name=OCRS.YANDEX,
                yandex_ocr_api_key='APi key')
# Config for PyTesseract
config = Config(ocr_name=OCRS.TESSERACT,
                tesseract_cmd=r'<path_to_tesseract.exe>')
# Start
_json = file_recognizer('<input_path_to_file> or np.array', config, 'outpath_to_save')

```

User guide for more files

```python
from docrecer import documents_recognizer, Config

# Set config
config = Config(input_path="<path_to_folder>",
                output_path="<path_to_folder_to_save>",
                ocr_name=...)
# start
documents_recognizer(config)
```