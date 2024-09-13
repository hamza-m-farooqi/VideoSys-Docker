from enum import Enum
from pydantic import BaseModel, conint


class JobStatus(Enum):
    WAITING = "waiting"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"


class Request(BaseModel):
    prompt: str = ""
    webhook: str = ""
    sampling_steps: int = 30
    cfg_scale: float = 7.0
    reference_url: str | None = None
    reference_path: str | None = None
    resolution: str | None = "720p"
    aspect_ratio: str = "9:16"
    length: str = "4s"


class Response(BaseModel):
    total_time: int = 0
    time_per_step: float = 0
    s3_url: str = ""


class Job(BaseModel):
    job_id: str = None
    job_request: Request = None
    job_progress: int = 0
    job_status: str = JobStatus.WAITING.value  # Initial status
    job_result: Response | None = None
