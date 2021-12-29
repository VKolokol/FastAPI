from typing import List

from fastapi import APIRouter, Depends, Response, HTTPException, status

from models.users import User
from models.proposals import Proposal, ProposalIn, ProposalUpdateIn
from repositories.proposals import ProposalRepository
from repositories.jobs import JobRepository
from permissions.get_permissions import Permissions
from endpoints.depends import get_current_user, get_proposal_repository, get_job_repository, get_permissions

router = APIRouter()


@router.post('/', response_model=Proposal)
async def send_proposal(
        proposal: ProposalIn,
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
        permissions: Permissions = Depends(get_permissions)
):
    current_job = await job.get_object(proposal.job_id)

    permissions.get_permission(obj=current_job, user=current_user, user_id=proposal.user_id)

    return await proposals.create(**proposal.dict())


@router.patch('/', response_model=Proposal)
async def reply_to_proposal(
        update: ProposalUpdateIn,
        proposal: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user),
        permissions: Permissions = Depends(get_permissions)
):
    current_job = await job.get_object(update.job_id)
    current_proposal = await proposal.get_object(update.user_id, update.job_id)

    permissions.get_permission(obj=current_job, user=current_user, user_id=current_job.owner_id)
    permissions.get_object(obj=current_proposal)

    return await proposal.update(update)


@router.get('/{user_id}', response_model=List[Proposal])
async def user_proposal(
        user_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")

    return await proposals.get_all(user_id)


@router.get('/candidates/{job_id}')
async def candidates_on_job(
        job_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        permissions: Permissions = Depends(get_permissions)
):
    current_job = await job.get_object(job_id)

    permissions.get_permission(obj=current_job, user=current_user, user_id=current_job.owner_id)

    return await proposals.get_all_candidates(job_id)


@router.get('/{user_id}/{job_id}')
async def proposal_detail(
        user_id: int,
        job_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        permissions: Permissions = Depends(get_permissions)

):
    current_job = await job.get_object(job_id)

    permissions.get_permission(obj=current_job, user=current_user, user_id=user_id)

    return await proposals.get_object(user_id, job_id)


@router.delete('/{user_id}/{job_id}')
async def remove_proposal(
        user_id: int,
        job_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        permissions: Permissions = Depends(get_permissions)
):
    current_job = await job.get_object(job_id)

    permissions.get_permission(obj=current_job, user=current_user, user_id=user_id)

    await proposals.remove(user_id, job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
