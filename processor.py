import os
import re
import select
import subprocess
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from models import Job, JobStatus
import settings as settings


def job_processor(job: Job):
    toml_path = os.path.join(job.job_config.output_dir, "config.toml")
    command = f"bash -c 'cd {settings.BASE_DIR} && accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision fp16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 sdxl_train_network.py --config {toml_path}'"
    print(command)

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Use select to read from stdout and stderr without blocking
        logs_count = 0
        safetensors_files = set()
        while True:
            reads = [process.stdout.fileno(), process.stderr.fileno()]
            ret = select.select(reads, [], [])
            for fd in ret[0]:
                if fd == process.stdout.fileno():
                    read = process.stdout.readline()
                    if read:
                        output = read.strip()
                        print(output)
                        percentage = 0
                        if f"/{job.job_request.total_steps}" in output:
                            percentage_value = get_progress_percentage(output)
                            percentage = percentage_value if percentage_value else 0
                            logs_count += 1
                        job.job_progress = percentage
                if fd == process.stderr.fileno():
                    read = process.stderr.readline()
                    if read:
                        output = read.strip()
                        print(output)
                        percentage = 0
                        if f"/{job.job_request.total_steps}" in output:
                            percentage_value = get_progress_percentage(output)
                            percentage = percentage_value if percentage_value else 0
                            logs_count += 1
                        job.job_progress = percentage
            if process.poll() is not None:
                break

        return_code = process.poll()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)

        print("Job is Finished")

    except subprocess.CalledProcessError as e:
        print(e)
        job.job_status = JobStatus.FAILED.value
        job.error_message = str(e)

    except Exception as e:
        print(e)
        job.job_status = JobStatus.FAILED.value
        job.error_message = str(e)


def get_progress_percentage(output_line):
    # Regex pattern to find the diffusion process progress
    pattern = re.compile(r"(\d+)/(\d+)\s+\[")
    match = pattern.search(output_line)
    if match:
        current, total = map(int, match.groups())
        percentage = (current / total) * 100
        return percentage
    return None
