# Stretch Pick and Place demo compatible with Low End GPU.

## 1. Hardware Tested On

Processor : 13th Gen Intel® Core™ i9-13900H Processor 2.6 GHz (24M  Cache, up to 5.4 GHz, 14 cores: 6 P-cores and 8 E-cores)

Graphics : NVIDIA® GeForce RTX™ 4070 Laptop GPU (321 AI TOPs)
 ROG Boost: 2030MHz* at 140W (1980MHz Boost Clock+50MHz OC, 115W+25W Dynamic Boost, 115W+25W in Manual Mode)
 8GB GDDR6

Memory : 16GB DDR5-4800 SO-DIMM


**Note :** This repository contains a custom version of the [Stretch AI repository](https://github.com/hello-robot/stretch_ai) to be compatible with GPUs with lower VRAM and performance will vary from what's shown in the repository. 

## 2. Setting Up Your System

OS : Ubuntu 20.04

CUDA: 12.4

### 2.1 CUDA Installation Guide

Installation steps taken from [CUDA 12.4 toolkit documentation](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html). For Additional details or debugging please refer to the original doumentation.

If you have CUDA installed and would like to switch to 12.4 version, you could also follow this guide.


#### 2.1.1 Pre-installation Actions

Steps taken from [here](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#pre-installation-actions).

1. Validating CUDA-capabale GPU : ``lspci | grep -i nvidia``
 
    If you do not see any settings, update the PCI hardware database that Linux maintains by entering update-pciids (generally found in /sbin) at the command line and rerun the previous lspci command.

    If your graphics card is from NVIDIA and it is listed in https://developer.nvidia.com/cuda-gpus, your GPU is CUDA-capable.

2. Verify the System Has gcc Installed : ``gcc --version``

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

#### 2.1.4 Optional Actions

1. [Power 9 Setup ](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#power9-setup)

2. [Verifying Instllation](https://docs.nvidia.com/cuda/archive/12.4.0/cuda-installation-guide-linux/index.html#power9-setup)

### 2.2 Stretch AI Virtual Environment Setup Guide

Steps taken from the [Stretch AI Repository](https://github.com/hello-robot/stretch_ai/blob/main/docs/start_with_docker_plus_virtenv.md).

**Note:** As of now pytorch installation through conda/mamba is currently not supported and may change in the future. So pytorch is required to be installed using pip.

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


### 2.3 Stretch AI Docker Setup In Stretch Robot

Steps taken from [here](https://github.com/hello-robot/stretch_ai/blob/main/docs/start_with_docker_plus_virtenv.md#install-docker-on-the-robot). 

#### 2.3.1 SSH or connect to the Stretch Robot 

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

You will need to clone the *stretch-ai* repository on your robot to access the "robot script".

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


https://github.com/hello-robot/stretch_ai/blob/main/docs/start_with_docker_plus_virtenv.md


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


 <iframe width="560" height="315" src="https://uofi.box.com/s/z17qanjpvfsburltnl2xchyvrimqwanz" frameborder="0" allowfullscreen></iframe>
