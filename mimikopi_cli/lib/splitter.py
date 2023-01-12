import glob
import os
import shutil
import sys

from dotenv import load_dotenv
from spleeter.audio import Codec  # NOQA
from spleeter.separator import Separator  # NOQA

from mimikopi_cli.utils.id import generate_time_id
from mimikopi_cli.utils.logger import logger

# TODO: tensorflowのwarningを消す
# import warnings
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# warnings.filterwarnings("ignore")

# .envファイル読み込見込み
load_dotenv()


MODE_LIST = [
    2,  # ボーカル, その他
    4,  # ボーカル, ベース, ドラム, その他
    5,  # ボーカル, ベース, キーボード, その他
]


# tmpフォルダ作成
def create_tmp_dir(target_path: str, tmp_path: str) -> None:
    try:
        music_file_paths = glob.glob(target_path)
        if len(music_file_paths) == 0:
            logger.info("入力フォルダが空です。")
            logger.info(f"入力先: {target_path}")
            sys.exit()

        # ファイルを.wavに変換してtmpフォルダに追加
        for file_path in music_file_paths:
            logger.info(f"[LOAD]: {file_path}")
            file_name, _ = os.path.splitext(os.path.basename(file_path))
            time_id = generate_time_id()
            out_file_path = f"{tmp_path}/{file_name}_{time_id}.wav"
            os.makedirs(tmp_path, exist_ok=True)
            shutil.copyfile(file_path, out_file_path)
    except OSError as error:
        logger.info("ファイルの読み込みに失敗しました。")
        raise error
    except Exception:
        logger.info("予期せぬエラーが発生しました。")
        sys.exit()


# outputフォルダ作成
def create_output_dir(output_path: str) -> None:
    try:
        os.makedirs(output_path, exist_ok=True)
    except OSError as error:
        logger.info("出力ファイルの作成に失敗しました。")
        raise error
    except Exception:
        logger.info("予期せぬエラーが発生しました。")
        sys.exit()


# tmpフォルダを削除する
def delete_tmp_dir(assets_path: str) -> None:
    try:
        shutil.rmtree(f"{assets_path}/tmp/")
    except FileNotFoundError:
        logger.info("tmpフォルダが見つかりませんでした。")


class Splitter:
    def sp(self, mode: int) -> None:
        """
        音声をパートごとに分割する関数

        Parameters
        ----------
        mode : int
            分割数のオプション
        """

        if not (mode in MODE_LIST):
            logger.error("無効なオプションです。mode=(2 | 4 | 5)")
            sys.exit()

        logger.info(f"mode: {mode}")

        assets_path = os.getenv("ASSETS_PATH")
        if assets_path is None:
            logger.error("環境変数を設定してください。(ASSETS_PATH)")
            sys.exit()

        tmp_path = f"{assets_path}/tmp"
        output_path = f"{assets_path}/out"
        target_path = f"{assets_path}/music/*"

        # ファイルの読み込み
        try:
            create_tmp_dir(target_path, tmp_path)
            create_output_dir(output_path)
        except OSError as error:
            logger.info("Error: ", error)
            sys.exit()
        except Exception as error:
            logger.error("Error: ", error)
            sys.exit()

        # パートごとに音声を分割
        try:
            separator = Separator(f"spleeter:{mode}stems")
            tmp_music_file_paths = glob.glob(tmp_path + "/*")

            for file_path in tmp_music_file_paths:
                file_basename = os.path.basename(file_path)
                logger.info("")
                logger.info(f"[{file_basename}]")

                separator.separate_to_file(f"{tmp_path}/{file_basename}", output_path, codec=Codec.MP3)
        except Exception as error:
            logger.info("Error: ", error)
        finally:
            logger.info("")
            logger.info(f"出力先: {output_path}")
            delete_tmp_dir(assets_path)
            sys.exit()
