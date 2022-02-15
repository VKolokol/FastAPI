from typing import List

from fastapi import APIRouter, Depends, Response, HTTPException, status

from models.users import User
from models.jobs import Jobs, JobIn
from repositories.jobs import JobRepository
from permissions.get_permissions import Permissions
from endpoints.depends import get_job_repository, get_current_user, get_permissions
from schemas.jobs import ViewJobsWithUsers


router = APIRouter()


@router.get('/', response_model=List[ViewJobsWithUsers])
async def get_jobs(
        jobs: JobRepository = Depends(get_job_repository),
        limit: int = 100,
        skip: int = 0
):
    return await jobs.get_all(limit=limit, skip=skip)


@router.get('/{job_id}')
async def get_job(
    job_id: int,
    jobs: JobRepository = Depends(get_job_repository),
):
    return await jobs.get_object(job_id)


@router.post('/', response_model=Jobs)
async def create_job(
        job: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
):
    if current_user.is_company:
        return await jobs.create(user_id=current_user.id, job=job)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")


@router.patch('/{job_id}', response_model=Jobs)
async def update_job(
        job_id: int,
        job: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
        permissions: Permissions = Depends(get_permissions)
):
    current_job = await jobs.get_object(job_id)

    permissions.get_permission(obj=current_job, user=current_user, user_id=current_job.owner_id)

    return await jobs.update(job_id=job_id, job=job)


@router.delete('/{job_id}')
async def remote_job(
        job_id: int,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
        permissions: Permissions = Depends(get_permissions)
):
    job = await jobs.get_object(job_id)

    permissions.get_permission(obj=job, user=current_user, user_id=job.owner_id)

    await jobs.remove(job_id=job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
