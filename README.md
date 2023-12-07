# hugegraph-test

CI testing is carried out through this project for hugegraph

```bash
git clone https://github.com/hugegraph/hugegraph-test.git

cd hugegraph-test

pip install -r requirements.txt

cd src
python deploy_start.py all

pytest
```

Note: python >= 3.8 and <= 3.10
