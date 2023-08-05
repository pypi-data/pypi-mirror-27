# GitPackageManager
Import directly from git.

## :: ALPHA 1 v0.5 version :: (Please do not use this in production just yet.)

```bash
sudo pip3.6 install python-git-pkgManager
```

# simple usage.

```python
from gitPkgManager.pkgManager import GitPackageManager
GitPackageManager(ssh_repo_url="git@github.com:{username}/{library}.git",
              save_path="/project_path/libraries/")
# than simple use it.
import project.path.libraries.{library}
```

## Yet another simple example:
Using pymysql database directly importing from git.

```python
from gitPkgManager.pkgManager import GitPackageManager
GitPackageManager(ssh_repo_url="git@github.com:PyMySQL/PyMySQL.git",
              save_path="/Users/benny/PycharmProjects/poc/libraries")
import libraries.PyMySQL.pymysql as pymysql

cnt = pymysql.connect(**{"host": "localhost", "port": 3306, "user": "hiveuser", "password":
    "XXX", "database": "surge_test"})

cur = cnt.cursor()
cur.execute("SELECT NOW()")
print(cur.fetchall())

```

# Usage suggestion:

A. create file packages.py
```python
from gitPkgManager.pkgManager import GitPackageManager


SAVE_PATH = "/Users/benny/git_import/libraries/"

PACKAGES = {
    "pymysql": {
        "ssh_repo_url": "git@github.com:PyMySQL/PyMySQL.git",
        "save_path": SAVE_PATH
    },
    "credstash": {
        "ssh_repo_url": "git@github.com:fugue/credstash.git",
        "save_path": SAVE_PATH,
        "use_commit": "7969917f1a77cf1350933ceca0faeb60df907187"
    },
    "boto3": {
        "ssh_repo_url": "git@github.com:boto/boto3.git",
        "save_path": SAVE_PATH
    },
    "records": {
        "ssh_repo_url": "git@github.com:kennethreitz/records.git",
        "save_path": SAVE_PATH
    },
    "DummyRDD": {
        "ssh_repo_url": "git@github.com:wdm0006/DummyRDD.git",
        "save_path": SAVE_PATH
    },
    "Retrying": {
        "ssh_repo_url": "git@github.com:rholder/retrying.git",
        "save_path": SAVE_PATH,
        "alwyas_async": True
    },
    "commonRegex": {
        "ssh_repo_url": "git@github.com:madisonmay/CommonRegex.git",
        "save_path": SAVE_PATH
    },
    "TimeConvert": {
        "ssh_repo_url": "git@github.com:xxx-convert/TimeConvert.git",
        "save_path": SAVE_PATH
    },
    "tzlocal": {
        "ssh_repo_url": "git@github.com:regebro/tzlocal.git",
        "save_path": SAVE_PATH
    }

}

print("Analyzing project libraries..")
for package_name, package_info in PACKAGES.items():
    GitPackageManager(**package_info)
print("Done..")
```

B. in your project main import the file and forget it. :)
```python
import packages  # act as the package manager.
import libraries.boto3.boto3 as boto3
import libraries.PyMySQL.pymysql as pymysql
import libraries.credstash.credstash as cstash
import libraries.records.records as records
from libraries.DummyRDD.dummy_spark import SparkConf, SparkContext
from libraries.retrying.retrying import retry
from libraries.CommonRegex.commonregex import CommonRegex
from libraries.TimeConvert.TimeConvert import TimeConvert as tc

# Code samples. :P

boto3.resource("s3")
# cstash.getSecret("")
# pymysql.connect(**{})

# db = records.Database('sqlite:///users.db')
sconf = SparkConf()
sc = SparkContext(master='', conf=sconf)
rdd = sc.parallelize([1, 2, 3, 4, 5])
print(rdd.count())
print(rdd.map(lambda x: x**2).collect())
parser = CommonRegex()
print(parser.times("When are you free?  Do you want to meet up for coffee at 4:00?"))
dt = tc.utc_datetime()
print(dt)

```

That's it. use the packages according to the selected path.

Available options , `use_branch`, to insure you use specific branch.
`use_commit` - to use a specific commit.
`always_sync`- to be syncing with your your selected branch.



# Notes:


* Dependencies of packages are not implemented yet so if the package is depending another external package which you don't have you will get an exception.
* Some of the packages will fail to work due to Paths problem, this issue is fixable but required the user to adujst some imports in the cloned library.

### Solution: ###

"#1"

Install the dependency by adding it to the file, just find the route in github.

"#2"

just work with the exceptions and modify the path of the import file with your path.
i.e TimeConvert package required to do so, I did it in aprox~ 3 minutes.