import sys
import string
import slither
import json
from slither.detectors import all_detectors
import os

slith = slither.Slither(sys.argv[1], compile_force_framework=sys.argv[2])
filename = sys.argv[3]

for detector in dir(all_detectors):
    if detector[0] in string.ascii_uppercase:
        slith.register_detector(getattr(all_detectors, detector))

detector_results = sum(slith.run_detectors(), [])

detectors = []
for detector in detector_results:
    elems = []
    for element in detector["elements"]:
        relpath = os.path.relpath(element['source_mapping']['filename_absolute'], sys.argv[1])
        if relpath == filename:
            elems.append({
                "name": element["name"],
                "source_mapping": {
                    "relative_file": element["source_mapping"]["filename_short"],
                    "line": element["source_mapping"]["lines"][0],
                    "starting_column": element["source_mapping"]['starting_column'],
                    "length": element["source_mapping"]['length']
                },
            })
    if not elems:
        continue
    detectors.append(
        {
            "check": detector["check"],
            "overall_description": detector["description"],
            "impact": detector["impact"],
            "confidence": detector["confidence"],
            "first_markdown_source": detector["first_markdown_element"],
            "elements": elems
        }
    )

json.dump(detectors, sys.stdout)

