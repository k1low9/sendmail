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


MODE = get_env("SENDMAIL_MODE", "TEST")
SENDER = get_env("SMTP_SENDER", required=True)
PASSWORD = get_env("SMTP_PASSWORD", required=True)
SUBJECT = get_env("SENDMAIL_SUBJECT", "2026年盛夏展示会のご案内-lilou+lily- -all hours-")
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
       "shimizu@orne.co.jp,shimura@orne.co.jp","f-tanino@twn.ne.jp","tanaka.eiko@in-natural.co.jp","info@orangeegg.com","t-craft@wanotakumi.jp","m.totani@adastria.co.jp","ki.ishii@adastria.co.jp","soyoko.ishihara@lusc.jp","maeda@ilex.co.jp","nakamura_kumi2@isetanmitsukoshi.co.jp","yoshino@aming.co.jp","hus@krone-kamakura.com","shop@surba-surbi.com","lipingzhang@vip.163.com","kukka@be-smart.jp","syoko.s@qscend.jp","info@hamilton-essence.co.jp","avenue4908la@yahoo.co.jp","kodomofuku@wacky.ne.jp","mokusha_sapporo@icloud.com","omorishouten237@gmail.com","tamura@neuron-inc.com","n-matsumoto@watashinoheya.co.jp","smz@welbeck.co.jp,yamaguchi@welbeck.co.jp","contact@cirkusneon.com","uozumi@sal.ne.jp","calend157@gmail.com","hasegawa.r@creema.co.jp","miki_nakama@hakka-group.co.jp","kumagai@debby.co.jp","lebell@bi.wakwak.com","ohtake@clearcamp.co.jp","qq5.au5@gmail.com","ivyaky@yahoo.com.hk","abby.ng@stations18.com.hk","jackey.ma@stations18.com.hk","sally.lam@stations18.com.hk","roppongirpg@yahoo.com.hk","tsaiyunyin@hotmail.com","y2kcollection@yahoo.com.hk","marketingtbc@hotmail.com","veronica.tbcjapan@gmail.com","mjjapan1@gmail.com","t31059833@gmail.com","nicolebut@yahoo.com.hk","tszwan621@gmail.com","greenstc2@yahoo.com.hk","chfashion2013@gmail.com","qtgaru@yahoo.com","ericastorehk@gmail.com","katehsien@gmail.com","andy@nissin-ns.co.jp","cadette@song.ocn.ne.jp","m.okeda.bishop@aranciato.com","earthware.tomo@gmail.com","rottan.mika@gmail.com","tarumi-zakka@books-futaba.co.jp","ikuko-kitano@jupiter.ocn.ne.jp","goodsprimo2008@gmail.com","rika.shimizu@hankyu-hanshin-dept.jp","muku_kajiya@ybb.ne.jp","kochi@wonder.ocn.ne.jp","expo@angers.jp","info@fastcut.jp","info@lapre.jp","sukima@sepia.plala.or.jp","honeyhoney1900@yahoo.co.jp","o_m_blue2314@yahoo.co.jp","slowf_door@yahoo.co.jp","chabbit@chabbit.name","tosu@bluebeat.co.jp","1em-rue@shop-ambience.com","douguchi1113@yahoo.co.jp","grasol.h@gmail.com","grasolclassic@gmail.com","yuka.ch1019.me@gmail.com","mas@ma28.co.jp","nishijima@ma28ya.co.jp","coup@juno.ocn.ne.jp","akao@becrews.co.jp","lesfilles@wit.ocn.ne.jp","pm.mgr.inuzuka@gmail.com","crayon@orange.ocn.ne.jp","shop@t-moonchild.com","03name866@gmail.com","culure@tamaoki.co.jp","kumi@matheruba.com","info@jagghouse.jp","mitsuonakayama1688@gmail.com","month2024.i.tile@gmail.com","a-sonoda@poplar.ocn.ne.jp","z.garage.815@gmail.com","spoonfulosaji@icloud.com","soleilmatsu@gmail.com","offaliving@yahoo.co.jp","info-shop@scol.jp","madoka.muroi@83milk.com","rire@rire.ocnk.net","n.yamamuta@icloud.com","desaki19@yahoo.co.jp","ttstylefukuoka@gmail.com","minoya.buyer@vesta.ocn.ne.jp","bingo.bhc131@gmail.com","kajiwara@la-coet.jp","yutingzhao35@gmail.com","nonaka@bisque.co.jp","t-kaizaki@tachibanaya-web.com"
    ]

    send_to = to_test_list if MODE == "TEST" else to_list

    body_text = """
拝啓
寒冷の候、貴社ますますご健勝のこととお喜び申し上げます。
平素よりLILOU+LILY ALL HOURSをご愛顧いただき、誠にありがとうございます。

このたび、 LILOU+LILY, ALL HOURS は、2026年 盛夏展示会 を開催いたします。
東京・大阪・福岡での開催となります。

新シーズンの最新アイテムをいち早くご紹介いたしますので、ぜひお気軽にお立ち寄りください。

製品納期に付きましては、5月～7月を予定しております。

==========================================================

【東京展示会のご案内】

■展示会名：LILOU+LILY, ALL HOURS 盛夏展示会
■会期：
2026年2月17日（火）12:00～18:00
2026年2月18日（水）10:00～18:00
2026年2月19日（木）10:00～16:00

■会場：EBISU ROOM
〒150-0022 渋谷区恵比寿南 1丁目12－1 瑩心会ビル 1F

==========================================================

【大阪展示会のご案内】

■展示会名：is am are(合同展示会内）
■会期：
2026年2月24日（火）10:00～18:00
2026年2月25日（水）10:00～18:00
2026年2月26日（木）10:00～16:00

■会場：綿業会館７F 本館、新館
〒541-0051 大阪府大阪市中央区備後町2-5-8

==========================================================

【福岡展示会のご案内】

■展示会名：LOCAL DISH(合同展示会内）
■会期：
2026年3月3日（火）10:00～18:00
2026年3月4日（水）10:00～17:00

■会場：THE KEGO CLUB
〒810-0001福岡市中央区天神2-2-20警固神社社務所ビル5F



==========================================================

※事前にアポイントをいただけますと、よりスムーズにご案内可能です。
※ご多忙のところ恐れ入りますが、
ご来場のお客様は2月9日までにご来場のご予定を
お知らせいただけますと幸いです。

皆さまにお会いできますことを、スタッフ一同心より楽しみにしております。
よろしくお願いいたします。



--
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
