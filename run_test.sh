#!/bin/bash

# editable
configFile="${PWD}/config/test_config.json"
audioDir="${PWD}/test/audio"
outputDir="${PWD}/test/speechServiceOutput"


# not editable
source env/bin/activate
python3 src/main.py \
	--config ${configFile} \
	--audio_dir ${audioDir} \
	--output_dir ${outputDir}
deactivate
