import os

def list_all_files(directory):
    """
    تقوم هذه الدالة بالمرور على كل المجلدات الفرعية في المسار المحدد
    وتُرجع قائمة بجميع مسارات الملفات.
    """
    # قائمة فارغة لتخزين مسارات الملفات التي سنجدها
    file_paths = []

    # os.walk هي أفضل طريقة للمرور على شجرة المجلدات
    for root, dirs, files in os.walk(directory):
        # المرور على كل اسم ملف في القائمة 'files'
        for filename in files:
            # دمج مسار المجلد الحالي مع اسم الملف للحصول على المسار الكامل
            full_path = os.path.join(root, filename)
            # إضافة المسار الكامل إلى قائمتنا
            file_paths.append(full_path)
            
    return file_paths

# --- الجزء الرئيسي من البرنامج ---
if __name__ == "__main__":
    # تحديد مجلد المشروع. النقطة '.' تعني "المجلد الحالي الذي يتم تشغيل الكود منه"
    project_folder = '.'

    print(f"--- البحث عن الملفات في المجلد: '{os.path.abspath(project_folder)}' ---")

    # استدعاء الدالة للحصول على قائمة الملفات
    all_files_in_project = list_all_files(project_folder)

    # التحقق مما إذا تم العثور على أي ملفات
    if all_files_in_project:
        # طباعة كل مسار ملف في سطر جديد
        for file_path in all_files_in_project:
            print(file_path)
    else:
        print("لم يتم العثور على أي ملفات في هذا المجلد.")

    print(f"\n--- إجمالي عدد الملفات التي تم العثور عليها: {len(all_files_in_project)} ---")