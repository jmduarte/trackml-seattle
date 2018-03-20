# trackml-seattle

## login to fnal/aws
ssh -L localhost:8899:localhost:8899 jduarte1@cmslpc-sl6@fnal.gov
ssh -L localhost:8899:localhost:8899 ec2-user@34.215.95.84

## install miniconda2
```bash
cp install_miniconda.sh ~/
cd ~
source install_miniconda.sh
```

## install everything else
```bash
cd trackml-seattle
source install.sh
```

## setup
```bash
source setup.sh
```

## get data
wget https://www.dropbox.com/s/ew4jm6jwu2quo21/public_data.zip?dl=1

## launch jupyter
jupyter notebook --ip 127.0.0.1 --port 8899 --no-browser &