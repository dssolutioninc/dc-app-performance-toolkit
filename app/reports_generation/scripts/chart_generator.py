import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
# Configure matplotlib for headless/Docker environments to prevent hangs
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['figure.max_open_warning'] = 50
matplotlib.rcParams['interactive'] = False
matplotlib.rcParams['backend'] = 'Agg'

import pandas as pd
from pandas import DataFrame

from scripts.utils import validate_file_exists, validate_str_is_not_blank, validate_is_number, get_app_specific_actions

def __normalize_file_name(s) -> str:
    s = s.lower()
    # Remove all non-word characters (everything except numbers, letters and '-')
    s = re.sub(r"[^\w\s-]", '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)

    return s


def __resolve_and_expand_user_path(path: Path) -> Path:
    return path.resolve().expanduser()


def __read_file_as_data_frame(file_path: Path, index_col: str) -> DataFrame:
    if not file_path.exists():
        raise SystemExit(f"File {file_path} does not exist")
    return pd.read_csv(file_path, index_col=index_col)


def __generate_image_name(title: str) -> Path:
    return Path(f"{__normalize_file_name(title)}.png")


def validate_config(config: dict):
    validate_str_is_not_blank(config, "aggregated_csv_path")
    validate_str_is_not_blank(config, "index_col")
    validate_str_is_not_blank(config, "title")
    validate_is_number(config, "image_height_px")
    validate_is_number(config, "image_width_px")


def make_chart(config: dict, results_dir: Path, scenario_status: str) -> Path:
    csv_path_str = config["aggregated_csv_path"]
    index_col = config["index_col"]
    title = config["title"] + f" | Scenario status: {scenario_status}"
    image_height_px = config["image_height_px"]
    image_width_px = config["image_width_px"]

    image_height = image_height_px / 100
    image_width = image_width_px / 100

    file_path = __resolve_and_expand_user_path(Path(csv_path_str))
    data_frame = __read_file_as_data_frame(file_path, index_col)
    print(f"Input data file {file_path} successfully read")

    # Set app-specific mark
    print("Getting app-specific actions...")
    app_specific_actions_list = get_app_specific_actions(file_path)
    print(f"Found {len(app_specific_actions_list)} app-specific actions")
    for action in app_specific_actions_list:
        data_frame = data_frame.rename(index={action: f"\u2714{action}"})
    print("App-specific actions applied")

    print("Sorting dataframe...")
    data_frame = data_frame.sort_index()
    print(f"Dataframe sorted with {len(data_frame)} rows and {len(data_frame.columns)} columns")
    
    print("Creating barh plot...")
    import matplotlib.backends.backend_agg as agg_backend
    from matplotlib.figure import Figure
    
    fig = Figure(figsize=(image_width, image_height))
    print("Figure created")
    ax = fig.add_subplot(111)
    print("Axes created")
    
    print("Plotting data...")
    y_pos = range(len(data_frame))
    num_cols = len(data_frame.columns)
    bar_height = 0.8 / num_cols if num_cols > 0 else 0.8
    
    for i, col in enumerate(data_frame.columns):
        offset = (i - num_cols/2 + 0.5) * bar_height
        ax.barh([p + offset for p in y_pos], data_frame[col], height=bar_height, label=col)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(data_frame.index)
    if num_cols > 1:
        ax.legend()
    print("barh plot created")
    
    print("Setting xlabel and title...")
    ax.set_xlabel('Time, ms')
    ax.set_title(title)
    print("Calling tight_layout...")
    fig.tight_layout()
    print("tight_layout completed")

    image_path = results_dir / __generate_image_name(Path(csv_path_str).stem)
    print(f"About to save figure to {image_path}...")
    canvas = agg_backend.FigureCanvasAgg(fig)
    print("Canvas created")
    canvas.print_png(str(image_path))
    print("savefig completed, closing plot...")
    fig.clear()
    print("plot cleared")
    validate_file_exists(image_path, f"Result file {image_path} is not created")
    print(f"Chart file: {image_path.absolute()} successfully created")

    return image_path


def perform_chart_creation(config: dict, results_dir: Path, scenario_status: str) -> Path:
    validate_config(config)
    output_file_path = make_chart(config, results_dir, scenario_status)
    return output_file_path