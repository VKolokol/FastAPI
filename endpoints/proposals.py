from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.users import User
from models.proposals import Proposal, ProposalIn, ProposalUpdateIn
from repositories.proposals import ProposalRepository
from repositories.jobs import JobRepository
from endpoints.depends import get_current_user, get_proposal_repository, get_job_repository

router = APIRouter()


@router.post('/', response_model=Proposal)
async def send_proposal(
        proposal: ProposalIn,
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)
):
    if current_user.id != proposal.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")

    if job.get_object(proposal.job_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return await proposals.send_proposal(**proposal.dict())


@router.patch('/', response_model=Proposal)
async def reply_to_proposal(
        update: ProposalUpdateIn,
        proposal: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)
):
    current_job = await job.get_object(update.job_id)

    if current_job is None or current_job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")

    if await proposal.get_proposal(update.user_id, update.job_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return await proposal.reply_to_proposal(update)


@router.get('/{user_id}', response_model=List[Proposal])
async def user_proposal(
        user_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return await proposals.get_all_user_proposal(user_id)


@router.get('/candidates/{job_id}')
async def candidates_on_job(
        job_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository)
):
    current_job = await job.get_object(job_id)

    if current_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if current_user.id != current_job.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")

    return await proposals.get_all_candidates(job_id)


@router.get('/{user_id}/{job_id}')
async def proposal_detail(
        user_id: int,
        job_id: int,
        current_user: User = Depends(get_current_user),
        proposals: ProposalRepository = Depends(get_proposal_repository),
        job: JobRepository = Depends(get_job_repository)

):
    current_job = await job.get_object(job_id)

    if current_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")

    return await proposals.get_proposal(user_id, job_id)
