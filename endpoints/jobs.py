from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.users import User
from models.jobs import Jobs, JobIn
from repositories.jobs import JobRepository
from endpoints.depends import get_job_repository, get_current_user
from schemas.jobs import ViewJob, ViewJobsWithUsers


router = APIRouter()


@router.get('/', response_model=List[ViewJobsWithUsers])
async def get_jobs(
        jobs: JobRepository = Depends(get_job_repository),
        limit: int = 100,
        skip: int = 0
):
    return await jobs.get_list(limit=limit, skip=skip)


@router.post('/', response_model=Jobs)
async def create(
        job: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
):
    if current_user.is_company:
        return await jobs.create_job(user_id=current_user.id, job=job)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")


@router.put('/', response_model=ViewJob)
async def update_job(
        job_id: int,
        job: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)
):
    old_job = await jobs.get_object(job_id)

    if old_job is None or old_job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found job")

    return await jobs.update(job_id=job_id, job=job)
