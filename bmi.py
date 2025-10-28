"""簡單的 BMI 計算器

用法:
  - 互動式：直接執行 `python bmi.py`，會要求輸入體重(kg)與身高(cm 或 m)
  - 命令列：`python bmi.py --weight 70 --height 170`

假設與行為：
  - 若輸入的身高數值大於 3，會視為公分(cm)並自動轉為公尺；否則視為公尺(m)。
  - 體重單位為公斤(kg)。
"""

import argparse
import sys


def calculate_bmi(weight_kg: float, height_m: float) -> float:
	"""計算 BMI 並回傳浮點數（不做四捨五入）。

	weight_kg: 體重（公斤）
	height_m: 身高（公尺）
	"""
	if height_m <= 0:
		raise ValueError("height must be > 0")
	return weight_kg / (height_m ** 2)


def bmi_category(bmi: float) -> str:
	"""依 WHO 標準回傳分類（中文）"""
	if bmi < 18.5:
		return "體重過輕"
	if bmi < 25:
		return "體重正常"
	if bmi < 30:
		return "過重"
	return "肥胖"


def parse_args(argv=None):
	p = argparse.ArgumentParser(description="計算 BMI 的小工具")
	p.add_argument("--weight", "-w", type=float, help="體重，公斤 (kg)")
	p.add_argument("--height", "-t", type=float, help="身高，數字（可為公分或公尺）: 若>3則視為公分")
	return p.parse_args(argv)


def _to_meters(height_value: float) -> float:
	"""若高度 > 3 則當作公分(cm)並轉為公尺，否則當作公尺回傳。"""
	if height_value > 3:
		return height_value / 100.0
	return height_value


def interactive_input():
	try:
		w_raw = input("請輸入體重 (公斤): ").strip()
		h_raw = input("請輸入身高 (公分或公尺，例如 170 或 1.70): ").strip()

		weight = float(w_raw)
		height = float(h_raw)
	except ValueError:
		print("輸入錯誤：請輸入數字（例如體重 70，身高 170 或 1.70）")
		return 2

	if weight <= 0 or height <= 0:
		print("輸入錯誤：體重與身高必須為正值")
		return 3

	height_m = _to_meters(height)
	bmi = calculate_bmi(weight, height_m)
	print(f"BMI: {bmi:.1f}")
	print(f"分類: {bmi_category(bmi)}")
	return 0


def main(argv=None):
	args = parse_args(argv)

	if args.weight is None or args.height is None:
		# 進入互動式模式
		return interactive_input()

	# 命令列模式
	try:
		weight = float(args.weight)
		height = float(args.height)
	except ValueError:
		print("命令列參數錯誤：weight 與 height 必須為數字")
		return 2

	if weight <= 0 or height <= 0:
		print("錯誤：體重與身高必須為正值")
		return 3

	height_m = _to_meters(height)
	bmi = calculate_bmi(weight, height_m)
	print(f"BMI: {bmi:.1f}")
	print(f"分類: {bmi_category(bmi)}")
	return 0


if __name__ == "__main__":
	exit_code = main()
	sys.exit(exit_code)
