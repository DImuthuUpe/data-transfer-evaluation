import os
import sys

sys.path.append("./")
sys.path.append("../evalit/")
sys.path.append("./evalit/")

import evalit

print(evalit.__version__)

from loguru import logger

from evalit.api import MFTAutomation, NifiAutomation, RcloneAutomation
from evalit.controller import StandardAutomationController

nifi_installation = os.getenv("NIFI_INSTALLATION")
mft_installation = os.getenv("MFT_INSTALLATION")

dt_config = os.getenv("CFG_YAML", "tests/config.yaml")

# value is a tuple, first item is size in GB
filemap = {"testfile": (1,)}
filenames = tuple(filemap.keys())

###### Nifi ###########
controller = (
    StandardAutomationController()
    .add_automation(
        RcloneAutomation(
            dt_config,
            filenames,
            debug=True,
            buffer_size=512,
            multi_thread_streams=10,
            multi_thread_cutoff=50,
            ntransfers=8,
            s3_max_upload_parts=10,
            s3_upload_concurrency=10,
        )
    )
    .add_automation(
        NifiAutomation(
            config=dt_config,
            nifi_url="https://localhost:8443/nifi-api",
            nifi_dir=nifi_installation,
            files=filenames,
        )
    )
    .add_automation(
        MFTAutomation(
            config=dt_config,
            mft_dir=mft_installation,
            files=filenames,
        )
    )
)
print(controller)
controller.run(filemap=filemap)
