# hack-cb949bd8-aq
Hackathon team repository for AQ
ФАЙЛ ДЛЯ РЕПЕТИЦИИ НЕ ПУТАТЬ РЕПО

## Red-defect detector

The script considers a photo a defect when visibly red pixels cover at least 1%
of it. Place `ok.png` and `defect.png` beside the script, install the packages,
then run:

```bash
python -m pip install -r requirements.txt
python detect_defect.py
```

It prints one result for each image, for example:

```text
ok.png: OK (red area: 0.03%)
defect.png: DEFECT (red area: 4.21%)
```

To inspect a particular image or tune the red-area cutoff:

```bash
python detect_defect.py photo.png --threshold 0.02
```

`--threshold 0.02` means that 2% or more red pixels returns `DEFECT`.
