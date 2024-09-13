import json
import argparse
from utils import webhook_response, download_file
from models import Request, Job


def generate(request: dict):
    default_request = Request()
    job_id = request.get("job_id", None)
    prompt = request.get("prompt", "A beautiful city , full of amazing scenes.")
    webhook = request.get("webhook")
    if not webhook:
        return

    sampling_steps = int(request.get("sampling_steps", default_request.sampling_steps))
    cfg_scale = float(request.get("cfg_scale", default_request.cfg_scale))
    reference_url = request.get("reference_url", default_request.reference_url)
    reference_path = None
    resolution = request.get("resolution", default_request.resolution)
    aspect_ratio = request.get("aspect_ratio", default_request.aspect_ratio)
    length = request.get("length", default_request.length)

    if not job_id:
        webhook_response(webhook, False, 400, "Job Id is required")
        return
    if resolution not in ["144p", "240p", "360p", "480p", "720p"]:
        webhook_response(webhook, False, 400, "Resolution is invalid!")
        return
    if length not in ["2s", "4s", "8s", "16s"]:
        webhook_response(webhook, False, 400, "Length is Invalid!")
        return
    if reference_url and "http" not in reference_url:
        webhook_response(webhook, False, 400, "Reference must be a URL!")
        return

    if reference_url:
        reference_path = download_file(reference_url)
    request = Request(
        prompt=prompt,
        webhook=webhook,
        sampling_steps=sampling_steps,
        cfg_scale=cfg_scale,
        reference_url=reference_url,
        reference_path=reference_path,
        resolution=resolution,
        aspect_ratio=aspect_ratio,
        length=length,
    )

    job = Job(job_id=job_id, job_request=request)
    from open_sora_sample import run_base

    run_base(job)


def parse_args():
    parser = argparse.ArgumentParser(description="Request")
    parser.add_argument(
        "--request_dict", type=str, required=True, help="Request JSON string"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Convert the JSON string back to a dictionary
    request_dict = json.loads(args.request_dict)

    # Call the train function with the parsed dictionary
    generate(request_dict)

# request_dict = {
#     "job_id": "aljdfljsdfljskdf",
#     "prompt": "a close-up portrait of a woman set against a snowy backdrop. the woman is wearing a golden crown with a feathered design and a matching golden garment with a textured pattern. her makeup is dramatic, featuring dark red lipstick and smoky eyes. she has a neutral expression on her face and is looking directly at the camera. the background is blurred but appears to be a snowy landscape with trees and a clear sky. the lighting suggests it is daytime with natural light illuminating the scene. there are no visible texts or logos in the video. the style of the video is a fashion or portrait photograph with a focus on the woman's attire and makeup.",
#     "webhook": "https://webhook-test.com/1d708700d3cca1d504145ba553c9cf4d",
# }

# generate(request_dict)
