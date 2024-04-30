import datetime
import os

class Log():
    def __init__(self) -> None:
        self.max_file_count=20

        self.log_folder_path= "logs"
        current_datetime = datetime.datetime.now()
        filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S.txt")
        self.file_path = os.path.join(self.log_folder_path, filename)

    def enter_log(self, log:dict):
        with open(self.file_path,'a') as file: #Append mode
            for key, value in log.items():
                file.write(f"{key}: {value}\n" )
        file_list = os.listdir(self.log_folder_path)
        num_files=len(file_list)

        if num_files>self.max_file_count:
            self.delete_oldest_file()
            

    def delete_oldest_file(self):
        files = os.listdir(self.log_folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(self.log_folder_path, f))] # Filter out directories (if any)

        if files:
            file_times = [(f, os.path.getctime(os.path.join(self.log_folder_path, f))) for f in files] #Get the metadata change of each file
            sorted_files = sorted(file_times, key=lambda x: x[1])

            # Get the oldest file
            oldest_file_name = sorted_files[0][0]
            file_path = os.path.join(self.log_folder_path, oldest_file_name)

            # Delete the oldest file
            os.remove(file_path)
            print("Oldest file deleted:", oldest_file_name)
        else:
            print("No files in the directory to delete.")