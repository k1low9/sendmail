import os
import glob
import time
import ssl
import smtplib
from pathlib import Path
from email.utils import formatdate, make_msgid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# =========================
# Gmailで展示会メール送信（画像フォルダ一元管理版）
#  - 画像フォルダは「IMG_DIR」で一元管理
#    優先順位:
#      1) 環境変数 IMG_DIR（例: /var/mail_assets/localdish_imgs）
#      2) この .py ファイルと同じ階層の img/ フォルダ（例: ./img）
#  - SMTP: smtp.gmail.com:587 (STARTTLS)
#  - 認証: Gmail「アプリパスワード」(16桁)
# =========================

MODE = "PROD"  # "TEST" or "PROD"

# ---- Gmail送信者（From）----
GMAIL_SENDER = os.getenv("GMAIL_SENDER", "localdishjp@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "bkikytioedxgeymp")

# ---- 返信先（Reply-To）----
REPLY_TO = os.getenv("REPLY_TO", "localdishjp@gmail.com")

SUBJECT = "合同展示会 『Local dish 2nd』開催のご案内　3/3(火)-　4(水)"

TO_TEST_LIST = [
    "nakamura@localmaison.com",
    "mail@localmaison.com",
]

TO_PROD_LIST = [
    "oba@arukurashi.com","month2024.i.tile@gmail.com","baybrookpanna@gmail.com","info@nighthawksfk.com","info@morpheeleather.com","tigre@tenkumaru.com","tigre@tenkumaru.com","neoclub@5570.jp","tanaka@larco.jp","last6child@gmail.com","info@navyharrys.com","chanco0875@gmail.com","info@morpheeleather.com","harrysthearmygym@gmail.com","scene.ninetynine@gmail.com","info@daisuekfurukawa.com","pm.mgr.inuzuka@gmail.com","miyazaki.725@docomo.ne.jp","yamamoto@atdc.com","fukuoka@blancoweb.com","info.choo@gmail.com","giraffe 63@vivid.ocn.ne.jp","kakiuchi_mika@iwatayamitsukoshi.co.jp","beans@noahdesign.jp","uchida_kokoro@iwatayamitsukoshi.co.jp","leathertramp2011@yahoo.co.jp","herencia.cad@gmail.com","4rimichi.akizuki@gmail.com","penneys_vintage@ybb.ne.jp","matsuoka_anna@iwatayamitsukoshi.co.jp","lotus@titan.ocn.ne.jp","herencia.kikunaga@minos.ocn.ne.jp","mi521 @watanabeya.co.jp","beans@net.email.ne.jp","info@karatsushirtkoubou.com","matsuya@hug2.jp","contact@circlestyle.com","info@robinaso.com","yuzumitu123@gmail.com","ren.shintani@gmail.com","info@redgoodspeed.com","masahiro.nishikawa0129@gmail.com","desaki19@yahoo.co.jp","info@dayzsales.com","rk 515@watanabeya.co.jp","doubleheart@lake.ocn.ne.jp","nagashimamasahiko@lautrec.co.jp","beans@noahdesign.jp","attic_shop@million.vc","retrick0401@gmail.com","yamamoto@srlinc.com","yshow@purple.plala.or.jp","chiharu.ueda@onthebooks.jp","fobstore@ifn.ne.jp","labasse@topaz.plala.or.jp","muffyame@gmail.com","takayama@sanzentokyo.com","soejima@provokedb.com","nakashima@provokedb.com","info@magicuco.com","pmkominkan@gmail.com","haruna@sanzentokyo.com","mahiro_horie@libwork.co.jp","takayuki_kitamoto@libwork.co.jp","yyuasa@tw.caitac.co.jp","wyoshimoto@tw.caitac.co.jp","okada@sekimiki.co.jp","onizaki@sekimiki.co.jp","ogawa@sekimiki.co.jp","stereo.mk3@gmail.com","stereo.mk3@gmail.com","info@ampersandand.co.n.ne.jp","seisan@tenkumaru.com","tenkumaru@tenkumaru.com","yahata@linkitall.jp","info@mamekurogouchi.com","kasikaya12@gmail.com","kikaku@tenkumaru.com","kikaku@tenkumaru.com","press@bluebeat.co.jp","hiromik@coconutworld.com","tenkumaru@tenkumaru.com","tide@johnbull.co.jp","tenkumaru@tenkumaru.com","gatsgrand721@yahoo.co.jp","tenkumaru@tenkumaru.com","ral@coconutworld.com","bingo.bhc131@gmail.com","oba@arukurashi.com","paulinebleu0215@gmail.com","nakayama@hightide.co.jp","info@magicu.jp","info@hangarm.com","yano@fashionballoon.co.jp","tibetan@luck.ocn.ne.jp","famille@wing.ocn.ne.jp","suehiro@goshjp.com","francis7014@icloud.com","aulico@blue.plala.or.jp","kiharu@quantizedressline.com","saudadefn@icloud.com","mail@localmaison.com"
]

BODY_TEXT = """\
バイヤーご担当者様

このメールは前回の合同展示会でお名刺を頂戴いたしましたお客様へ送信しております。

合同展示会Local dish 運営事務局と申します。

このたび、2026年3月3日(火)〜4日(水)の2日間、合同展示会 『Local dish 2nd』を開催いたします。

今回は規模を拡大し、アパレル（メンズ・レディース）・アクセサリー・靴・バッグ・帽子・靴下・など国内外の約70ブランド以上が出展します。

既存のお取引先様に加え、新たな出会いを求めて、出展者一同、皆様のご来場を心よりお持ちしております。

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

合同展示会　Local dish　2nd

日時：2026年

3月3日（火）10：00〜18：00
3月4日（水）10：00〜17：00


場所：THE KEGO CLUB 5F

 福岡県福岡市中央区天神2-2-20　警固神社社務所ビル5階
(1階にブルーボトルコーヒーがあるビルです）
https://maps.app.goo.gl/Spqa8sTtPTM7QsZo7

出展企業：

アウターリミッツ（株）
(株）H.UNIT
(有)エマート
オイコス（株）
CATTA
(株）GEMEX
(株）コネクト
(株）SAS
GGG
(株）シーノート
(株）SIM
(株）スタンレーインターナショナル
(株)スプリング
(有)スペシャル
(株)スリーエイチワークス/TROIS AVRIL
SOAR clothing
Dayz
dish
(株)天空丸
(株)ナカハラ
(株)ハーベストムーン
(株)バスコ
(有)ビッグピンク
ヒコサカ（株）
(有)HERENCIA
(株)マウンテンディア—
(株)ミノオ・ラボ
(有)ライディングハイ
(株)リガメント
(株)Ray
Re:creations
(株)ローカルメゾン


ご来場について：

・基本的に招待状などはご用意しておりません。

※受付にて名刺２枚お渡しください。

※駐車場はございませんのでお近くのコインパーキングをご利用ください。

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
問い合わせは下記にお願いします。

Local dish 運営事務局

Mail：localdishjp@gmail.com
"""


# =========================
# 画像フォルダ一元管理：ここだけ触ればOK
# =========================
SCRIPT_DIR = Path(__file__).resolve().parent

# 1) 環境変数 IMG_DIR があればそれを使う（推奨）
# 2) なければこの .py と同階層の ./img を使う
IMG_DIR = Path(os.getenv("IMG_DIR", str(SCRIPT_DIR / "localdish_imgs"))).expanduser().resolve()

# 添付対象拡張子
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".bmp", ".tif", ".tiff"}


def normalize_recipients(recipients):
    """'a@x.com,b@y.com' のような要素が混じっても安全に分解してフラット化（重複除去）"""
    out = []
    for r in recipients:
        for one in str(r).split(","):
            one = one.strip()
            if one:
                out.append(one)

    seen = set()
    uniq = []
    for x in out:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(x)
    return uniq


def list_attachment_files(img_dir: Path) -> list[Path]:
    """
    img_dir 配下の添付ファイル（画像等）を列挙して Path の配列で返す。
    - カレントディレクトリ（cwd）に依存しない
    - フォルダを変更しない
    """
    if not img_dir.exists():
        raise FileNotFoundError(f"画像フォルダが見つかりません: {img_dir}")

    files = sorted([p for p in img_dir.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXTS])

    print(f"画像フォルダ: {img_dir}")
    print("添付ファイル一覧:")
    for p in files:
        print(" -", p.name)

    return files


def attach_files(msg: MIMEMultipart, file_paths: list[Path]) -> None:
    """
    ★重要：メールごとに添付パーツを新規生成（使い回し禁止）
    """
    for path in file_paths:
        with open(path, "rb") as f:
            part = MIMEApplication(f.read())
        part.add_header("Content-Disposition", "attachment", filename=path.name)
        msg.attach(part)


def build_message(to_addr: str, attachment_paths: list[Path]) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = GMAIL_SENDER
    msg["To"] = to_addr
    msg["Reply-To"] = REPLY_TO
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=GMAIL_SENDER.split("@")[-1])

    msg.attach(MIMEText(BODY_TEXT, "plain", "utf-8"))

    # 添付（毎回新規作成）
    attach_files(msg, attachment_paths)
    return msg


def send_exhibition_mail():
    send_to = TO_TEST_LIST if MODE == "TEST" else TO_PROD_LIST
    send_to = normalize_recipients(send_to)

    if not send_to:
        raise ValueError("宛先が空です。TO_PROD_LIST / TO_TEST_LIST を確認してください。")

    if not GMAIL_SENDER or "@gmail.com" not in GMAIL_SENDER.lower():
        print("注意: GMAIL_SENDER が Gmail でない可能性があります:", GMAIL_SENDER)

    if not GMAIL_APP_PASSWORD or len(GMAIL_APP_PASSWORD.replace(" ", "")) < 10:
        print("注意: GMAIL_APP_PASSWORD が未設定/不正っぽいです（アプリパスワード必須）")

    # 画像フォルダはここで一元的に参照（cwdに依存しない）
    attachment_paths = list_attachment_files(IMG_DIR)

    host, port = "smtp.gmail.com", 587
    context = ssl.create_default_context()

    with smtplib.SMTP(host, port, timeout=60) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        smtp.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)

        total = len(send_to)
        for i, to_addr in enumerate(send_to, start=1):
            print(f"{i}/{total} 送信中: {to_addr}")

            msg = build_message(to_addr, attachment_paths)

            try:
                smtp.send_message(msg)
                print(f"送信完了: {to_addr}")
            except Exception as e:
                print(f"送信失敗: {to_addr} / エラー: {e}")

            if i < total:
                time.sleep(5)

    print("=== 全メール送信完了 ===")
    print(f"MODE: {MODE}")
    print(f"IMG_DIR: {IMG_DIR}")


if __name__ == "__main__":
    send_exhibition_mail()
