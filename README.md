# Stretch Pick and Place Demo (Optimized for Low-End GPUs)

This demo showcases the STRETCH robot’s ability to interpret natural language commands and autonomously perform pick-and-place tasks. The robot can identify, grasp, and place objects without human intervention.

### Overview

The original [pick-and-place implementation](https://github.com/hello-robot/stretch_ai/blob/main/docs/llm_agent.md) utilizes the DETIC perception model alongside the SIGLIP feature matcher to recognize over 20,000 objects and receptacles. However, due to reliability issues with SIGLIP, it has been disabled. Instead, raw DETIC outputs are used for more consistent performance.

### Object and Receptacle Recognition

The robot is capable of recognizing a wide variety of objects and receptacles. Below are the currently supported categories:

<details>
<summary><strong>Objects (click to expand)</strong></summary>

```json
{
        "action_figure": 0,
        "android_figure": 1,
        "apple": 2,
        "backpack": 3,
        "baseballbat": 4,
        "basket": 5,
        "basketball": 6,
        "bath_towel": 7,
        "battery_charger": 8,
        "board_game": 9,
        "book": 10,
        "bottle": 11,
        "bowl": 12,
        "box": 13,
        "bread": 14,
        "bundt_pan": 15,
        "butter_dish": 16,
        "c-clamp": 17,
        "cake_pan": 18,
        "can": 19,
        "can_opener": 20,
        "candle": 21,
        "candle_holder": 22,
        "candy_bar": 23,
        "canister": 24,
        "carrying_case": 25,
        "casserole": 26,
        "cellphone": 27,
        "clock": 28,
        "credit_card": 29,
        "cup": 30,
        "cushion": 31,
        "doll": 32,
        "dumbbell": 33,
        "egg": 34,
        "electric_kettle": 35,
        "electronic_cable": 36,
        "file_sorter": 37,
        "folder": 38,
        "fork": 39,
        "gaming_console": 40,
        "glass": 41,
        "hammer": 42,
        "hand_towel": 43,
        "handbag": 44,
        "hard_drive": 45,
        "hat": 46,
        "helmet": 47,
        "jug": 48,
        "kettle": 49,
        "keychain": 50,
        "knife": 51,
        "ladle": 52,
        "lamp": 53,
        "laptop": 54,
        "laptop_cover": 55,
        "laptop_stand": 56,
        "lunch_box": 57,
        "milk_frother_cup": 58,
        "monitor_stand": 59,
        "mouse_pad": 60,
        "multiport_hub": 61,
        "pan": 62,
        "pen": 63,
        "pencil_case": 64,
        "phone_stand": 65,
        "picture_frame": 66,
        "pitcher": 67,
        "plant_container": 68,
        "plant_saucer": 69,
        "plate": 70,
        "potato": 71,
        "ramekin": 72,
        "scissors": 73,
        "screwdriver": 74,
        "shoe": 75,
        "soap_dish": 76,
        "soap_dispenser": 77,
        "spatula": 78,
        "spectacles": 79,
        "spicemill": 80,
        "sponge": 81,
        "spoon": 82,
        "spray_bottle": 83,
        "squeezer": 84,
        "statue": 85,
        "stuffed toy": 86,
        "stuffed_toy": 87,
        "sushi_mat": 88,
        "tape": 89,
        "teapot": 90,
        "tennis_racquet": 91,
        "tissue_box": 92,
        "tomato": 93,
        "toy_airplane": 94,
        "toy_animal": 95,
        "toy_bee": 96,
        "toy_cactus": 97,
        "toy_construction_set": 98,
        "toy_fire_truck": 99,
        "toy_food": 100,
        "toy_fruits": 101,
        "toy_pineapple": 102,
        "toy_swing": 103,
        "toy_vehicle": 104,
        "tray": 105,
        "vase": 106,
        "watch": 107,
	"person": 108
    },

```

</details>

<details>
<summary><strong>Receptacles (click to expand)</strong></summary>

```json
{
  {
        "bathtub": 0,
        "bed": 1,
        "bench": 2,
        "cabinet": 3,
        "chair": 4,
        "chest_of_drawers": 5,
        "couch": 6,
        "counter": 7,
        "filing_cabinet": 8,
        "hamper": 9,
        "serving_cart": 10,
        "shelves": 11,
        "shoe_rack": 12,
        "sink": 13,
        "stand": 14,
        "stool": 15,
        "table": 16,
        "toilet": 17,
        "trunk": 18,
        "wardrobe": 19,
        "washer_dryer": 20
    }
}
```

</details>

### Optimizations for Low-End Hardware

The original LLM-based voice interface requires over 8GB of VRAM. To support systems with lower memory:

* **Voice Interface**: The voice-based LLM has been replaced with the Whisper voice-to-text engine. The transcribed text is then passed to a lightweight text-based LLM for interpretation, greatly reducing VRAM usage.
* **Modified Pipeline**: To conserve memory, the LLM now processes the command *before* the robot is initialized. On high-end systems (>8GB VRAM), parallel initialization is possible for improved responsiveness.

### System Limitations

* **Execution Loop**: The demo does not support a continuous execution loop, as it requires to clear CUDA memory in low end machines (>8GB VRAM) to switch between using LLM and the robot pipeline.

* **Memory Usage**: As the robot identifies more objects, memory consumption increases. On machines with limited RAM, this can lead to system instability or crashes.
* **Duplicate Detections**: The robot may detect the same object multiple times at slightly different positions. Since it relies on depth data alone, inaccuracies can occur.

  * **Mitigation**:

    * Use known transforms to verify object positions.
    * Manually calibrate the camera.
    * Add logic to filter out duplicate detections based on spatial proximity.
    * CUDA memory can be cleared for LLM but to clear CUDA memory for the perception model is yet to be figured out, if it can be cleared then the demo can be ran in a loop.

### Improved Pick-and-Place Behavior

* **Graceful Fallback**: Previously, the robot would persist in searching for or grasping an object indefinitely. The updated pipeline includes timeouts and fallback behavior that returns the robot to a default position if the object is not found.
* **Smoother Placement**: Objects are now gently lowered before release, avoiding mid-air drops and improving stability and realism.




## 1. Hardware Tested On

Processor : 13th Gen Intel® Core™ i9-13900H Processor 2.6 GHz (24M  Cache, up to 5.4 GHz, 14 cores: 6 P-cores and 8 E-cores)

Graphics : NVIDIA® GeForce RTX™ 4070 Laptop GPU (321 AI TOPs)
 ROG Boost: 2030MHz* at 140W (1980MHz Boost Clock+50MHz OC, 115W+25W Dynamic Boost, 115W+25W in Manual Mode)
 8GB GDDR6

Memory : 16GB DDR5-4800 SO-DIMM

Robot : STRETCH 2 Modified to STRETCH 3 specs

Robot OS : Ubuntu 22.04

#### Recommended Specs from hello robot

We recommend the following hardware to run Stretch AI. Other GPUs and other versions of Stretch may support some of the capabilities found in this repository, but our development and testing have focused on the following hardware.

- **[Stretch 3](https://hello-robot.com/stretch-3-product) from [Hello Robot](https://hello-robot.com/)**
  - When *Checking Hardware*, `stretch_system_check.py` should report that all hardware passes.
- **Computer with an NVIDIA GPU**
  - The computer should be running Ubuntu 22.04. Later versions might work, but have not been tested.
  - Most of our testing has used a high-end CPU with an NVIDIA GeForce RTX 4090.
- **Dedicated WiFi access point**
  - Performance depends on high-bandwidth, low-latency wireless communication between the robot and the GPU computer.
  - The official [Stretch WiFi Access Point](https://hello-robot.com/stretch-access-point) provides a tested example.
- (Optional) [Stretch Dexterous Teleop Kit](https://hello-robot.com/stretch-dex-teleop-kit).
  - To use the learning-from-demonstration (LfD) code you'll need the Stretch Dexterous Teleop Kit.




**Note :** This repository contains a custom version of the [Stretch AI repository](https://github.com/hello-robot/stretch_ai) to be compatible with GPUs with lower VRAM and performance will vary from what's shown in the repository. 

## 2. Setting Up Your System

OS : Ubuntu 22.04

CUDA: 12.4

### 2.1 CUDA Installation Guide

Installation steps taken from [CUDA 12.4 toolkit documentation](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html). For Additional details or debugging please refer to the original doumentation.

**Note :** If you have CUDA installed you can skip to section 2.2. If would like to switch to 12.4 version, you could also follow this guide. If you are unsure about your CUDA version you can run the below command which will show you the cuda version.

```
Command:

nvcc --version

Output:

nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Tue_Feb_27_16:19:38_PST_2024
Cuda compilation tools, release 12.4, V12.4.99
Build cuda_12.4.r12.4/compiler.33961263_0

```



#### 2.1.1 Pre-installation Actions

Steps taken from [here](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#pre-installation-actions).

Open your terminal and run the below commands

1. Validating CUDA-capabale GPU : ``lspci | grep -i nvidia``
 
    This code will output the graphics card available in your system. If your graphics card is from NVIDIA and it is listed in https://developer.nvidia.com/cuda-gpus, your GPU is CUDA-capable.
    
    If you do not see any settings, update the PCI hardware database that Linux maintains by entering update-pciids (generally found in /sbin) at the command line and rerun the previous lspci command.

    

2. Verify the System Has gcc Installed : ``gcc --version``

    You will see a version displayed like below, if it does then you are good to go.

    ```
    gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
    Copyright (C) 2021 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    ```

   If an error message displays, you need to install the development tools from your Linux distribution or obtain a version of gcc and its accompanying toolchain from the Web.


#### 2.1.2 Installing CUDA

Download links taken from [here](https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local ).


1. Run the below command to install cuda 12.4

    ```
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pinsudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600wget https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda-repo-ubuntu2204-12-4-local_12.4.0-550.54.14-1_amd64.debsudo dpkg -i cuda-repo-ubuntu2204-12-4-local_12.4.0-550.54.14-1_amd64.debsudo cp /var/cuda-repo-ubuntu2204-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/sudo apt-get updatesudo apt-get -y install cuda-toolkit-12-4
    ```

#### 2.1.3 Post-Installations Actions

Steps taken from [here](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#post-installation-actions).


The PATH variable needs to include export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}. Nsight Compute has moved to /opt/nvidia/nsight-compute/ only in rpm/deb installation method. When using .run installer it is still located under /usr/local/cuda-12.4/.

To add this path to the PATH variable:
```
export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}
```
In addition, when using the runfile installation method, the LD_LIBRARY_PATH variable needs to contain /usr/local/cuda-12.4/lib64 on a 64-bit system, or /usr/local/cuda-12.4/lib on a 32-bit system

To change the environment variables for 64-bit operating systems:
```
    export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64\
                             ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
To change the environment variables for 32-bit operating systems:
```
export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
Note that the above paths change when using a custom install path with the runfile installation method.

**If you don't want to run these commands everytime to change CUDA version to 12.4, add the below commands to ~/.bashrc**


Open bashrc file using
```
gedit ~/.bashrc
```
Add the below lines of code in the file and save it. Then re launch the terminal
```
export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

#### 2.1.4 Recommended and Optional Actions

These steps are not required to setup this demo but would highly recommend to read the documents and install them if it's missing to ensure CUDA is working.

Full list of recommended actions - https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#recommended-actions

- **Power 9 setup**
    
    Systems now come installed with Power 9 setup when installing the OS and can be checked using the below commands.

    1. The NVIDIA Persistence Daemon should be automatically started for POWER9 installations. Check that it is running with the following command:

        ``systemctl status nvidia-persistenced``


    Because of the addition of new features specific to the NVIDIA POWER9 CUDA driver, there are some additional setup requirements in order for the driver to function properly. These additional steps are not handled by the installation of CUDA packages, and failure to ensure these extra requirements are met will result in a non-functional CUDA driver installation.

    If you did not have the service running  please follow the below link to setup Power 9, I did not have a need to do this personally.

    https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#power9-setup

- **Verification**
    
    This document will take you through multiple steps to ensure you are able to use CUDA to it's full extent.

    https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#verify-the-installation

### 2.2 Stretch AI Virtual Environment Setup Guide

Steps taken from the [Stretch AI Repository](https://github.com/hello-robot/stretch_ai/blob/main/docs/start_with_docker_plus_virtenv.md).

#### 2.2.1 Installing Conda

Steps taken from [here](https://www.anaconda.com/docs/getting-started/miniconda/install#basic-install-instructions).

1. Download miniconda and run the setup file.

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ~/Miniconda3-latest-Linux-x86_64.sh
```

2. Press Return to review Anaconda’s Terms of Service (TOS). Then press and hold Return to scroll. Enter yes to agree to the TOS.

3. Press Return to accept the default install location (PREFIX=/Users/<USER>/miniconda3), or enter another file path to specify an alternate installation directory. The installation might take a few minutes to complete.

4. Choose an initialization options:

    Yes - conda modifies your shell configuration to initialize conda whenever you open a new shell and to recognize conda commands automatically.
    
    No - conda will not modify your shell scripts. After installation, if you want to initialize, you must do so manually. For more information, see Manual shell initialization.

5. The installer finishes and displays, “Thank you for installing Miniconda3!”

6. Close and re-open your terminal window for the installation to fully take effect, or use the following command to refresh the terminal, depending on your shell:
```
source ~/.bashrc
```
#### 2.2.2 Creating Virtual Environment

Create a new virutal environment with python version 3.10 and then install pytorch.

**Note:** The environment can be installed easily through a single bash file provided in the original repository but as of now pytorch installation through conda/mamba is currently not supported and may change in the future. So pytorch is required to be installed using pip. I suggest keeping an eye out on the updated pushed in the original repo for the updated bash file. You can skip to 2.3 if you are installing using bash file.


```
# Create a new conda environment
conda create -n stretch_ai python=3.10 -y

# Activate the environment
conda activate stretch_ai

# Upgrade pip (optional but recommended)
pip install --upgrade pip

# Install the specific versions of torch, torchvision, and torchaudio
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1
```

#### 2.2.3 Installing Dependent Packages

Dependent Packages
```
# Install Git LFS - needed for large files like images
sudo apt-get install git-lfs
git lfs install

sudo apt-get update
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 espeak ffmpeg -y


# Clone the repository
# Do not forget the --recursive flag to clone submodules
git clone https://github.com/lifehome-illinois/Stretch_Ai.git --recursive


cd Stretch_Ai/stretch_ai

python -m pip install setuptools==69.5.1
python -m pip install -e ./src[dev]
```

Perception Packages

```
# Install detectron2 for perception (required by Detic)
git submodule update --init --recursive
cd third_party/detectron2
pip install -e .

# Install Detic for perception
cd ../../src/stretch/perception/detection/detic/Detic
# Make sure it's up to date
git submodule update --init --recursive
pip install -r requirements.txt

# Download DETIC checkpoint...
mkdir -p models
wget --no-check-certificate https://dl.fbaipublicfiles.com/detic/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth -O models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
```

#### 2.2.4 Setting up hugging face token

 1. Get Your Hugging Face Access Token

    Go to: https://huggingface.co/settings/tokens

    Generate a new token (if you don’t have one), with at least "Read" access.

2. Login Using Terminal

    Option A: Using huggingface-cli (recommended)
    ```
    pip install --upgrade huggingface_hub
    huggingface-cli login
    ```
    Then paste your token when prompted.

    Option B: Set it as environment variable (temporary)
    ```
    export HUGGINGFACE_TOKEN=your_token_here
    ```

Troubleshooting guide - https://huggingface.co/docs/hub/en/security-tokens


### 2.3 Stretch AI Docker Setup In Stretch Robot

Steps taken from [here](https://github.com/hello-robot/stretch_ai/blob/main/docs/start_with_docker_plus_virtenv.md#install-docker-on-the-robot). 

#### 2.3.1 SSH or connect to the Stretch Robot 

You can get the ip of stretch by connecting a display to the STRETCH robot.

Once you are connected and logged in, click on the top right WIFI icon -> WIFI (the network you are connected to) -> WIFI-settings -> click on the gear icon on the WIFI connected -> The ipv4 is your ip address.

Example: 

You can use the below command to ssh into Stretch 2

``ssh -X hello-robot@172.22.243.38``


#### 2.3.2 Install Docker on the Robot

Start by installing docker on your robot:

```
sudo apt-get update
sudo apt-get install docker.io
```

##### Optional: Setup Docker Group So You Do Not Need To Use `sudo`

You can add your user to the `docker` group so you do not need to use `sudo` to run Docker commands. To do this, run the following command:

1. Create the docker group if it doesn't already exist:

```bash
sudo groupadd docker
```

2. Add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

3. Restart the Docker service:

```bash
sudo systemctl restart docker
```

4. Log out and log back in so that your group membership is re-evaluated. Then you can verify that you can run Docker commands without sudo:

```bash
docker run hello-world
```

If you want to run a docker command without logging out, you can run the following command:

```bash
newgrp docker
```

This will change your group to the `docker` group for the current terminal session.

**When performing these steps on your robot, you may find that logging out fails to make docker group membership take effect.** In this case, you can try restarting Docker with the following command:

```bash
sudo systemctl restart docker
```

If this doesn't work, we recommend that you reboot your robot's computer.


#### 2.3.3 Clone the Stretch-AI Repository on your robot

You will need to clone the *stretch-ai* repository on your robot to access the "robot script" and run the stretch ROS2 bridge.

```bash
git clone https://github.com/hello-robot/stretch_ai.git
```

#### 2.3.4 Run the Robot's Script

The GitHub *stretch-ai* repository provides a startup script for running *stretch-ai* software in a Docker container on your Stretch robot. 

Prior to running the script, you need to have homed your robot with 
```
stretch_free_robot_process.py
stretch_robot_home.py
```

To use the Docker script, run the following command in the *stretch-ai* repository on the robot:

```
./scripts/run_stretch_ai_ros2_bridge_server.sh
```

You will see something like the following in the terminal as the Docker image is downloaded:

```
(base) hello-robot@stretch-se3-2005:~/src/stretchpy$ ./scripts/run_stretch_ai_ros2_bridge_server.sh 
Starting Stretch AI ROS2 Bridge Server on stretch-se3-3005
=========================================================
Unable to find image 'hellorobotinc/stretch-ai-ros2-bridge:latest' locally
latest: Pulling from hellorobotinc/stretch-ai-ros2-bridge
762bedf4b1b7: Pull complete                                         
84ceaedb8a21: Pull complete                                         
c558ecc26f22: Pull complete                                         
1006c31c0071: Downloading [===>                                               ]  33.99MB/484MB
2883f1b72f50: Download complete                                     
c29b29edc871: Download complete                                     
75fa503deb0b: Download complete                                     
03297d3829eb: Download complete 
fcf26cd86178: Download complete 
5bcaaf1fd219: Download complete 
431ffe29be39: Download complete 
79e926b74f85: Download complete 
4f4fb700ef54: Verifying Checksum 
27ae57810c0a: Downloading [=>                                                 ]  19.43MB/570.5MB
9ecd20cd6844: Download complete 
51c071dfcd29: Download complete 
438302fc8bd8: Download complete 
44999d133959: Downloading [>                                                  ]  10.79MB/10.57GB
a5ed971e796e: Pulling fs layer                                      
f570a0dd636d: Waiting                                               
1a08cbb00ee1: Waiting                                               
```

The Docker image can be large (i.e., > 10GB), so it takes time to download. You can plug an ethernet cable into your router and Stretch to speed up the download. You will only need to download each version of the *stretch-ai* Docker image a single time.

After downloading the Docker image, the server will begin running on your robot. Your robot should beep twice and its lidar should start spinning. The terminal should display output from the robot's *stretch-ai* server like the following:

```bash
[server-12] j='joint_wrist_yaw' idx=10 idx_q=10
[server-12] j='joint_wrist_pitch' idx=11 idx_q=11
[server-12] j='joint_wrist_roll' idx=12 idx_q=12
[server-12] ==========================================
[server-12] Starting up threads:                                    
[server-12]  - Starting send thread
[server-12]  - Starting recv thread
[server-12]  - Sending state information
[server-12]  - Sending servo information
[server-12] Running all...                                          
[server-12] Starting to send full state
[stretch_driver-3] [INFO] [1727454898.725969113] [stretch_driver]: Changed to mode = position
```



### 2.4 Validation 

The running the demo following the below link will open up the camera view in your system which utilizes your GPU. This is a recommended validation to check if the robot is able to use your system's GPU.

Original Guide : https://github.com/hello-robot/stretch_ai/blob/main/docs/start_with_docker_plus_virtenv.md


#### 2.4.1 Simple Installation Test

You can test your installation by running the `view_images` app.

While the Docker container on your robot is running, you can run the following commands in the terminal of your GPU computer.

First, you need to let the GPU computer know the IP address (#.#.#.#) for your Stretch robot.

```bash
./scripts/set_robot_ip.sh #.#.#.#
```

*Please note that it's important that your GPU computer and your Stretch robot be able to communicate via the following ports 4401, 4402, 4403, and 4404. If you're using a firewall, you'll need to open these ports.*

Next, run the `view_images` application in the Docker container on your GPU computer.

```
python -m stretch.app.view_images
```

With a functioning installation, the robot's gripper will open, the arm will move, and then you will see video from the robot's cameras displayed on your GPU computer.

To exit the app, you can press `q` with any of the popup windows selected.

If the `view_images` app doesn't work, the most common issue is that the GPU computer is unable to communicate with the robot over the network. We recommend that you verify your robot's IP address and use [`ping`](<https://en.wikipedia.org/wiki/Ping_(networking_utility)>) on your GPU computer to check that it can reach the robot.

You can validate it using the below commands

```
Here 172.22.243.38 is the ip of STRETCH 2 and 4401 is the port

$ nc -z -v 172.22.243.38 4401
Connection to 172.22.243.38 4401 port [tcp/*] succeeded!
$ nc -z -v 172.22.243.38 4402
Connection to 172.22.243.38 4402 port [tcp/*] succeeded!
$ nc -z -v 172.22.243.38 4403
Connection to 172.22.243.38 4403 port [tcp/*] succeeded!
$ nc -z -v 172.22.243.38 4404
Connection to 172.22.243.38 4404 port [tcp/*] succeeded!
```

## 3. Running The Pick And Place Demo using STRETCH 2


1. Turn on the Stretch Robot and connect to the robot through ssh with a terminal window using your laptop.

    ``ssh -X hello-robot@172.22.243.38``

    Home the robot using the below commandds

    ```
    stretch_free_robot_process.py
    stretch_robot_home.py
    ```

2. After Stretch has homed, run the ros2 bridge.

    ```
    cd /home/hello-robot/Desktop/stretch_ai_demo/stretch_ai
    ./scripts/run_stretch_ai_ros2_bridge_server.sh
    ````

3. After bringing up the ros2 bridge, open another terminal and go to the stretch_ai repository cloned in your latop/PC.
    
    ```
    cd ./Stretch_Ai/stretch_ai
    ./scripts/set_robot_ip.sh 172.22.243.38

    # for text 
    python -m stretch.app.lifehome_demo --use_llm

    or


    # for voice
    python -m stretch.app.lifehome_demo --use_llm --use_voice

    ```

4. The demo starts with you being able to chat with STRETCH robot. To activate the pick and place demo, you will need to say or type "pick and place demo" as this is hard coded in the demo.
5. After pick and place demo sequence is initiated try giving a command like "pick up the bottle and place it on the table".

Video demo example [here](https://uofi.app.box.com/file/1847915272622?s=z17qanjpvfsburltnl2xchyvrimqwanz)