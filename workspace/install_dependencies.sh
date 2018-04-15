apt install -y python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose python-pip
cd dependencies
git clone https://github.com/dat/pyner.git
pip install -r ../requirements.txt
python -m nltk.downloader stopwords -d /usr/local/share/nltk_data
cd pyner/
python setup.py install
cd ..
cp english.long /usr/local/share/nltk_data/corpora/stopwords/