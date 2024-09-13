import os
import time
import settings as settings
from videosys import OpenSoraConfig, VideoSysEngine
from utils import upload_to_s3, webhook_response
from models import Job, Response, JobStatus


def run_base(job: Job):
    # change num_gpus for multi-gpu inference
    # sampling parameters are defined in the config
    job.job_status = JobStatus.PROCESSING.value
    job.job_progress = 0
    webhook_response(job.job_request.webhook, True, 200, "Job Started!", job.dict())
    start_time = time.time()
    config = OpenSoraConfig(
        num_sampling_steps=job.job_request.sampling_steps,
        cfg_scale=job.job_request.cfg_scale,
        num_gpus=1,
    )
    engine = VideoSysEngine(config)

    # prompt = "a close-up portrait of a woman set against a snowy backdrop. the woman is wearing a golden crown with a feathered design and a matching golden garment with a textured pattern. her makeup is dramatic, featuring dark red lipstick and smoky eyes. she has a neutral expression on her face and is looking directly at the camera. the background is blurred but appears to be a snowy landscape with trees and a clear sky. the lighting suggests it is daytime with natural light illuminating the scene. there are no visible texts or logos in the video. the style of the video is a fashion or portrait photograph with a focus on the woman's attire and makeup."
    # prompt = 'A breathtaking sunrise scene.{"reference_path": "/var/www/Open-Sora/assets/images/condition/wave.png","mask_strategy": "0"}'
    if job.job_request.reference_path:
        job.job_request.prompt += f"""{{"reference_path": {job.job_request.reference_path},"mask_strategy": "0"}}"""
    # num frames: 2s, 4s, 8s, 16s
    # resolution: 144p, 240p, 360p, 480p, 720p
    # aspect ratio: 9:16, 16:9, 3:4, 4:3, 1:1
    video = engine.generate(
        prompt=job.job_request.prompt,
        resolution=job.job_request.resolution,
        aspect_ratio=job.job_request.aspect_ratio,
        num_frames=job.job_request.length,
    ).video[0]
    output_path = os.path.join(settings.BASE_DIR, "outputs", f"{job.job_id}.mp4")
    engine.save_video(video, output_path)
    url = upload_to_s3(output_path)
    end_time = time.time()
    total_time = end_time - start_time
    response = Response(
        total_time=total_time,
        time_per_step=total_time / job.job_request.sampling_steps,
        s3_url=url,
    )
    job.job_status = JobStatus.FINISHED.value
    job.job_progress = 100
    job.job_result = response

    webhook_response(
        job.job_request.webhook,
        True,
        200,
        "Video Generated Successfully!",
        job.dict(),
    )


# def run_pab():
#     config = OpenSoraConfig(enable_pab=True)
#     engine = VideoSysEngine(config)

#     prompt = "Pirates sailing the sea."
#     video = engine.generate(prompt).video[0]
#     engine.save_video(video, f"./outputs/{prompt}.mp4")
