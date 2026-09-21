"""샘플 PDF 재생성: reportlab 필요. --font에 한글 TTF 경로 지정."""
from pathlib import Path
import argparse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parent

def build(font):
    pdfmetrics.registerFont(TTFont("Korean", str(font)))
    dest = ROOT / "output/pdf/대한민국_태극기와_애국가.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(dest), pagesize=A4, invariant=1)
    c.setTitle("대한민국 태극기와 애국가 | PKOS 변환 샘플")
    c.setAuthor("PKOS")
    w,h=A4
    def text(x,y,t,size=12,color="#172B4D"):
        c.setFillColor(HexColor(color));c.setFont("Korean",size);c.drawString(x,y,t)
    text(48,790,"PKOS  /  PDF 변환 샘플",10,"#56708F")
    text(48,751,"대한민국의 태극기와 애국가",25)
    text(48,724,"한글 텍스트와 그림이 함께 있는 문서로 변환을 연습해 보세요.",11)
    c.drawImage(str(ROOT / "samples/taegeukgi.png"),148,480,width=300,height=200)
    text(48,438,"01   태극기",17)
    text(48,410,"대한민국의 국기는 태극기입니다.")
    text(48,386,"흰 바탕에 태극 문양과 건·곤·감·리 네 괘가 배치되어 있습니다.")
    text(48,322,"변환 결과에서 확인할 것",16)
    for i,t in enumerate(["제목과 한글 문장이 깨지지 않고 읽히는지 확인합니다.","다음 쪽의 애국가 1~4절과 후렴이 모두 포함되는지 확인합니다.","현재 2부 PDF 변환은 글자만 추출하며, 태극기 그림은 추출하지 않습니다.","이 샘플은 글자가 들어 있는 PDF입니다. 스캔 PDF의 OCR 시험용은 아닙니다."]):
        text(48,292-i*26,t,10)
    text(48,101,"태극기 이미지 출처: 행정안전부 국가상징 - 국기(태극기)",9)
    text(48,83,"https://www.mois.go.kr/frt/sub/a06/b08/nationalIcon_2/screen.do",8)
    text(48,48,"PKOS · 공개 연습 자료",9);text(525,48,"1 / 2",9)
    c.showPage()
    text(48,790,"PKOS  /  PDF 변환 샘플",10,"#56708F")
    text(48,747,"02   애국가",25)
    verses=[("1절", "동해물과 백두산이 마르고 닳도록", "하느님이 보우하사 우리나라 만세"),
            ("2절", "남산 위에 저 소나무 철갑을 두른 듯", "바람서리 불변함은 우리 기상일세"),
            ("3절", "가을 하늘 공활한데 높고 구름 없이", "밝은 달은 우리 가슴 일편단심일세"),
            ("4절", "이 기상과 이 맘으로 충성을 다하여", "괴로우나 즐거우나 나라 사랑하세")]
    for i,(label,a,b) in enumerate(verses):
        y=694-i*113
        text(48,y,label,12,"#23599B");text(48,y-27,a,15);text(48,y-53,b,15)
    text(48,231,"후렴 · 각 절 뒤에 반복",12,"#23599B")
    text(48,202,"무궁화 삼천리 화려강산",15)
    text(48,175,"대한 사람 대한으로 길이 보전하세",15)
    text(48,110,"가사 확인 출처: 행정안전부 국가상징 - 국가(애국가)",9)
    text(48,92,"https://www.mois.go.kr/frt/sub/a06/b08/nationalIcon_3/screen.do",8)
    text(48,73,"오래된 애국가 가사만 수록했습니다. 음원과 악보는 포함하지 않습니다.",9)
    text(48,48,"PKOS · 공개 연습 자료",9);text(525,48,"2 / 2",9)
    c.save()
    return dest

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--font", default="C:/Windows/Fonts/malgun.ttf")
    print(build(parser.parse_args().font))
