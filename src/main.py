from client_fva.ui.fvaclient import run
import sys
from pathlib import Path
from client_fva.user_settings import UserSettings

if __name__ == "__main__":
    settings = UserSettings.getInstance()
    if settings.installation_path is not None:
        settings.installation_path = str(Path(sys.argv[0]).parent)
    run()