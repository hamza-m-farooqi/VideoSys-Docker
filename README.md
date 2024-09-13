
# Video-Sys Docker Setup and Google Cloud Artifact Registry Integration

This guide will walk you through setting up a Docker container, committing the current state after downloading all the necessary models, and pushing the image to Google Cloud Artifact Registry for use in Google Cloud batch jobs.

This project is based on the following repository: [NUS-HPC-AI-Lab/VideoSys](https://github.com/NUS-HPC-AI-Lab/VideoSys.git)

<!-- ## 1. Clone & Setup 
```bash
git clone https://github.com/NUS-HPC-AI-Lab/VideoSys.git
cd VideoSys
pip install -e .
``` -->

## 1. Modify `main.py`

### Step 1: Comment Out the Following Code
In `main.py`, comment out the following section of the code:

```python
if __name__ == "__main__":
    args = parse_args()
    # Convert the JSON string back to a dictionary
    request_dict = json.loads(args.request_dict)

    # Call the train function with the parsed dictionary
    generate(request_dict)
```

### Step 2: Uncomment the Following Code
Uncomment the `request_dict` and the call to `generate()` in the `main.py` file:

```python
request_dict = {
#     "prompt": "a close-up portrait of a woman set against a snowy backdrop. the woman is wearing a golden crown with a feathered design and a matching golden garment with a textured pattern. her makeup is dramatic, featuring dark red lipstick and smoky eyes. she has a neutral expression on her face and is looking directly at the camera. The background is blurred but appears to be a snowy landscape with trees and a clear sky. The lighting suggests it is daytime with natural light illuminating the scene. There are no visible texts or logos in the video. The style of the video is a fashion or portrait photograph with a focus on the woman's attire and makeup.",
#     "webhook": "https://webhook-test.com/1d708700d3cca1d504145ba553c9cf4d",
}

# generate(request_dict)
```

## 2. Build and Run Docker Image

### Step 1: Create Docker Image
Run the following command to build the Docker image:

```bash
docker build -t video-sys .
```

### Step 2: Run Docker Container with GPU Support
Run the container using the command below to start the image with GPU access:

```bash
docker run --gpus all --privileged -it video-sys /bin/bash
```

### Step 3: Run `main.py` and Download Models
Once inside the container, run the `main.py` script:

```bash
python3 main.py
```

This will download all required models into the container. After a successful video generation, the image size will be approximately **35GB**.

### Step 4: Commit the Current Container State
Once the process is complete, commit the current state of the container into a new Docker image:

```bash
docker commit <container_id_or_name> video-sys:latest
```

## 3. Google Cloud Setup

Now that the Docker image is ready, we will push it to **Google Cloud Artifact Registry**.

### Optional: Google Cloud Initial Setup

If you haven't already configured your Google Cloud environment, follow these steps:

1. **Login to Google Cloud Console**: Access your [Google Cloud Console](https://console.cloud.google.com/).
2. **Create an Artifact Registry Repository**: 
   - Go to **Artifact Registry**.
   - Create a repository in the region where you have available quotas for your resources.

### Step 1: Authenticate Google Cloud CLI
Log in to your Google Cloud account and configure Docker to work with Artifact Registry:

```bash
gcloud auth login
gcloud config set project <project-id>
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Step 2: Tag the Docker Image for Artifact Registry
Tag your Docker image using the following command:

```bash
docker tag video-sys:latest us-central1-docker.pkg.dev/<project-id>/<artifacts-repository>/<image-name>:<tag>
```

### Step 3: Push the Docker Image to Google Artifact Registry
Push the tagged Docker image to the Google Artifact Registry:

```bash
docker push us-central1-docker.pkg.dev/<project-id>/<artifacts-repository>/<image-name>:<tag>
```

## 4. Using the Image for Google Cloud Batch Jobs

Now that the image is pushed to Google Cloud Artifact Registry, you can use it in **Google Cloud Batch Jobs**. The code in `main.py` is designed to work efficiently with batch jobs.

You're all set!
