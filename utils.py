import os
import re
import subprocess
import shutil
import tiktoken

CODE_ROOT = '/tmp/st/'

def run_code(function_name):
    py_file = os.path.join(CODE_ROOT, f'{function_name}.py')
    process = subprocess.Popen(['python', py_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    ret = process.returncode
    return output.decode(), err.decode(), ret

def write_to_disk(code, function_name):
    os.makedirs(CODE_ROOT, exist_ok=True)
    with open(os.path.join(CODE_ROOT, f'{function_name}.py'), 'w') as f:
        f.write(code)
    shutil.copyfile('./simplify.py', os.path.join(CODE_ROOT, 'simplify.py'))

def redact_test_output(text):
    # Define the regex pattern
    pattern = r"(Ran) (\d+) (tests in) (\d+\.\d+)(s)"
    # Replace the matched text with the specified format
    redacted_text = re.sub(pattern, r"\1 \2 \3 <redacted>", text)
    return redacted_text

def count_tokens(text: str) -> int:
    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = list(enc.encode(text))
    return len(tokens)

def split_text_into_chunks(html, max_tokens=2000):
    lines = html.split('\n')
    chunks = []
    cur_chunk = ""
    for line in lines:
        if count_tokens(cur_chunk + line) > max_tokens:
            chunks.append(cur_chunk)
            cur_chunk = line
        else:
            cur_chunk += "\n" + line
    chunks.append(cur_chunk)
    return chunks
