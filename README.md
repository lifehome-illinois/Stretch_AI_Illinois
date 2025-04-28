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
# Step 1: Create a new conda environment
conda create -n stretch_ai python=3.10 -y

# Step 2: Activate the environment
conda activate stretch_ai

# Step 3: Upgrade pip (optional but recommended)
pip install --upgrade pip

# Step 4: Install the specific versions of torch, torchvision, and torchaudio
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1
```

#### 2.2.3 Installing Dependent Packages
