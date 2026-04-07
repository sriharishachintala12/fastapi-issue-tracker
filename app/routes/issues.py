from fastapi import APIRouter,HTTPException,status
from app.schemas import createIssue,updateIssue,getIssues
from app.storage import load_data,save_data
import uuid
router=APIRouter(prefix="/api/v1/issues")

@router.get("/",response_model=list[getIssues])
def get_issues():
    issues=load_data()
    return issues

@router.post("/",response_model=getIssues,
status_code=status.HTTP_201_CREATED)
def issueCreate(issue:createIssue):
    issues=load_data()
    new_issue={
        "id": str(uuid.uuid4()),
        "title": issue.title,
        "description": issue.description,
        "priority": issue.priority,
        "status": issue.status,
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue

@router.get("/{issue_id}",response_model=getIssues)
def getIssue_BYID(issue_id:str):
    issues=load_data()
    for issue in issues:
        if issue["id"]==issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Issue not found")

@router.put("/{issue_id}",response_model=getIssues)
def issueUpdate(issue_id:str,issue:updateIssue):
    issues=load_data()
    for index,uissue in enumerate(issues):
        if uissue["id"]==issue_id:
            update_issue=uissue.copy()
            if issue.title is not None:
                update_issue["title"]=issue.title
            if issue.description is not None:
                update_issue["description"]=issue.description
            if issue.priority is not None:
                update_issue["priority"]=issue.priority
            if issue.status is not None:
                update_issue["status"]=issue.status
            issues[index]=update_issue
            save_data(issues)
            return update_issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Issue Not Found")

@router.delete("/{issue_id}",status_code=status.HTTP_200_OK)
def deleteIssue(issue_id:str):
    issues=load_data()
    for index,issue in enumerate(issues):
        if issue["id"]==issue_id:
            issues.pop(index)
            save_data(issues)
            return {"message":issue_id+"  Deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No issue Found")
