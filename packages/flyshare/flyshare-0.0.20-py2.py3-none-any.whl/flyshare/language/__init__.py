# encoding: UTF-8

# 默认设置
from chinese import text, constant

# 是否要使用英文
import flyshare.ApiConfig as ac

if ac.LANGUAGE == 'english':
    from english import text, constant
