import os
import re
import multiprocessing

def is_valid_file(file_name):
    # '숫자_문자열' 패턴을 가진 파일은 필터링합니다.
    pattern = r'\d+_[^\d]+'
    return not re.match(pattern, file_name)

def rename_file(file_path, folder_path):
    try:
        # 파일명과 확장자를 분리합니다.
        file_name = os.path.basename(file_path)
        file_name_without_extension, file_extension = os.path.splitext(file_name)
        
        # 파일명에서 '-', '~', 공백을 제거하고 strip()을 적용합니다.
        cleaned_file_name = re.sub(r'[-~ _(),.+!/]+', '', file_name_without_extension)
        
        # 파일명을 숫자 배열과 문자열 배열로 분리합니다.
        numbers = re.findall(r'\d+', cleaned_file_name)
        strings = re.findall(r'[^\d]+', cleaned_file_name)
        
        # 숫자와 문자열을 '_'로 구분하여 조합합니다.
        new_file_name = "_".join(numbers + strings)
        
        # 새 파일명에 확장자를 추가합니다.
        new_file_name_with_extension = new_file_name + file_extension
        
        # 새 파일명으로 파일을 rename 합니다.
        new_file_path = os.path.join(folder_path, new_file_name_with_extension)
        os.rename(file_path, new_file_path)
        
        print(f"파일 '{file_name}'을 '{new_file_name_with_extension}'로 rename 했습니다.")
    except Exception as e:
        print(f"파일 '{file_name}'을 처리하는 동안 오류 발생: {str(e)}")

def rename_files_in_current_folder(folder_path=None):
    if folder_path is None:
        folder_path = os.getcwd()

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # '숫자_문자열' 패턴을 가진 파일은 필터링합니다.
    files = [f for f in files if is_valid_file(f)]

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # CPU 코어 수에 따라 병렬 처리
    pool.starmap(rename_file, [(os.path.join(folder_path, file_name), folder_path) for file_name in files])
    pool.close()
    pool.join()

if __name__ == "__main__":
    rename_files_in_current_folder()
