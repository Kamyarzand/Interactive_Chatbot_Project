import sys

def setup_encoding():
    """تنظیم انکودینگ برای خروجی"""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

def list_questions(qa_list):
    """
    نمایش ساده تمام سوالات در پایگاه دانش
    """
    if not qa_list:
        print("پایگاه دانش خالی است.")
        return

    print("لیست سوالات:")
    print("-" * 40)
    
    for i, qa in enumerate(qa_list, 1):
        try:
            # فقط شماره و متن سوال رو نمایش میدیم
            print(f"{i}. {qa['question']}")
        except Exception as e:
            print(f"خطا در نمایش سوال {i}: {str(e)}")
    
    print("-" * 40)