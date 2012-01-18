#Please note this only works for the IHP application

from submissions import models

def data():
    resp = {}
    for submission in models.Submission.objects.all():
        q = {}
        for question in submission.dpquestion_set.all():
            q['agency'] = q.get('agency',{})
            q['agency'][question.question_number] = {
                    'baseline':(question.baseline_year,question.baseline_value), 
                    'latest':(question.latest_year,question.latest_value), 
                    'comment':question.comments
                }

        for question in submission.govquestion_set.all():
            q['gov'] = q.get('gov',{})
            q['gov'][question.question_number] = {
                    'baseline':(question.baseline_year,question.baseline_value), 
                    'latest':(question.latest_year,question.latest_value), 
                    'comment':question.comments
                }
        resp[submission.agency.agency] = resp.get(submission.agency.agency,{})
        resp[submission.agency.agency][submission.country.country] = q
    return resp
    
