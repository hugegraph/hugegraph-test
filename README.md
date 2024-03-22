# hugegraph-test

CI testing is carried out through this project for hugegraph

```bash
git clone https://github.com/hugegraph/hugegraph-test.git

cd hugegraph-test

# try pip3 if pip is not found, or set alias
pip install -r requirements.txt

cd src
# try python3 if pip is not found, or set alias
python --version # ensure version is in 3.8~3.10

# cleanup existed environment and data if you need
bash cleanup.sh

''' 
Note: modify the configs in basic_config.py before run the test script
1. modify server/toolchain_release_version (like 1.3.0 -> 1.5.0)
2. modify server/toolchain_git_branch_commit
3. modify auth/https/serice ports if need..
'''
python deploy_start.py all # or 'server' or 'toolchain'

# 2. decompress dataset
unzip src/config/dataset.zip -d src/config/

# 3. run test
pytest 
# OR
pytest --html=test.html --capture=tee-sys
```

**Note:** python version must be in `[3.8, 3.10]`
