# this file doesn't require the OPENAI_API_KEY
# its purpose is to amalgamate the prompts and completions into a single JSONL file
# in the right format
# in the MARCUS case we reverse the sequence to completion : prompt
# this file differs significantly from what David Shapiro wrote
# and may not work correctly with his FinetuningTutorial any more
# what did he do to remove some of the rows from the plots.jsonl file?

import os
import json


completions_dir = '/Users/edsil/openai-store/WhatMightMarcusSay/completions/'
prompts_dir = '/Users/edsil/openai-store/WhatMightMarcusSay/prompts/'


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


if __name__ == '__main__':
    # apparently the sequence of files is arbitrary so we need to sort them
    # this sorts to start with Marcus_100_ ... but that doesn't matter for our purposes
    files_p = sorted(os.listdir(prompts_dir))
    print('\n\n',files_p[:10],'\n',len(files_p))
    files_c = sorted(os.listdir(completions_dir))
    print('\n\n',files_c[:10],'\n',len(files_c))
    data = list()
    for i in range(len(files_c)):
        completion = open_file(completions_dir + files_c[i])
        prompt = open_file(prompts_dir + files_p[i])
        # note the reversal of the order for WMMS
        info = {'prompt': prompt, 'completion': completion}
        # this appends the new json line to the plots file
        data.append(info)
    with open('/Users/edsil/openai-store/WhatMightMarcusSay/plots.jsonl', 'w') as outfile:
        for i in data:
            json.dump(i, outfile)
            outfile.write('\n')