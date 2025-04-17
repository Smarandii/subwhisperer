import os, argparse
from engine import process_video


def _parse():
    p = argparse.ArgumentParser("subwhisperer")
    p.add_argument("video")
    p.add_argument("-o", "--out", default="out", help="output directory")
    return p.parse_args()


def _run(device: str):
    os.environ["CUDA_VISIBLE_DEVICES"] = "" if device == "cpu" else os.getenv("CUDA_VISIBLE_DEVICES", "0")
    args = _parse()
    process_video(args.video, output_directory_full_path=args.out, device=device)


def main():       _run(device=os.getenv("SUBWHISPERER_DEVICE", "auto"))


def main_cpu():   _run(device="cpu")


def main_cuda():  _run(device="cuda")
