# ----------------
# Standard library
# ----------------

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    """Entry point that launches streamlit run con NX_ENV=dev."""
    parser = argparse.ArgumentParser(description="NIXNOX Web Application")
    parser.add_argument(
        "--logger-level",
        default="info",
        help="Streamlit logger level (default: info)",
    )
    parser.add_argument(
        "streamlit_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to streamlit run",
    )
    args = parser.parse_args()
    # Configurar NX_ENV=dev
    # env = os.environ.copy()
    # env["NX_ENV"] = "dev"

    package_dir = Path(__file__).parent
    web_app_path = package_dir / "web_app.py"

    # streamlit run command
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(web_app_path),
        f"--logger.level={args.logger_level}",
    ]

    # streamlit extra arguments
    cmd.extend(args.streamlit_args)

    # Ejecutar
    # subprocess.check_call(cmd, env=env)
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
