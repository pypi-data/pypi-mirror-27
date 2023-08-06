# flask_template

templates used to fast create flask project.

## install

`pip install flask_template`


# usage

`flasktemplate create [-t simple] project_name`

will create a flask project directory named after project_name on current path.

`flasktemplate list` will list current supported templates.


# update logs

## 0.4

1. 增加migrations目录，修改默认env.py，在alembic.ini增加alembic:include和alembic:exclude字段支持，以限定alembic
  默认检测的表;

2. 修复一些typo；
