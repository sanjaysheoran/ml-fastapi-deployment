# Deployment Challanges, logs and success results
1. Initially I created requirements.txt manually by providing the version of 5 library but after learning from class I used uv command to create requirements.txt from requirements.in. Which help us listing the version of library/package and also the dependent package so that whole team will have same behaviour
2. I was facing problem setting up conda environment on my local because pip was used from base environment and installing the packages in base packages. After installing pip on conda environment evrrything worked fine and I was able to execute the application on local
3. Initially I used docker build for creating image and then run for running the container with the port. Later I learned about docker compose file where I can provide the port and I just need to run docker compose up command to create image and run container.
4. Below are logs from docker showing application was running on port 8000 and then I hit the service for checking health and then predict the results.  
```web-1  | INFO:     Will watch for changes in these directories: ['/fastapiapp']
web-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
web-1  | INFO:     Started reloader process [7] using WatchFiles
web-1  | INFO:     Started server process [9]
web-1  | INFO:     Waiting for application startup.
web-1  | INFO:     Application startup complete.
web-1  | INFO:     172.19.0.1:62736 - "GET /docs HTTP/1.1" 200 OK
web-1  | INFO:     172.19.0.1:62736 - "GET /openapi.json HTTP/1.1" 200 OK
web-1  | INFO:     172.19.0.1:62736 - "GET /health HTTP/1.1" 200 OK
web-1  | /usr/local/lib/python3.11/site-packages/sklearn/utils/validation.py:2739: UserWarning: X does not have valid feature names, but RandomForestRegressor was fitted with feature names
web-1  |   warnings.warn(
web-1  | INFO:     172.19.0.1:62738 - "POST /predict HTTP/1.1" 200 OK ```
5. Git Actions build the application with every commit on main branch. This help developer for Continous integration and deployment. With the deployment it checks for container logs and also hit the health service to verify if service is running properly. Below are logs from action
```View container logs
Run docker compose logs
time="2026-08-16T02:26:35Z" level=warning msg="/home/runner/work/ml-fastapi-deployment/ml-fastapi-deployment/compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
web-1  | INFO:     Will watch for changes in these directories: ['/fastapiapp']
web-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
web-1  | INFO:     Started reloader process [7] using WatchFiles
Test if FastAPI responds
Run sleep 3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    27  100    27    0     0   3943      0 --:--:-- --:--:-- --:--:--  4500
{"status":"healthy server"}```.  

# Why I made particulat deployment/architecture decision
1. requirements.txt help keeping same version for all packages and dependencies for all team. So this will allow all developer to run the same version of packages and it will reproduce the same results.
2. conda environment help us maintaining multiple environment at same time. So that if we are working on 2 project with different version of libraries we would be able to manage it through different conda environments.
3. Docker gives developer the consistency with the environment. It allow us to create an image which we can deploy and run on docker container and it will have the same experience for all the developers using same container.
4. Git Action allow developers for continous integration, testing and deployment. So that as soon as developer commit something on specific branch. It will build, deploy and verify the test cases so that developer can see the changes without any delay.

# Results and logs
1. Application log on local
```docker compose up
WARN[0000] /Users/sanjaysheoran/Documents/ML-AI/VS-Folder/ml-fastapi-deployment/compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] up 1/1
 ✔ Container ml-fastapi-deployment-web-1 Recreated                                                          0.1s
Attaching to web-1
web-1  | INFO:     Will watch for changes in these directories: ['/fastapiapp']
web-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
web-1  | INFO:     Started reloader process [7] using WatchFiles
web-1  | INFO:     Started server process [9]
web-1  | INFO:     Waiting for application startup.
web-1  | INFO:     Application startup complete.
web-1  | INFO:     172.19.0.1:62736 - "GET /docs HTTP/1.1" 200 OK
web-1  | INFO:     172.19.0.1:62736 - "GET /openapi.json HTTP/1.1" 200 OK
web-1  | INFO:     172.19.0.1:62736 - "GET /health HTTP/1.1" 200 OK
web-1  | INFO:     172.19.0.1:62738 - "POST /predict HTTP/1.1" 200 OK```
2. Below is log file from git action where it is setting up a jobm starting a container and then checking the container and hitting the health service to make sure service is up and runnning.  
https://productionresultssa14.blob.core.windows.net/actions-results/6b234462-f219-4d41-b394-b602d63c1526/workflow-job-run-722cd570-cf9f-5855-b9ab-cc93594e7511/logs/job/job-logs.txt?rsct=text%2Fplain&se=2026-08-20T08%3A10%3A52Z&sig=Rf4L5B6uv6ATMBecy5nRU36%2BBxClCyjKM3JSWWco47Q%3D&ske=2026-08-20T09%3A21%3A41Z&skoid=ca7593d4-ee42-46cd-af88-8b886a2f84eb&sks=b&skt=2026-08-20T05%3A21%3A41Z&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skv=2025-11-05&sp=r&spr=https&sr=b&st=2026-08-20T08%3A00%3A47Z&sv=2025-11-05


# Key lessons learned and what you would change for a production deployment
1. Environment should be setup so that it would be same for all developer
2. System should support Developer to execute, deploy and validate the changes as soon as possible.
3. For this assignment, we used a simple model without any scaler but for production we need to update the model with additional customization including data cleaning, data validation, preprocessing, etc
4. Developer should be able to commit only for lower environment and there should be a process for merging all the changes from feature branch to main branch so that deployment to production should be more streamlined and individual developer should not be able to do the deployment on production.


# What’s different about deploying ML models vs normal software?  
1. For ML Models, we need to **save the models and preprocessors** with their corrosponding **versions**. While executing the model for any prediction, we need to use the latest model which is trained and verified with the corrosponding preprocessors.  
2. For ML Models, we need to monitor the **data and concept drift**. We can't keep using the same model without any monitoring. We need to observe the drift in the data as well in the model score. Data drift can be monitored using feature monitoring where as concept drift can be monitored using model score difference.  
3. For ML, we need to manage the model and features differently. We should keep the track of model(via version) using **Model Registry** and have a **versioned Dataset** so that we would be able to reproduce the same output from same dataset using same version of a model. And while predicting the results we should use the same preprocessors which was used while training the model.  
4. In both i.e. ML and normal software we should use the **best practices** like.  
    - Create a requirements.txt with all dependent libraries and their corrosponding version so that whole team will have exactly same behavious  
    - Use CI/CD for continous integration and deployment using Git action or Jenkins.  
    - Use Docker for running the code on exactly the same environment. and compose is to configure all different services at one place.  
    - Use Kubernete to run and manage the Docker containers with more controlled way.   
  
  
# What challenges might arise in production (data drift, scaling, monitoring)?  
There might be many challanges which might arise in production, but I want to highlight which are very common.  
1. **Data Drift** - While running the same model for long period of time there is a possibility of Data drift i.e. data may drift for a feature which is important for the model like mean, median, schema change, api not responding properly, new category introduced, etc. In that case model would be able to predict well. So in that case, we need to have monitoring in place which will monitor the features so that in case of any data drift team will get notified and they will look into the drift and plan for retrain the model
2. **Concept Drift** - While running the model for long time there is a possibility that data is similar but the model is not performing well and its score is degrading. This can happen with fraud detection model, etc where data is similar but model is not performing well because the user is recognizing the pattern to handle the model by avoid some keywords, etc. To handle we need to setup monitors for model score as well so that in case the model is not performing well then team should get alert and they would be able to investigate.
3. **Preprocessing** - In production, there is a possibility that the preprocessing done on inputs features while running the prediction are not same preprocessing done while training the model. We need to make sure that we should use exactly the same preprocessing while training the model and running to predict. Best way is the same the preprocessors while saving the model with version.
4. **Monitoring** - As mentioned earlier that we need to monitor the features for Data Drift and also need to monitor the model score for Concept drift. These monitoring should be configured with some alerts so that it will notify the correct group on time so that they can examine and avoide the degradation of model performance on production.
5. **ReTraining** - If we we get an alert because of data or concept drift, we should analyse and if required by then we should plan for retrain the model and come up with new model with the new preprocessor and save it in model registry with new version. While training we need to make sure that we are not overtraining the model. Model should be trained so that it would be able to recognize the pattern from features but not to remember based on training data. Once we are good with the new version of retraining, we should plan for deploying the new version of model so that we can test it first for few requests and varify if the model is scoring well for live data.