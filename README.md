# trackml-seattle
## info
https://indico.cern.ch/event/658267/sessions/265774/

## login to fnal/aws
```bash
ssh -L localhost:8899:localhost:8899 jduarte1@cmslpc-sl6@fnal.gov
ssh -L localhost:8899:localhost:8899 ec2-user@34.215.95.84
```

## install miniconda3
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
```bash
wget https://www.dropbox.com/s/ew4jm6jwu2quo21/public_data.zip?dl=1
mv public_data.zip?dl=1 public_data.zip
unzip public_data
```

## launch jupyter
```bash
jupyter notebook --ip 127.0.0.1 --port 8899 --no-browser
```
