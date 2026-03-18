import os
import time
from pathlib import Path
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from env_utils import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DOTENV_PATH = load_dotenv(BASE_DIR / ".env")


def get_env(name: str, default: str = "", required: bool = False) -> str:
    value = os.getenv(name, default).strip()
    if required and not value:
        raise ValueError(f"環境変数 {name} が未設定です。.env を確認してください: {DOTENV_PATH}")
    return value


MODE = "TEST"
SENDER = get_env("SMTP_SENDER", required=True)
PASSWORD = get_env("SMTP_PASSWORD", required=True)
SUBJECT = "2026年盛夏展示会のご案内-lilou+lily- -all hours-"
SMTP_HOST = get_env("SMTP_HOST", "www2368.sakura.ne.jp")
SMTP_PORT = int(get_env("SMTP_PORT", "587"))
ATTACHMENT_DIR = Path(get_env("SENDMAIL_IMG_DIR", str(BASE_DIR / "imgs"))).expanduser().resolve()


def sendMail():
    print(f"=== 現在の送信モード: {MODE} ===")

    to_test_list = [
        "nakamura@localmaison.com",
        "hara@localmaison.com"
    ]

    to_list = [
    ]

    send_to = to_test_list if MODE == "TEST" else to_list

    body_text = """
お取引先様各位

このたび LILOU+LILY秋冬展示会、ならびに
ALL HOURS晩夏初秋展示会 を開催いたします。

福岡・東京・大阪の3会場にて開催予定となっております。
新シーズンの最新アイテムをいち早くご覧いただけますので、
ぜひお気軽にお立ち寄りください。

なお、製品納期につきましては
LILOU+LILY：9月～
ALL HOURS：7月～
を予定しております。

LILOU+LILY秋冬展示会 / ALL HOURS晩夏初秋展示会

==========================================================
【福岡展示会のご案内】

■会期
2026年4月7日（火）10:00～18:00
2026年4月8日（水）10:00～18:00

■会場
LOCALMAISON SHOWROOM

〒810-0041
福岡市中央区大名2-11-19-5F



==========================================================

【東京展示会のご案内】

■会期
2026年4月14日（火）10:00～18:00
2026年4月15日（水）10:00～18:00
2026年4月16日（木）10:00～16:00

■会場
DAIKANYAMA GARAGE

〒153-0061
東京都目黒区中目黒1-3-12
アーバンリゾート代官山2F

==========================================================

【大阪展示会のご案内】

■会期
2026年4月21日（火）10:00～18:00
2026年4月22日（水）10:00～18:00

■会場
〒541-0059
大阪市中央区博労町4-6-10ハニービル2階 C会場

==========================================================

※完全アポイント制となっております。ご連絡お待ちしております。
******************************************
株式会社ローカルメゾン
中嶋・原
〒810-0041
福岡市中央区大名2-11-19-5F
TEL:092-260-7277
FAX:092-260-7266
MOBILE
080-4332-0707(中嶋）
090-9070-7076(原）
mail@localmaison.com(中嶋）
hara@localmaison.com(原）
******************************************
    """

    print("Current dir:", os.getcwd())
    files = sorted(ATTACHMENT_DIR.glob("*"))
    print("添付ファイル一覧:", [str(path) for path in files])

    attach_parts = []
    for file_path in files:
        if not file_path.is_file():
            continue
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read())
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=file_path.name
            )
            attach_parts.append(part)

    for index, to in enumerate(send_to, start=1):
        print(f"{index}/{len(send_to)} 件目送信中: {to}")

        msg = MIMEMultipart()
        msg["Subject"] = SUBJECT
        msg["From"] = SENDER
        msg["To"] = to

        msg.attach(MIMEText(body_text, "plain"))

        for part in attach_parts:
            msg.attach(part)

        try:
            with SMTP(SMTP_HOST, SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(SENDER, PASSWORD)
                smtp.send_message(msg)
            print(f"送信完了: {to}")
        except Exception as e:
            print(f"送信失敗: {to} / エラー: {e}")

        if index < len(send_to):
            print("待機中（5秒）...")
            time.sleep(5)

    print("=== 全メール送信完了 ===")
    print(f"送信モード: {MODE}")


if __name__ == "__main__":
    sendMail()
