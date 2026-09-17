from app.job_loader import load_jobs


class JobRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_all(self):
        return load_jobs(file_path=self.file_path)

    def get_by_id(self, job_id):
        jobs = load_jobs(file_path=self.file_path)
        for job in jobs:
            if job.job_id == job_id:
                return job
        return None

