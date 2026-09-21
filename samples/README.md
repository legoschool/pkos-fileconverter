# 공개 PDF 샘플

`output/pdf/대한민국_태극기와_애국가.pdf`는 PKOS 변환 연습용 2쪽 문서입니다.

- 태극기 이미지: [행정안전부 국기 안내](https://www.mois.go.kr/frt/sub/a06/b08/nationalIcon_2/screen.do)의 태극기 파일 ZIP에서 국기 JPG를 추출하고 1200×800 PNG로 축소했습니다. 제작 방법 설명 그림이 아닌 국기 그림입니다.
- 가사 확인: [행정안전부 애국가 안내](https://www.mois.go.kr/frt/sub/a06/b08/nationalIcon_3/screen.do). 오래된 애국가 가사 1~4절과 후렴을 수록했습니다. 음원·악보는 포함하지 않았습니다.
- 국기와 오래된 애국가 가사는 공개 영역 자료입니다. 이 저장소의 MIT 표시는 제3자 음원 등의 사용 허가를 뜻하지 않습니다.
- PDF는 선택 가능한 한글 텍스트를 포함합니다. 2부 변환기는 텍스트를 추출하며 그림 추출·OCR은 하지 않습니다.

재생성에는 reportlab과 한글 TTF가 필요합니다. Windows 기본값은 맑은 고딕입니다.

```sh
python build_sample.py --font "C:/Windows/Fonts/malgun.ttf"
python build_notebook.py
```

노트북에는 PDF 바이트가 내장되므로 샘플 실행 시 GitHub 파일을 추가 다운로드하지 않습니다. 임시 폴더에 샘플 PDF와 변환 결과를 저장하며 개인 드라이브의 원본 파일을 수정하지 않습니다.
