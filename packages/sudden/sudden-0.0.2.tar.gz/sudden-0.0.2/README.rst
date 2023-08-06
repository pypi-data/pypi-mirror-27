Sudden
======

Sudden is a command line interface for automating the installation of software in Ubuntu/Debian Linux systems using a simple and intuitive way.

It tries to integrate other package managers such as apt, pip, conda and etc.

This project was inspired by `AUR<https://aur.archlinux.org>` and `packer<https://bbs.archlinux.org/viewtopic.php?id=88115>`

Examples
========

sudden -i docker conda rstudio pip sublime telegram spotify java8 chrome htop python3-dev

Sudden can also be used to install Bioinformatics packages:

sudden -i bwa gatk picard fastqc qualimap sambamba deepvariant snpeff vep 

----

Installation
************

pip install sudden

Usage
*****

For installing binaries:

sudden -i conda
sudden -i rstudio
sudden -i sublime
sudden -i telegram
sudden -i spotify
sudden -i java8
sudden -i chrome
sudden -i htop

For installing direct from source:

sudden -s conda
sudden -s rstudio
sudden -s sublime
sudden -s telegram
sudden -s spotify
sudden -s java8
sudden -s chrome
sudden -s htop

You can provide a requirements file to install your packages with sudden

requirements.sud

ubuntu:
  bwa
  samtools
  vcftools
  tabix
github:
  raonyguimaraes/pynnotator
pypi:
  pynnotator
conda:
  mosdepth

.sudden/
    .priority
        ubuntu
        pypi
        conda
        github
        source
        external
    .config


This will install all the packages available in your repository github.com/raonyguimaraes/sudden-repo

sudden -g raonyguimaraes/sudden-repo
