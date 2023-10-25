import json
import logging
import os
from scripts import ResumeProcessor, JobDescriptionProcessor
from scripts.utils import init_logging_config, get_filenames_from_dir

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def remove_old_files(files_path):
    try:
        for filename in os.listdir(files_path):
            file_path = os.path.join(files_path, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)

        logging.info("Deleted old files from " + files_path)
    except Exception as e:
        logging.error(f"Error deleting files from {files_path}:\n{e}")

def process_files(file_directory, processor_class, processed_directory, item_name):
    try:
        remove_old_files(processed_directory)
        file_names = get_filenames_from_dir(file_directory)
        logging.info(f'Reading from {file_directory} is now complete.')
        logging.info(f'Started processing {item_name}s.')

        for file in file_names:
            processor = processor_class(file)
            success = processor.process()

        logging.info(f'Processing of {item_name}s is now complete.')
    except Exception as e:
        logging.error(f'An error occurred while processing {item_name}s: {str(e)}')

if __name__ == "__main__":
    init_logging_config()
    
    PROCESSED_RESUMES_PATH = "Data/Processed/Resumes"
    PROCESSED_JOB_DESCRIPTIONS_PATH = "Data/Processed/JobDescription"
    
    logging.info('Started to read from Data/Resumes')
    try:
        process_files("Data/Resumes", ResumeProcessor, PROCESSED_RESUMES_PATH, "resume")
    except:
        logging.error('There are no resumes present in the specified folder.')
        logging.error('Exiting from the program.')
        logging.error('Please add resumes in the Data/Resumes folder and try again.')
        exit(1)
    
    logging.info('Started to read from Data/JobDescription')
    try:
        process_files("Data/JobDescription", JobDescriptionProcessor, PROCESSED_JOB_DESCRIPTIONS_PATH, "job description")
    except:
        logging.error('There are no job descriptions present in the specified folder.')
        logging.error('Exiting from the program.')
        logging.error('Please add job descriptions in the Data/JobDescription folder and try again.')

    logging.info('Success! Now run `streamlit run streamlit_second.py`')
