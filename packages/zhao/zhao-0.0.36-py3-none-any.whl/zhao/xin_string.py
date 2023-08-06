# -*- coding:utf-8 -*-
"""zhao.xin_string
提供字符串相关的函数及对象
"""
# Information from https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
# The Chinese, Japanese and Korean (CJK) scripts share a common background,
# collectively known as CJK characters. Unicode 8.0, Unicode defines a total
# of 80,388 CJK Unified Ideographs.

UNICODE_VERSION = '8.0'
TATAL_CJK_UNIFIED_IDEOGRAPHS = 80388
TATAL_CHINESE_CHARACTERS = 'TOO MANY, WHO KNOWS'
CJK_UNIFIED_IDEOGRAPHS_BLOCKS = \
    dict(CJK_Unified_Ideographs=(0x4E00, 0x9FD5, 0x9FFF),  # 常用
         CJK_Unified_Ideographs_Extension_A=(0x3400, 0x4DB5, 0x4DBF),  # 不常用
         CJK_Unified_Ideographs_Extension_B=(0x20000, 0x2A6D6, 0x2A6DF),  # 更少
         CJK_Unified_Ideographs_Extension_C=(0x2A700, 0x2B734, 0x2B73F),  # 更少
         CJK_Unified_Ideographs_Extension_D=(0x2B740, 0x2B81D, 0x2B81F),  # 更少
         CJK_Unified_Ideographs_Extension_E=(0x2B820, 0x2CEA1, 0x2CEAF),  # 更少
         CJK_Compatibility_Ideographs=(0xF900, 0xFAFF, 0xFAFF),  # 有12个不连续
         # 以上为 80,388 CJK Unified Ideographs defined in Unicode 8.0
         CJK_Radicals_Supplement=(0x2E80, 0x2EF3, 0x2EFF),  # 常用偏旁部首
         Kangxi_Radicals=(0x2F00, 0x2FD5, 0x2FDF),  # 康熙字典偏旁部首
         Ideographic_Description_Characters=(0x2FF0, 0x2FFB, 0x2FFF),  # 字形
         CJK_Symbols_and_Punctuation=(0x3000, 0x303F, 0x303F),  # 标点符号
         CJK_Strokes=(0x31C0, 0x31E3, 0x31EF),  # 笔画
         Enclosed_CJK_Letters_and_Months=(0x3200, 0x32FD, 0x32FF),  # 日韩括号字
         CJK_Compatibility=(0x3300, 0x33FF, 0x33FF),  # ?
         CJK_Compatibility_Forms=(0xFE30, 0xFE4F, 0xFE4F),  # ?
         CJK_Compatibility_Ideographs_Supplement=(0x2F800, 0x2FA1D, 0x2FA1F))  # ?


def is_chinese(char):
    """判断字符是否是汉字
    - 其中有少数未用到的编码范围也包含在内
    - 不包含偏旁部首笔画及标点
    """
    code = ord(char)
    return (0x4E00 <= code <= 0x9FFF or
            0x3400 <= code <= 0x4DBF or     # EXT BLOCK A
            0x20000 <= code <= 0x2A6DF or   # EXT BLOCK B
            0x2A700 <= code <= 0x2CEAF or   # EXT BLOCK C~E
            0xF900 <= code <= 0xFAFF)


if __name__ == '__main__':
    print(is_chinese('㐀'))
